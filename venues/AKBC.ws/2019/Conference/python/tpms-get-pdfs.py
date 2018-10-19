from __future__ import print_function
import requests


'''
Modify the out_dir variable
'''
out_dir = '../data/iclr19_pdfs'

invitation_id = 'ICLR.cc/2019/Conference/-/Blind_Submission'

limit = 1000
offset = 0
done = False

while not done:
	submissions_response = requests.get(
		'https://openreview.net/notes?invitation={}'.format(invitation_id),
		params={'limit': limit, 'offset': offset})
	submissions = submissions_response.json()['notes']

	if len(submissions) < limit:
		done = True
	else:
		offset += limit

	for n in submissions:
	    pdf_url = 'https://openreview.net{0}'.format(n['content']['pdf'])
	    paper_id = n['number']
	    print("retrieving paper{0} at {1}".format(paper_id, pdf_url))
	    pdf_response = requests.get(pdf_url, stream=True)
	    with open('{}/paper{}.pdf'.format(out_dir, paper_id), 'wb') as f:
	        f.write(pdf_response.content)

