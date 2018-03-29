import openreview
import argparse
import os

parser = argparse.ArgumentParser()
parser.add_argument('--baseurl')
parser.add_argument('--username')
parser.add_argument('--password')
args = parser.parse_args()

client = openreview.Client(baseurl=args.baseurl, username=args.username, password=args.password)
print 'connecting to {0}'.format(client.baseurl)

papers = client.get_notes(invitation='auai.org/UAI/2018/-/Blind_Submission')

anonreviewers = client.get_groups('auai.org/UAI/2018/Paper.*/AnonReviewer.*')
anonreviewers_by_number = {n.number: [] for n in papers}
for a in anonreviewers:
    id_components = a.id.split('/')
    _, number = id_components[3].split('Paper')
    anonreviewers_by_number[int(number)].append(a.id)

for paper in papers:
    all_users_group = openreview.Group(**{
        'id': 'auai.org/UAI/2018/Paper{}/All_Users'.format(paper.number),
        'readers': ['auai.org/UAI/2018'],
        'writers': ['auai.org/UAI/2018'],
        'signatures': ['auai.org/UAI/2018'],
        'signatories': [],
        'members': [
            'auai.org/UAI/2018/Paper{}/Authors'.format(paper.number),
            'auai.org/UAI/2018/Paper{}/Reviewers'.format(paper.number),
            'auai.org/UAI/2018/Paper{}/Area_Chairs'.format(paper.number),
            'auai.org/UAI/2018/Program_Chairs',
            'auai.org/UAI/2018'
        ]
    })
    client.post_group(all_users_group)

    reviewers_unsubmitted = openreview.Group(**{
        'id': 'auai.org/UAI/2018/Paper{}/Reviewers/Unsubmitted'.format(paper.number),
        'readers': ['auai.org/UAI/2018'],
        'writers': ['auai.org/UAI/2018'],
        'signatures': ['auai.org/UAI/2018'],
        'signatories': [],
        'members': anonreviewers_by_number[paper.number]
    })
    client.post_group(reviewers_unsubmitted)

    reviewers_submitted = openreview.Group(**{
        'id': 'auai.org/UAI/2018/Paper{}/Reviewers/Submitted'.format(paper.number),
        'readers': ['auai.org/UAI/2018'],
        'writers': ['auai.org/UAI/2018'],
        'signatures': ['auai.org/UAI/2018'],
        'signatories': [],
        'members': []
    })
    client.post_group(reviewers_submitted)

    print paper.id
