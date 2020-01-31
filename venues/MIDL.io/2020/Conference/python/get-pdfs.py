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

submission_invitation = 'MIDL.io/2020/Conference/-/Blind_Submission'
submissions = openreview.tools.iterget_notes(client, invitation=submission_invitation, details='original')

if not os.path.exists('midl2020-pdfs'):
    os.makedirs('midl2020-pdfs')

for submission in submissions:
    if 'pdf' in submission.details['original']['content']:
        pdf_url = '{0}{1}'.format(client.baseurl, submission.details['original']['content']['pdf'])
        paper_id = submission.number
        print ('retrieving Paper{0} at {1}'.format(paper_id, pdf_url))
        with open('midl2020-pdfs/Paper{0}.pdf'.format(paper_id), 'wb') as f:
            f.write(client.get_pdf(submission.details['original']['id']))
    else:
        print('Paper number {0} has no pdf'.format(submission.number))