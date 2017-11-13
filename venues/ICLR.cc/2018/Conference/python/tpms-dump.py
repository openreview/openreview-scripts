import argparse
import openreview
import csv
import config
import operator
from collections import defaultdict

## Argument handling
parser = argparse.ArgumentParser()
parser.add_argument('csv')
parser.add_argument('datestring')
parser.add_argument('--baseurl', help="base url")
parser.add_argument('--username')
parser.add_argument('--password')
args = parser.parse_args()

client = openreview.Client(baseurl=args.baseurl, username=args.username, password=args.password)
print "connecting to ", client.baseurl
datestring = args.datestring

# create mapping from email --> first,last
names_by_email = {}

with open(args.csv) as f:
    for email, first, last in csv.reader(f):
        names_by_email[email] = (first, last)

print "retrieving profiles where available ..."
signature_by_email = {}
profile_by_email = {}
for email, names in names_by_email.iteritems():
    try:
        profile = client.get_profile(email)
        profilenote = client.get_note(profile.id)
        signature_by_email[email] = profile.id
        profile_by_email[email] = profilenote
    except openreview.OpenReviewException as e:
        signature_by_email[email] = None
        profile_by_email[email] = None

email_by_signature = {v:k for k,v in signature_by_email.iteritems()}

# get all bids
bids = client.get_tags(invitation='ICLR.cc/2018/Conference/-/Add_Bid')
print "retrieved {0} bids".format(len(bids))

# dump the bids to a csv file
blind_submissions = client.get_notes(invitation=config.BLIND_SUBMISSION)

blind_by_forum = {n.forum: n for n in blind_submissions}

bidscore = {
    'I want to review': 4,
    'I can review': 3,
    'I can probably review but am not an expert': 2,
    'I cannot review': 1
}

bad_forums = set()

rows = []

for b in bids:
    try:
        number = blind_by_forum[b.forum].number
        if b.tag.lower() != 'no bid':
            signature = b.signatures[0].encode('utf8')
            email = email_by_signature[signature]
            rows.append([email, 'Paper{0}'.format(number), bidscore[b.tag]])
    except KeyError as e:
        bad_forums.update(e)

rows = sorted(rows, key=lambda x: (x[0], int(x[1].split('Paper')[1])))

with open('../data/tpms/bids-{0}.csv'.format(datestring), 'w') as f:
    writer = csv.writer(f)
    for r in rows:
        writer.writerow(r)


'''
dump conflicts of interest.

Things to get:

For each email, find all the domains that they are affiliated with.

{
    email: { 'domains': [brown.edu, cs.umass.edu], 'relations': [serre@brown.edu, mccallum@cs.umass.edu]}
}

for each paper, find all the domains that are affiliated with the paper.

{
    1123: { 'domains': [brown.edu], 'relations': ['amso@brown.edu']}
}

Generated conflicts from the intersection.

Important note: removes conflicts from the domain "@gmail.com"
'''


def get_domains(email):
    full_domain = email.split('@')[1]
    domain_components = full_domain.split('.')
    domains = ['.'.join(domain_components[index:len(domain_components)]) for index, path in enumerate(domain_components)]
    valid_domains = [d for d in domains if '.' in d]
    return valid_domains


conflicts_by_email = {}

for email in names_by_email:
    conflicts_by_email[email] = {}
    conflicts_by_email[email]['domains'] = set()
    conflicts_by_email[email]['domains'].update(get_domains(email))

    conflicts_by_email[email]['relations'] = set()
    conflicts_by_email[email]['relations'].update([email])
    profile = profile_by_email[email]
    if profile != None:
        profile_domains = []
        for e in profile.content['emails']:
            profile_domains += get_domains(e)

        conflicts_by_email[email]['domains'].update(profile_domains)

        institution_domains = [h['institution']['domain'] for h in profile.content['history']]
        conflicts_by_email[email]['domains'].update(institution_domains)

        if 'relations' in profile.content:
            conflicts_by_email[email]['relations'].update([r['email'] for r in profile.content['relations']])

    # remove the domain "gmail.com"
    if 'gmail.com' in conflicts_by_email[email]['domains']:
        conflicts_by_email[email]['domains'].remove('gmail.com')

submissions = client.get_notes(invitation=config.SUBMISSION)
conflicts_by_paper = {}

for n in submissions:
    authorids = n.content['authorids']
    conflicts_by_paper[n.number] = {}
    conflicts_by_paper[n.number]['domains'] = set()

    for e in authorids:
        if '@' in e:
            conflicts_by_paper[n.number]['domains'].update(get_domains(e))

    conflicts_by_paper[n.number]['relations'] = set([e for e in authorids if '@' in e])

    # remove the domain "gmail.com"
    if 'gmail.com' in conflicts_by_paper[n.number]['domains']:
        conflicts_by_paper[n.number]['domains'].remove('gmail.com')

# write the conflicts

f = open('../data/tpms/conflicts-{0}.csv'.format(datestring), 'w')
writer = csv.writer(f)

for email, email_conflict in sorted(conflicts_by_email.iteritems()):
    for papernumber, paper_conflict in conflicts_by_paper.iteritems():
        if paper_conflict['domains'] and email_conflict['domains']:
            domain_conflict = paper_conflict['domains'].intersection(email_conflict['domains'])
        else:
            domain_conflict = None

        if paper_conflict['relations'] and email_conflict['relations']:
            relation_conflict = paper_conflict['relations'].intersection(email_conflict['relations'])
        else:
            relation_conflict = None

        if domain_conflict or relation_conflict:
            writer.writerow([email,'Paper{0}'.format(papernumber)])

f.close()


