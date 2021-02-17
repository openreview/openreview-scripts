'''
1) Reviewers: The reviewer list should be in csv file.

    - in csv format: ReviewerEmail,FirstName,LastName,<comma-separated-additional-emails>

'''

import argparse
import openreview
import csv
from openreview import tools

## Argument handling
parser = argparse.ArgumentParser()
parser.add_argument('--baseurl', help="base url")
parser.add_argument('--username')
parser.add_argument('--password')
args = parser.parse_args()

client = openreview.Client(baseurl=args.baseurl, username=args.username, password=args.password)

reviewers_group = client.get_group(id='MIDL.io/2021/Conference/Reviewers')

no_profile = []
rows = []
for email in reviewers_group.members:
    row = []
    profile = openreview.tools.get_profile(client, email)
    if(profile):
        preferred_email = profile.content.get('preferred_email', None)
        emails = profile.content.get('emails')
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
    else:
        no_profile.append(email)
for email in no_profile:
    rows.append([email])

with open('MIDL2021-tpms-reviewers-dump.csv', 'w') as f:
    writer = csv.writer(f)
    for row in rows:
        writer.writerow(row)

print(len(no_profile), 'reviewers with no profile')