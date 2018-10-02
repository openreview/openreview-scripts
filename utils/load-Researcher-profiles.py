#!/usr/bin/python

###############################################################################
# Load json files into profiles
###############################################################################

## Import statements
import argparse
import json
import os
import openreview
from openreview import tools

## Argument handling
parser = argparse.ArgumentParser()
parser.add_argument('directory', help = "the full path to the JSON files")
parser.add_argument('--baseurl', help="base url")
parser.add_argument('--username')
parser.add_argument('--password')
source_entity = 'Researcher.cc'
source_id = source_entity+'/Upload'

def init_source_groups(client):
    # create the source groups (or overwrite it if it exists)
    source_group = openreview.Group(id=source_entity, signatures=['OpenReview.net'],
                                   signatories=[source_entity], readers=[source_entity],
                                   writers=['OpenReview.net'], members=[])
    client.post_group(source_group)
    source_id_group = openreview.Group(id=source_id, signatures=['OpenReview.net'],
                                   signatories=[source_id], readers=[source_id],
                                   writers=['OpenReview.net'], members=[])
    client.post_group(source_id_group)

def  get_all_profiles(client):
    # Pull all of the profile info in at once to # of calls by getting them one at a time
    # To determine ids for all profiles, get all groups w/ tilde_id names as an id.
    print("Loading profiles...")
    profile_groups = list(tools.iterget(client.get_groups, id='~.*'))
    tilde_ids = []
    for group in profile_groups:
        tilde_ids.append(group.id)

    # get all profiles associated with the tilde_ids
    all_profiles = []
    for i in range(0, len(tilde_ids), 100):
        all_profiles.extend(client.get_profiles(tilde_ids[i:i + 100]))

    # store the profiles in easy to access dictionaries
    # stored by id and by email
    profiles_by_id = {}
    profiles_by_email = {}
    for profile in all_profiles:
        profiles_by_id[profile.id] = profile
        for email in profile.content['emails']:
            profiles_by_email[email]= profile

    print("Retrieved profiles")
    return profiles_by_id, profiles_by_email

def print_status(file_count, total_files, one_percent, filename):
    # print progress
    file_count += 1
    if file_count / one_percent == file_count // one_percent:
        print("{0}% complete {1}".format(file_count * 100 / total_files, filename))
    return file_count

def repair_dates(imported_content):
    # replaces values of -1 with None
    for fieldname in ['history', 'relations', 'expertise']:
        if fieldname in imported_content:
            for entry in imported_content[fieldname]:
                for key in entry.keys():
                    if entry[key] == '-1':
                        entry[key] = None
    return imported_content

def repair_email(email):
    # remove <> around email, strip off spaces and ensure email in lower case
    if '<' in email:
        email = email.split('<')[1]
    if '>' in email:
        email = email.split('>')[0]
    email = email.strip()
    email = email.lower()
    return email

def load_json_content(filename):
    data = None
    if filename.endswith('.json'):
        with open(filename) as infile:
            try:
                json_data = json.load(infile)
                data = repair_dates(json_data.get('content', json_data))
            except ValueError as e:
                print("{}: {}".format(filename, e))

    return data

def load_json_file(dirpath, filename):
    # create main_email from filename
    main_email = filename.split('/')[-1].replace('.json','').strip()

    emails = [main_email]
    name = {}
    imported_profile_content = load_json_content(dirpath+'/'+filename)
    if imported_profile_content:
        for name_entry in imported_profile_content['names']:
            if name_entry.get('first') and name_entry.get('last'):
                name = name_entry
                break

        other_emails = imported_profile_content.get('emails', [])
        emails += other_emails
        emails = [repair_email(e) for e in emails]
        imported_profile_content['emails'] = emails

        converted_name = {'first':name.get('first',''), 'middle':name.get('middle',''), 'last':name.get('last','')}
        imported_profile_content['names'].insert(0,converted_name)
    return imported_profile_content

def main():
    args = parser.parse_args()

    ## Initialize the client library with username and password.
    client = openreview.Client(baseurl=args.baseurl, username=args.username, password=args.password)
    init_source_groups(client)

    # get list of files in directory or list is just one file
    dirpath = args.directory
    if os.path.isdir(dirpath):
        file_names = os.listdir(dirpath)
    else:
        file_names = [dirpath.split('/')[-1]]
        dirpath = dirpath[:-len(file_names[0])]

    # initialize counts
    num_new = 0
    num_updates = 0
    total_files = len(file_names)
    file_count = 0
    one_percent = total_files//100.0
    if one_percent < 1:
        one_percent = 1

    profiles_by_id, profiles_by_email = get_all_profiles(client)

    for filename in file_names:
        file_count = print_status(file_count, total_files, one_percent, filename)

        new_profile_content = load_json_file(dirpath, filename)
        if new_profile_content:
            main_email = new_profile_content['emails'][0]
            if main_email in profiles_by_email.keys():
                # profile exists, add new reference
                existing_profile = profiles_by_email[main_email]
                profile = openreview.Profile(referent=existing_profile.id,
                                             invitation=existing_profile.invitation,
                                             signatures=[source_id],
                                             writers=[source_id],
                                             content=new_profile_content)
                profile = client.update_profile(profile)
                '''   except openreview.OpenReviewException as e:
                        print("OpenReviewException {}".format(e))
                        print(id)'''
                num_updates += 1
            else:
                # profile doesn't exist, try creating it
                try:
                    tools.create_profile(client, main_email, new_profile_content['names'][0]['first'],
                                         new_profile_content['names'][0]['last'],
                                         middle=new_profile_content['names'][0]['middle'], allow_duplicates=True)
                    num_new += 1
                except openreview.OpenReviewException as e:
                    # can be unhappy if name includes parenthesis etc
                    # in this case it is OK to skip it
                    print("Error with {} {}".format(filename, e))
                    continue


if __name__ == "__main__":
    main()
