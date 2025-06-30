import requests
import os
import openreview
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--baseurl', help="base URL")
parser.add_argument('--username')
parser.add_argument('--password')
args = parser.parse_args()

client = openreview.Client(baseurl=args.baseurl, username=args.username, password=args.password)
print ('connecting to {0}'.format(client.baseurl))

submission_invitation = 'auai.org/UAI/2019/Conference/-/Blind_Submission'
submissions = openreview.tools.iterget_notes(client, invitation=submission_invitation)

if not os.path.exists('uai2019-pdfs'):
    os.makedirs('uai2019-pdfs')

for submission in submissions:
    pdf_url = '{0}{1}'.format(client.baseurl, submission.content['pdf'])
    paper_id = submission.number
    print ('retrieving Paper{0} at {1}'.format(paper_id, pdf_url))
    with open('uai2019-pdfs/Paper{0}.pdf'.format(paper_id), 'wb') as f:
        f.write(client.get_pdf(submission.id))
