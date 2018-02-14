import requests
import os

submissions_response = requests.get('https://openreview.net/notes?invitation=ICLR.cc/2018/Workshop/-/Submission', params={})

if not os.path.exists('./pdfs'):
    os.makedirs('./pdfs')

for n in submissions_response.json()['notes']:
    pdf_url = 'https://openreview.net{0}'.format(n['content']['pdf'])
    paper_id = n['number']
    print "retrieving Paper{0} at {1}".format(paper_id, pdf_url)
    pdf_response = requests.get(pdf_url, stream=True)

    with open('./pdfs/Paper{0}.pdf'.format(paper_id), 'wb') as f:
        f.write(pdf_response.content)

