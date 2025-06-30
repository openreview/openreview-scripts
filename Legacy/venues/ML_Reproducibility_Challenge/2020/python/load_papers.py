import math

import pandas as pd
import openreview
import argparse

data = pd.read_csv("rc2020-papers-emnlp2020.csv")

venueid_map = {'ICLR': 'ICLR.cc/2020/Conference',
               'ICML': 'ICML.cc/2020/Conference',
               'ACL': 'aclweb.org/ACL/2020/Conference',
               'CVPR': 'thecvf.com/CVPR/2020/Conference',
               'ECCV': 'thecvf.com/ECCV/2020/Conference',
               'NeurIPS': 'NeurIPS.cc/2020/Conference',
               'EMNLP': 'EMNLP/2020/Conference'}

venue_map = {'ICLR': 'ICLR 2020',
             'ICML': 'ICML 2020',
             'ACL': 'ACL 2020',
             'CVPR': 'CVPR 2020',
             'ECCV': 'ECCV 2020',
             'NeurIPS': 'NeurIPS 2020',
             'EMNLP':'EMNLP 2020'}

print("uniq", data['Conference'].unique())
filtered_data = data

CONFERENCE_ID = 'ML_Reproducibility_Challenge/2020'
ACCEPTED_PAPER_ID = CONFERENCE_ID + '/-/Accepted_Papers'
PROGRAM_CHAIRS_ID = CONFERENCE_ID + '/Program_Chairs'

parser = argparse.ArgumentParser()
parser.add_argument('--baseurl', help="base url")
parser.add_argument('--username')
parser.add_argument('--password')
args = parser.parse_args()

client = openreview.Client(baseurl=args.baseurl, username=args.username, password=args.password)


def post_paper(paper, client):
    authors = ""
    if paper['Authors']:
        authors = paper['Authors'].split(",") if "," in paper['Authors'] else [paper['Authors']]
        for i in range(len(authors)):
            authors[i] = str(authors[i]).strip()

    note = openreview.Note(invitation=ACCEPTED_PAPER_ID,
                           readers=['everyone'],
                           writers=[CONFERENCE_ID, PROGRAM_CHAIRS_ID],
                           signatures=[PROGRAM_CHAIRS_ID],
                           content={
                               'title': paper['Title'],
                               'authors': authors,
                               'pdf': paper['PDF_url'],
                               'html': paper['PWC_url'],
                               'venueid': venueid_map[paper['Conference']],
                               'venue': venue_map[paper['Conference']]
                           }
                           )
    note = client.post_note(note)
    print(paper['Title'])


for index, paper in filtered_data.iterrows():
    try:
        # print(paper)
        post_paper(paper, client)
    except Exception as e:
        print("Error in paper: " + paper['Title'])
        print(e)

print(filtered_data.iloc[0])
print(filtered_data.size)
