from __future__ import print_function
import requests
import openreview
import argparse
import os

parser = argparse.ArgumentParser()
parser.add_argument('--baseurl', help="base url")
parser.add_argument('--username')
parser.add_argument('--password')
args = parser.parse_args()

client = openreview.Client(baseurl=args.baseurl, username=args.username, password=args.password)
print ('connecting to {0}'.format(client.baseurl))

submission_invitation = 'thecvf.com/ECCV/2020/Conference/-/Submission'

submissions = openreview.tools.iterget_notes(client, invitation=submission_invitation)

if not os.path.exists('eccv2020_pdfs'):
	os.makedirs('eccv2020_pdfs')

for submission in submissions:
	if 'pdf' in submission.content:
		pdf_url = '{0}{1}'.format(client.baseurl, submission.content['pdf'])
		paper_id = submission.number
		print ('retrieving Paper{0} at {1}'.format(paper_id, pdf_url))
		with open('eccv2020_pdfs/Paper{0}.pdf'.format(paper_id), 'wb') as f:
			f.write(client.get_pdf(submission.id))
	else:
		print('Paper number {0} has no pdf'.format(submission.number))
