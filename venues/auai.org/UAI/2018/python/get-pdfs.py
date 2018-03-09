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
print 'connecting to {0}'.format(client.baseurl)

submission_invitation = 'auai.org/UAI/2018/-/Blind_Submission'
submissions = client.get_notes(invitation=submission_invitation)

if not os.path.exists('../pdfs'):
    os.makedirs('../pdfs')

for n in submissions:
    pdf_url = '{0}{1}'.format(client.baseurl, n.content['pdf'])
    paper_id = n.number
    print "retrieving Paper{0} at {1}".format(paper_id, pdf_url)
    pdf_response = requests.get(pdf_url, stream=True)

    with open('../pdfs/Paper{0}.pdf'.format(paper_id), 'wb') as f:
        f.write(pdf_response.content)

