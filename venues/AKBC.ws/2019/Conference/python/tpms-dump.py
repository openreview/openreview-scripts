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
import iclr19

## Argument handling
parser = argparse.ArgumentParser()
parser.add_argument('label')
parser.add_argument('--baseurl', help="base url")
parser.add_argument('--username')
parser.add_argument('--password')
args = parser.parse_args()

client = openreview.Client(baseurl=args.baseurl, username=args.username, password=args.password)

# At this point, all reviewers & ACs should have been
# converted to profile IDs and deduplicated.
reviewers_group = client.get_group(iclr19.REVIEWERS_ID)
if not all(['~' in member for member in reviewers_group.members]):
    print('WARNING: not all reviewers have been converted to profile IDs. Members without profiles will not have metadata created.')
valid_reviewer_ids = [r for r in reviewers_group.members if '~' in r]

reviewer_profiles = client.get_profiles(valid_reviewer_ids)

areachairs_group = client.get_group(iclr19.AREA_CHAIRS_ID)
if not all(['~' in member for member in areachairs_group.members]):
    print('WARNING: not all area chairs have been converted to profile IDs. Members without profiles will not have metadata created.')
valid_ac_ids = [r for r in areachairs_group.members if '~' in r]

ac_profiles = client.get_profiles(valid_ac_ids)

user_profiles = ac_profiles + reviewer_profiles

rows = []

for profile in user_profiles:
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

with open('../data/{}-tpms-reviewers-dump.csv'.format(args.label), 'w') as f:
    writer = csv.writer(f)
    for row in rows:
        writer.writerow(row)



