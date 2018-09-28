from __future__ import print_function
import requests
import openreview


'''
Modify the out_dir variable
'''
out_dir = '../data/iclr19_pdfs'

client = openreview.Client(baseurl='https://openreview.net')
invitation_id = 'ICLR.cc/2019/Conference/-/Blind_Submission'

submissions = openreview.tools.iterget_notes(client, invitation=invitation_id)

for n in submissions:
    pdf_url = 'https://openreview.net{0}'.format(n.content['pdf'])
    paper_id = n.number
    print("retrieving paper{0} at {1}".format(paper_id, pdf_url))
    pdf_response = requests.get(pdf_url, stream=True)
    with open('{}/paper{}.pdf'.format(out_dir, paper_id), 'wb') as f:
        f.write(pdf_response.content)

