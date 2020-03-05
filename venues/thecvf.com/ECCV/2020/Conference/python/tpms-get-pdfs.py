from __future__ import print_function
import requests
import openreview
import argparse
import os
from tqdm import tqdm
from multiprocessing import Pool

parser = argparse.ArgumentParser()
parser.add_argument('--baseurl', help="base url")
parser.add_argument('--username')
parser.add_argument('--password')
args = parser.parse_args()

client = openreview.Client(baseurl=args.baseurl, username=args.username, password=args.password)
print ('connecting to {0}'.format(client.baseurl))

submission_invitation = 'thecvf.com/ECCV/2020/Conference/-/Submission'

print('Get Submissions')
submissions = openreview.tools.iterget_notes(client, invitation=submission_invitation)

if not os.path.exists('eccv2020_pdfs'):
	os.makedirs('eccv2020_pdfs')

submissions_without_pdf = 0

def get_pdf(submission):
	if 'pdf' in submission.content:
		pdf_url = '{0}{1}'.format(client.baseurl, submission.content['pdf'])
		paper_number = submission.number
		try:
			with open('eccv2020_pdfs/Paper{0}.pdf'.format(paper_number), 'wb') as f:
				f.write(client.get_pdf(submission.id))
		except Exception as e:
			print ('Error during pdf download for paper number {}, error: {}'.format(submission.number, e))
		return 1
	return 0

print('Download files')
with Pool(16) as p:
	r = p.map(get_pdf, submissions)

print('Done')
