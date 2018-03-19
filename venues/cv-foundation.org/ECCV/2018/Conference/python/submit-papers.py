import openreview
import argparse
import csv
import os

parser = argparse.ArgumentParser()
parser.add_argument('--baseurl', help="base URL")
parser.add_argument('--username')
parser.add_argument('--password')
args = parser.parse_args()
client = openreview.Client(baseurl=args.baseurl, username=args.username, password=args.password)

def create_cv_note(title, abstract, authors, authorids, subject_areas, paper_id):
    return openreview.Note(**{
            'readers': ['cv-foundation.org/ECCV/2018/Conference/Program_Chairs'],
            'writers': [],
            'signatures': ['~Super_User1'],
            'nonreaders': [],
            'invitation': 'cv-foundation.org/ECCV/2018/Conference/-/Submission',
            'content': {
                'title': title.replace('\n', ''),
                'abstract': abstract,
                'authors': authors,
                'authorids': authorids,
                'subject areas': subject_areas,
                'paperId': paper_id
            }

        })

with open(os.path.join(os.path.dirname(__file__),'../data/papers.csv')) as f:
    reader = csv.reader(f)
    for line in reader:
        number = line[0]
        title = line[3]
        abstract = line[4]
        authors = [a.split(',')[0].strip().replace('*','') for a in line[5].split(';')]
        authorids = [l.strip() for l in line[6].split(';')]
        subject_areas = [l.strip().replace('*','') for l in line[8].split(';')]

        # Filter withdrawn and invalid papers
        if number not in ['497', '592', '2388', '3200']:
            note = create_cv_note(title, abstract, authors, authorids, subject_areas, number)
            posted_n = client.post_note(note)
            print posted_n.content['title']
        else:
            print 'Ignore paper', number
