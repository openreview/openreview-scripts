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

def suggest_username(first, middle, last, client):
    response = requests.get(
        client.baseurl + '/tildeusername?first={first}&middle={middle}&last={last}'.format(
            first=first, middle=middle, last=last))

    if response.json().get('username'):
        suggested_username = response.json()['username']
        return suggested_username
    else:
        return None

def get_profile(email, name, imported_profile_content, client):
    exists = True
    try:
        profile = client.get_profile(email)
        profile = client.get_note(profile.id)
    except openreview.OpenReviewException as e:
        if 'Profile not found' in e[0]:
            profile = openreview.Note(**{
                    'invitation': '~/-/profiles',
                    'writers': ['OpenReview.net'],
                    'signatures': ['OpenReview.net'],
                    'readers': ['OpenReview.net'],
                    'content': {
                        'emails': [email],
                        'preferred_email': email
                    }
                })
        else:
            raise(e)

    if not profile.id:
        exists = False
        # get the first name that has at least a first and a last name

        profile.id = suggest_username(name['first'].encode('utf-8'), name['middle'].encode('utf-8'), name['last'].encode('utf-8'), client)
        profile.readers.append(profile.id)

    return profile, exists

def update_dblp(existing_content, imported_content):
    if not existing_content.get('dblp', None):
        existing_content['dblp'] = imported_content['dblp']

def update_names(existing_content, imported_content):
    for n in imported_content['names']:
        if 'preferred' in n and n['preferred']:
            n['preferred'] = False

    if 'names' in existing_content:
        existing_names = [
            '{}_{}_{}'.format(
                n['first'].encode('utf-8'),
                n['middle'].encode('utf-8'),
                n['last'].encode('utf-8')) for n in existing_content['names']]

        for name_entry in imported_content['names']:
            name_id = '{}_{}_{}'.format(
                name_entry['first'].encode('utf-8'),
                name_entry['middle'].encode('utf-8'),
                name_entry['last'].encode('utf-8'))

            if name_id not in existing_names:
                existing_content['names'].append(name_entry)
    else:
        existing_content['names'] = imported_content['names']
        # if there are no existing preferred names, set the first name as preferred.
        existing_content['names'][0]['preferred'] = True

def update_dated_field(imported_content, fieldname):
    for entry in imported_content[fieldname]:
        for key in entry.keys():
            if entry[key] == '-1':
                entry[key] = None

def update_relations(existing_content, imported_content):
    email_regex = re.compile('^([a-zA-Z0-9_\-\.]+)@([a-zA-Z0-9_\-\.]+)\.([a-zA-Z]{2,5})$')

    if not 'relations' in existing_content:
        existing_content['relations'] = imported_content['relations']
    else:
        existing_relations = ['{}_{}'.format(n['name'].encode('utf-8'), n['email']) for n in existing_content['relations']]

        for relation_entry in imported_content['relations']:
            if email_regex.match(relation_entry['email']):
                relation_id = '{}_{}'.format(relation_entry['name'].encode('utf-8'), relation_entry['email'])
                if relation_id not in existing_relations:
                    existing_content['relations'].append(relation_entry)

def update_history(existing_content, imported_content):
    if not 'history' in existing_content:
        existing_content['history'] = imported_content['history']
    else:
        existing_histories = ['{}_{}_{}_{}_{}'.format(
            h['start'],
            h['end'],
            h['position'].encode('utf-8'),
            h['institution']['name'].encode('utf-8'),
            h['institution']['domain']) for h in existing_content['history']]

        for history_entry in imported_content['history']:
            history_id = '{}_{}_{}_{}_{}'.format(
                history_entry['start'],
                history_entry['end'],
                history_entry['position'].encode('utf-8'),
                history_entry['institution']['name'].encode('utf-8'),
                history_entry['institution']['domain'].encode('utf-8'))
            if history_id not in existing_histories:
                existing_content['history'].append(history_entry)

def process_content(existing_content, imported_content):
    update_dated_field(imported_content, 'history')
    update_dated_field(imported_content, 'relations')

    for update in [update_dblp, update_names, update_history, update_relations]:
        update(existing_content, imported_content)

    return existing_content

def post_profile(profile, exists, client):
    put_or_post = requests.post if exists else requests.put

    response = put_or_post(client.baseurl + '/user/profile',
        json = profile.to_json(),
        headers = client.headers)

    return response.json()['id']


def update_user_groups(profile, client):
    email_groups = []
    for email in profile.content['emails']:
        try:
            email_group = client.get_group(email)
        except openreview.OpenReviewException as e:
            if e[0][0]['type'] == 'Not Found':
                email_group = openreview.Group(**{
                    'id': email,
                    'signatures': ['OpenReview.net'],
                    'signatories': [email],
                    'readers': [email],
                    'writers': [email]
                    })
            else:
                raise e
        email_groups.append(email_group)

    name_groups = []
    for name_entry in profile.content['names']:
        if 'username' in name_entry and name_entry['username']:
            name_group = client.get_group(name_entry['username'])
        else:
            name_id = suggest_username(name_entry['first'].encode('utf-8'), name_entry['middle'].encode('utf-8'), name_entry['last'].encode('utf-8'), client)

            name_group = openreview.Group(**{
                'id': name_id,
                'signatures': ['OpenReview.net'],
                'signatories': [name_id],
                'readers': [name_id],
                'writers': [name_id]
                })

            name_entry['username'] = name_id
        name_groups.append(name_group)

        for email_group in email_groups:
            if email_group.id not in name_group.members:
                name_group.members.append(email_group.id)
            if name_group.id not in email_group.members:
                email_group.members.append(name_group.id)

    all_groups = name_groups + email_groups

    return all_groups



#filename = '../data/researcher-json/william.l.spector@gmail.com.json'
#filename = '../data/researcher-json/akobren@cs.umass.edu.json'

def import_user(filename, client):
    main_email = filename.split('/')[-1].replace('.json','').strip()
    email_regex = re.compile('^([a-zA-Z0-9_\-\.]+)@([a-zA-Z0-9_\-\.]+)\.([a-zA-Z]{2,5})$')

    error_type = None
    name = None
    with open(filename) as infile:
        try:
            imported_profile_content = json.load(infile)
            for name_entry in imported_profile_content['names']:
                if name_entry.get('first') and name_entry.get('last'):
                    name = name_entry
                    break
            if not name:
                error_type = 'missing_name'
            else:
                if not suggest_username(name['first'].encode('utf-8'),
                    name['middle'].encode('utf-8'),
                    name['last'].encode('utf-8'),
                    client):
                    error_type = 'invalid_name'

        except ValueError as e:
            error_type = 'bad_json'

    if not email_regex.match(main_email):
        error_type = 'bad_filename'

    if not error_type:
        profile, exists = get_profile(main_email, name, imported_profile_content, client)

        process_content(profile.content, imported_profile_content)

        groups = update_user_groups(profile, client)

        for g in groups:
            new_group = client.post_group(g)

        return post_profile(profile, exists, client), None

    else:
        return filename, error_type




