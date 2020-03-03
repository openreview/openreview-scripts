'''
1) Reviewers: The reviewer list should be in csv file.

    - in csv format: ReviewerEmail,FirstName,LastName,<comma-separated-additional-emails>

2) Papers: Once the deadline has passed you package and provide TPMS
with all of the submissions, in pdf format. The simplest, given the
size of that file, is probably for me to download that package from
some server.

  - papers should be given a numeric ID and files should be named:
      paperID.pdf (e.g., paper134.pdf)
'''

import argparse
import openreview
import csv
from tqdm import tqdm

def get_valid_profiles(client, group_id):
    group = client.get_group(group_id)
    if not all(['~' in member for member in group.members]):
        print('WARNING: not all members of {0} have been converted to profile IDs.'.format(group_id))
    valid_tildes = [r for r in group.members if r.startswith('~')]
    return client.search_profiles(ids = valid_tildes)


## Argument handling
parser = argparse.ArgumentParser()
parser.add_argument('--baseurl', help="base url")
parser.add_argument('--username')
parser.add_argument('--password')
args = parser.parse_args()

client = openreview.Client(baseurl=args.baseurl, username=args.username, password=args.password)

# At this point, all reviewers & ACs should have been
# converted to profile IDs and deduplicated.

valid_reviewer_profiles = get_valid_profiles(client, 'thecvf.com/ECCV/2020/Conference/Reviewers')

valid_ac_profiles = get_valid_profiles(client, 'thecvf.com/ECCV/2020/Conference/Area_Chairs')

user_profiles = valid_ac_profiles + valid_reviewer_profiles

rows = []

for profile in tqdm(user_profiles):
    row = []
    preferred_email = profile.content.get('preferred_email', None)
    emails = profile.content.get('emails', [])
    if not emails:
        print('No emails in profile {}'.format(profile.id))
    else:
        if not preferred_email:
            preferred_email = emails[0]
        row.append(preferred_email)
        name = openreview.tools.get_preferred_name(profile)
        name_parts = name.split(' ')
        firstname = name_parts[0]
        lastname = name_parts[-1]
        row.append(firstname)
        row.append(lastname)
        for email in [e for e in emails if e != preferred_email]:
            row.append(email)
        rows.append(row)

with open('../data/ECCV2020-tpms-reviewers-dump.csv', 'w') as f:
    writer = csv.writer(f)
    writer.writerows(rows)



