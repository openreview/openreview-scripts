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
