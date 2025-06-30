from __future__ import print_function
import requests
import openreview
import argparse
import datetime
import os
from tqdm import tqdm
import concurrent.futures

parser = argparse.ArgumentParser()
parser.add_argument('--baseurl', help="base url")
parser.add_argument('--username')
parser.add_argument('--password')
args = parser.parse_args()

client = openreview.Client(baseurl=args.baseurl, username=args.username, password=args.password)
print ('connecting to {0}'.format(client.baseurl))
start = datetime.datetime.utcnow()

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
		return pdf_url
	return None

print('Download files')
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
    # Start the load operations and mark each future with its URL
    future_to_url = {executor.submit(get_pdf, submission): submission for submission in submissions}
    for future in concurrent.futures.as_completed(future_to_url):
        url = future_to_url[future]
        try:
            data = future.result()
        except Exception as exc:
            print('%r generated an exception: %s' % (url, exc))

end = datetime.datetime.utcnow()

print('Done', (end - start).total_seconds(), 'seconds')
