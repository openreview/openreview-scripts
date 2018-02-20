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

# create mapping from email --> first,last
names_by_email = {}

with open(args.csv) as f:
    for email, first, last in csv.reader(f):
        names_by_email[email] = (first, last)

print "retrieving profiles where available ..."
email_by_signature = {}
profile_by_email = {}
for email, names in names_by_email.iteritems():
    try:
        # TODO - why does profile differ from client.get_note()
        profile = client.get_profile(email)
        profile_by_email[email] = client.get_note(profile.id)
        email_by_signature[profile.id] = email
    except openreview.OpenReviewException as e:
        profile_by_email[email] = None
        email_by_signature[profile.id] = None


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

# return list of domains associated with the given email
def get_domains(email):
    full_domain = email.split('@')[1]
    domain_components = full_domain.split('.')
    domains = ['.'.join(domain_components[index:len(domain_components)]) for index, path in enumerate(domain_components)]
    valid_domains = [d for d in domains if '.' in d]
    return valid_domains

# fill in conflicts_by_email using profile email domains, history data, and relations
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

        # if domains or relations of paper authors and reviewers overlap, write conflict line
        if domain_conflict or relation_conflict:
            writer.writerow([email,'Paper{0}'.format(papernumber)])

f.close()


