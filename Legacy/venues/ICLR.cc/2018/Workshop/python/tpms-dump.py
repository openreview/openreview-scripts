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


# user conflicts
names_by_email = {}
with open(args.csv) as f:
    for email, first, last in csv.reader(f):
        names_by_email[email] = (first, last)

conflicts_by_email = {}
for email in names_by_email:
    conflicts_by_email[email] = {'domains': set(), 'relations': set()}

    domain_conflicts, relation_conflicts = openreview.tools.get_profile_conflicts(client, email)

    conflicts_by_email[email]['domains'].update(domain_conflicts)
    conflicts_by_email[email]['relations'].update(relation_conflicts)

# paper conflicts
submissions = client.get_notes(invitation=config.SUBMISSION)
conflicts_by_paper = {}
for n in submissions:
    conflicts_by_paper[n.number] = {'domains': set(), 'relations': set()}
    domain_conflicts, relation_conflicts = openreview.tools.get_paper_conflicts(client, n)

    conflicts_by_paper[n.number]['domains'].update(domain_conflicts)
    conflicts_by_paper[n.number]['relations'].update(relation_conflicts)

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


