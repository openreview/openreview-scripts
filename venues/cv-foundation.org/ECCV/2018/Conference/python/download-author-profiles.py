import openreview
import random
import argparse
import requests
from collections import defaultdict
import csv
import os
import pickle

parser = argparse.ArgumentParser()
parser.add_argument('--baseurl', help="base URL")
parser.add_argument('--username')
parser.add_argument('--password')

args = parser.parse_args()

client = openreview.Client(baseurl=args.baseurl, username=args.username, password=args.password)
print 'connecting to {0}'.format(client.baseurl)

papers = openreview.tools.get_all_notes(client, 'cv-foundation.org/ECCV/2018/Conference/-/Submission')
profiles_by_email = {}

for paper in papers:
    print paper.number
    authorids = [e.lower() for e in paper.content['authorids']]
    paper_profiles = client.get_profiles(authorids)
    profiles_by_email.update(paper_profiles)

with open('../data/author-profiles.pkl', 'wb') as f:
    pickle.dump(profiles_by_email, f)


