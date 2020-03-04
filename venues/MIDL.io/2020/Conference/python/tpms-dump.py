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
parser.add_argument('label')
parser.add_argument('--baseurl', help="base url")
parser.add_argument('--username')
parser.add_argument('--password')
args = parser.parse_args()

client = openreview.Client(baseurl=args.baseurl, username=args.username, password=args.password)

reviewers_group = client.get_group(id='MIDL.io/2020/Conference/Reviewers')

areachairs_group = client.get_group(id='MIDL.io/2020/Conference/Area_Chairs')

rows = []
count = 0
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
    else:
        count+=1
        row.append(email)
    rows.append(row)

with open('{}-tpms-reviewers-dump.csv'.format(args.label), 'w') as f:
    writer = csv.writer(f)
    for row in rows:
        writer.writerow(row)

print(count, 'reviewers with no profile')

rows = []
count = 0
for email in areachairs_group.members:
    row = []
    profile = None
    try:
        profile = client.get_profile(email_or_id = email)
    except:
        pass
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
        
    else:
        count+=1
        row.append(email)
    rows.append(row)

with open('{}-tpms-ACs-dump.csv'.format(args.label), 'w') as f:
    writer = csv.writer(f)
    for row in rows:
        writer.writerow(row)

print(count, 'ACs with no profile')



