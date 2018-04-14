'''
This script is used to import the ECCV reviewers from ReSearcher profiles to OpenReview.

There is no argument parsing because this is a hack that should only be executed once, and NEVER on the live site!

It requires several files that are not checked into source control. If for some reason you want to run this script,
talk to Michael about getting the following directories and files:

../data/researcher-08-04-18/json
../data/researcher-08-04-18/missing-reviewers-json
../data/missing-reviewers-2018-04-08-1102.csv
../data/reviewers.csv

'''

import openreview
client = openreview.Client()
print client.baseurl

import openreview_matcher
from openreview_matcher.solver import Solver
from openreview import tools
import csv

import os
from shutil import copyfile, rmtree


from import_user import *

'''
Find files for missing reviewers and copy them over into the missing-reviewers-json subdirectory.

The users that have researcher profiles will be found and moved into the missing-reviewers-json subdirectory.

Reviewers with *no* researcher profile are put into the no_profiles list.
'''

no_profiles = []

researcher_json_dir = '../data/researcher-08-04-18/json/'
missing_reviewer_json_dir = '../data/researcher-08-04-18/missing-reviewers-json/'
if os.path.isdir(missing_reviewer_json_dir):
    rmtree(missing_reviewer_json_dir)

os.makedirs(missing_reviewer_json_dir)

with open('../data/missing-reviewers-2018-04-11-1104.csv') as f:
    reader = csv.reader(f)
    for row in reader:
        missing_email = row[0].lower().strip()
        researcher_json_path = '{}{}.json'.format(researcher_json_dir, missing_email)
        if os.path.isfile(researcher_json_path):
            copyfile(researcher_json_path, researcher_json_path.replace('/json/','/missing-reviewers-json/'))
        else:
            no_profiles.append(missing_email)


def Files(directory):
    for filename in os.listdir(directory):
        if filename.endswith('.json'):
            yield os.path.join(directory, filename)

files = Files('../data/researcher-08-04-18/missing-reviewers-json/')

'''
Among the missing reviewers that have researcher profiles, import them into OpenReview
'''

precreated_profiles = []
failed_profile_emails = []
for filename in files:
    profile_data, resolved = import_user(client, filename)

    profile_id = ''
    if resolved:
        profile_note = openreview.Note(**profile_data)
        updated_profile = client.update_profile(profile_note.id, profile_note.content)
        precreated_profiles.append(updated_profile)
    else:
        email = filename.split('/')[-1].replace('.json', '').lower().strip()
        failed_profile_emails.append(email)

'''
Now pre-create profiles for all the reviewers that *don't* have researcher profiles,
or whose researcher profiles were invalid.

These reviewer emails are in the no_profiles list and the failed_profile_emails list
'''

with open('../data/reviewers.csv') as f:
    reader = csv.reader(f)
    reader.next()
    for row in reader:
        first = row[0]
        last = row[2]
        email = row[3].lower().strip()
        if email in no_profiles + failed_profile_emails:
            profile_note = openreview.tools.create_profile(client, email, first, last, allow_duplicates=True)
            print profile_note.id
