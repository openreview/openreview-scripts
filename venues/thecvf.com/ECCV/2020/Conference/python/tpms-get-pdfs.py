from __future__ import print_function
import requests
import openreview
import argparse


'''
Modify the out_dir variable
'''
out_dir = '../data/eccv2020_pdfs'

submission_invitation = 'thecvf.com/ECCV/2020/Conference/-/Submission'

parser = argparse.ArgumentParser()
parser.add_argument('--baseurl', help="base url")
parser.add_argument('--username')
parser.add_argument('--password')
args = parser.parse_args()

client = openreview.Client(baseurl=args.baseurl, username=args.username, password=args.password)

submissions = openreview.tools.iterget_notes(client, invitation = submission_invitation)

for note in submissions:
	pdf_name = note.content.get('pdf')
	if pdf_name:
		pdf_url = 'https://openreview.net{0}'.format(pdf_name)
		paper_number = note.number
		print("retrieving paper{0} at {1}".format(paper_number, pdf_url))
		pdf_response = client.get_pdf(note.id)
		with open('{}/paper{}.pdf'.format(out_dir, paper_number), 'wb') as f:
			f.write(pdf_response)
