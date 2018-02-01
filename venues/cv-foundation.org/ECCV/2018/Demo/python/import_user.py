'''
Given a directory full of json files, formatted as $EMAIL_ADDRESS$.json,
process each file as follows:

1) if the email address does not belong to any existing OpenReview profile,
pre-create a new (inactive) profile for that email address.

2) if the email address *does* belong to an existing OpenReview profile,
try to merge them in a way that keeps as much information as possible.
Then, email the user to let them know that they should check and correct
their profile information.

'''

import openreview
import requests
import csv
import argparse
import os
import json
import re

def load_researcher_data(filename):
    with open(filename) as infile:
        return repair_dates(json.load(infile))
def repair_dates(imported_content):
    for fieldname in ['history', 'relations', 'expertise']:
        if fieldname in imported_content:
            for entry in imported_content[fieldname]:
                for key in entry.keys():
                    if entry[key] == '-1':
                        entry[key] = None
    return imported_content

def signup_details(filename):
    main_email = filename.split('/')[-1].replace('.json','').strip()

    imported_profile_content = load_researcher_data(filename)

    for name_entry in imported_profile_content['names']:
        if name_entry.get('first') and name_entry.get('last'):
            name = name_entry
            break

    other_emails = imported_profile_content.get('emails', [])
    emails = [main_email] + other_emails

    return emails, name['first'].encode('utf-8'), name['middle'].encode('utf-8'), name['last'].encode('utf-8'), imported_profile_content

def merge_relations(old_relations, new_relations):
    updated_relations = []
    existing_keys = []

    def get_relation_key(relation_entry):
        if relation_entry.get('name', None):
            return '{}_{}'.format(
                re.sub('\s+','-', relation_entry['name'].encode('utf-8')),
                relation_entry['relation']
            )
        else:
            return False

    for new_entry in new_relations + old_relations:
        '''
        If the new entry has a name and a unique key, add it.
        If the new entry matches the key of an old entry,
            but the time range falls *outside* of the old one, add it.
        '''

        new_entry_key = get_relation_key(new_entry)
        if new_entry_key not in existing_keys:
            updated_relations.append(new_entry)
            existing_keys.append(get_relation_key(new_entry))
        else:
            old_entry = [e for e in updated_relations if get_relation_key(e) == new_entry_key][0]
            merged_entry = {k:v for k,v in old_entry.iteritems()} # copy the old entry

            merged_entry['start'] = min(new_entry.get('start'), old_entry.get('start'))
            merged_entry['end'] = max(new_entry.get('end'), old_entry.get('end'))

            updated_relations.remove(old_entry)
            updated_relations.append(merged_entry)

    updated_relations.sort(key=lambda x: x['name'].encode('utf-8'), reverse=True)
    updated_relations = sorted(updated_relations, key=lambda x: int(x['end']) if x['end']!=None else float('inf'), reverse=True)

    return updated_relations

def merge_names(old_names, new_names):
    updated_names = []
    existing_keys = []

    def get_name_key(name_entry):
        if 'first' in name_entry and 'last' in name_entry and 'middle' in name_entry:
            return '{}_{}_{}'.format(
                name_entry['first'].encode('utf-8'),
                name_entry['middle'].encode('utf-8'),
                name_entry['last'].encode('utf-8')
            )
        else:
            return False

    for new_entry in old_names + new_names:
        new_entry_key = get_name_key(new_entry)

        if new_entry_key not in existing_keys:
            updated_names.append(new_entry)
            existing_keys.append(new_entry_key)

    return updated_names

def merge_history(old_history, new_history):
    updated_history = []
    existing_keys = []

    def get_history_key(history_entry):
        if 'institution' in history_entry and 'position' in history_entry:
            return '{}_{}'.format(history_entry['institution']['name'].encode('utf-8'), history_entry['position'].encode('utf-8'))
        else:
            return False

    for new_entry in old_history + new_history:
        new_entry_key = get_history_key(new_entry)
        if new_entry_key not in existing_keys:
            updated_history.append(new_entry)
            existing_keys.append(get_history_key(new_entry))
        else:
            old_entry = [e for e in updated_history if get_history_key(e) == new_entry_key][0]
            merged_entry = {k:v for k,v in old_entry.iteritems()} # copy the old entry

            merged_entry['start'] = min(new_entry.get('start'), old_entry.get('start'))
            merged_entry['end'] = max(new_entry.get('end'), old_entry.get('end'))

            updated_history.remove(old_entry)
            updated_history.append(merged_entry)

    updated_history = sorted(updated_history, key=lambda x: int(x['end']) if x['end']!=None else float('inf'), reverse=True)
    return updated_history

def merge_researcher_data(profile_note, researcher_data):
    new_names = researcher_data['names']
    new_relations = researcher_data['relations']
    new_history = researcher_data['history']

    for fieldname in ['dblp', 'gscholar', 'wikipedia', 'linkedin', 'homepage']:
        if profile_note.content.get(fieldname, None) and researcher_data.get(fieldname, None):
            profile_note.content[fieldname] = researcher_data.get(fieldname)

    email_set = set(profile_note.content['emails'])
    email_set.update(set(researcher_data.get('emails', [])))
    updated_email_list = list(email_set)
    profile_note.content['emails'] = updated_email_list

    profile_note.content['names'] = merge_names(profile_note.content.get('names',[]), new_names)
    profile_note.content['relations'] = merge_relations(profile_note.content.get('relations',[]), new_relations)
    profile_note.content['history'] = merge_history(profile_note.content.get('history',[]), new_history)

    return profile_note

def import_user(client, filename, id=None):
    '''
    the @id argument should be a user ID.
    if @id != None, do a forced update of that profile.
    '''

    emails, first, middle, last, researcher_data = signup_details(filename)
    # the goal here is to get a profile note, or to determine that the record is unresolvable.

    profile_note = None
    email_profile = None
    resolved = False # resolved is True if a profile was successfully created or updated

    for email in emails:
        try:
            email_profile = client.get_profile(email)
            break
        except openreview.OpenReviewException as error:
            if 'Profile not found' in error[0][0]:
                pass
            else:
                raise error

    if not email_profile:
        try:
            profile_note = openreview.tools.create_profile(client, emails[0], first, last, middle=middle)
        except openreview.OpenReviewException as error:
            # If, at this point, there is someone with the same name as this user,
            # then the record is unresolvable, because we have already checked the
            # email addresses in this record for existing profiles.

            if not id and 'There is already a profile with this first' in error[0]:
                return researcher_data, resolved
            elif id:
                profile_note = client.get_note(id)

    else:
        profile_note = client.get_note(email_profile.id)

    if profile_note:
        resolved = True
        profile_note = merge_researcher_data(profile_note, researcher_data)
        return profile_note.to_json(), resolved

    return profile_note, resolved
