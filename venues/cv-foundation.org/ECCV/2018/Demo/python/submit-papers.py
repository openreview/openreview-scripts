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

print 'connecting to', client.baseurl

def create_cv_note(title, abstract, authors, authorids, keywords):
    return openreview.Note(**{
            'readers': ['everyone'],
            'writers': [],
            'signatures': ['~Super_User1'],
            'nonreaders': [],
            'invitation': 'cv-foundation.org/ECCV/2018/Demo/-/Submission',
            'content': {
                'title': title.replace('\n', ''),
                'abstract': abstract,
                'authors': authors,
                'authorids': authorids,
                'keywords': keywords
            }

        })

posted_notes = 0

with open(os.path.join(os.path.dirname(__file__),'../data/papers.csv')) as f:
    reader = csv.reader(f)
    reader.next()
    for line in reader:
        number = line[0]
        title = line[1]
        abstract = line[2]
        authors = [a.split(',')[0].strip().replace('*','') for a in line[3].split(';')]
        authorids = [l.strip() for l in line[4].split(';')]
        keywords = [l.strip().replace('*','') for l in line[5].split(';')]

        posted_n = client.post_note(create_cv_note(title, abstract, authors, authorids, keywords))
        print posted_n.content['title']
        posted_notes += 1
        if posted_notes > 500:
            break
