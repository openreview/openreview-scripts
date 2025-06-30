import requests
import os
import openreview
import argparse
import csv

parser = argparse.ArgumentParser()
parser.add_argument('paper_number')
parser.add_argument('--baseurl', help="base URL")
parser.add_argument('--username')
parser.add_argument('--password')
args = parser.parse_args()

paper_number = args.paper_number

client = openreview.Client(baseurl=args.baseurl, username=args.username, password=args.password)
print 'connecting to {0}'.format(client.baseurl)

paper = client.get_notes(invitation='auai.org/UAI/2018/-/Blind_Submission',number=paper_number)[0]
metadata = client.get_notes(invitation='auai.org/UAI/2018/-/Paper_Metadata', forum=paper.id)[0]

reviewer_entries = metadata.content['groups']['auai.org/UAI/2018/Program_Committee']

with open('./{}.csv'.format(openreview.tools.get_paperhash(str(paper_number), paper.content['title'])), 'w') as f:
    writer = csv.writer(f, delimiter='\t')
    writer.writerow([paper.content['title']])
    writer.writerow(['Paper {}'.format(paper.number)])
    writer.writerow(['https://openreview.net/forum?id={}'.format(paper.id)])
    writer.writerow([])

    writer.writerow(['Assigned Reviewers'])
    writer.writerow(['{:25s}'.format('User ID'), "TPMS Score", "Bid Score", ])
    writer.writerow(['Insert assigned reviewers here when available.'])
    writer.writerow([])

    writer.writerow(['All Reviewers'])
    writer.writerow(['{:25s}'.format('User ID'), "TPMS Score", "Bid Score", ])
    reviewer_entries = sorted(reviewer_entries, key=lambda x: x['scores'].get('tpms_score', 0), reverse=True)
    for entry in reviewer_entries:
        print entry['userId']
        user_id = '{:30s}'.format(entry['userId'].encode('utf-8'))
        tpms_score = '{:4f}'.format(entry['scores'].get('tpms_score', 0.0))
        bid_score = '{:4f}'.format(entry['scores'].get('bid_score', 0.0))
        writer.writerow([user_id, tpms_score, bid_score])
