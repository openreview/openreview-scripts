from __future__ import print_function
import requests

out_dir = '../data/iclr19_pdfs'

submissions_response = requests.get('https://openreview.net/notes?invitation=ICLR.cc/2019/Conference/-/Blind_Submission', params={})

for n in submissions_response.json()['notes']:
    pdf_url = 'https://openreview.net{0}'.format(n['content']['pdf'])
    paper_id = n['number']
    print("retrieving paper{0} at {1}".format(paper_id, pdf_url))
    pdf_response = requests.get(pdf_url, stream=True)
    with open('{}/paper{}.pdf'.format(out_dir, paper_id), 'wb') as f:
        f.write(pdf_response.content)

