import argparse
import openreview
import csv
import config

## Argument handling
parser = argparse.ArgumentParser()
parser.add_argument('csv', help="input file with emails, first_name, last_name")
parser.add_argument('datestring', help="append to output file name")
parser.add_argument('--baseurl', help="base url")
parser.add_argument('--username')
parser.add_argument('--password')
args = parser.parse_args()

client = openreview.Client(baseurl=args.baseurl, username=args.username, password=args.password)
print "connecting to ", client.baseurl
datestring = args.datestring

## intersect reviewers file (ICLR Conference) and reviewers group (only ICLR Workshop)
workshop_reviewers = client.get_group('ICLR.cc/2018/Workshop/Reviewers')
## get all members that are in email form, get their profiles to get ~ids
emails = []
workshop_reviewers = workshop_reviewers.members
for name in workshop_reviewers:
    if '@' in name:
        emails.append(name)
email_profiles = client.get_profiles(emails)
for p in email_profiles:
    workshop_reviewers.append(p['profile']['id'])

# load in ICLR reviewers from file
ids_by_email = {}
names_by_email = {}
with open(args.csv) as f:
    for email, first, last in csv.reader(f):
        ids_by_email[email] = ""
        names_by_email[email] = (first, last)

# get profiles from list of emails
iclr_profiles = client.get_profiles(names_by_email.keys())
for profile in iclr_profiles:
    ids_by_email[profile['email']] = profile['profile']['id']

# remove ICLR members that aren't on workshop_reviewers list
# check for profile id, email and created tilde_id (in case given email not part of profile)
for email in ids_by_email:
    if ids_by_email[email] not in workshop_reviewers and email not in workshop_reviewers:
        tilde_name = "~{0}_{1}1".format(names_by_email[email][0], names_by_email[email][1])
        if tilde_name not in workshop_reviewers:
            del names_by_email[email]

print len(names_by_email)

# print out new reviewers list
f = open('../data/tpms/reviewers-{0}.csv'.format(datestring), 'w')
writer = csv.writer(f)
for email in names_by_email:
    writer.writerow([email,names_by_email[email][0],names_by_email[email][1]])

f.close()


