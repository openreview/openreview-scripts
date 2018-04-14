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
papers_by_forum = {}
forum_by_paperId = {}
for p in papers:
    papers_by_forum[p.forum] = p
    forum_by_paperId[p.content['paperId']] = p.forum

profiles_by_email = {}

#Load CMT conflicts
with open('../data/reviewers.csv') as f:
    reader = csv.reader(f)
    reader.next()
    for line in reader:
        # First Name,Middle Initial (optional),Last Name,E-mail,Organization
        first = line[0]
        last = line[2]
        email = line[3].strip().lower()

        if not email in profiles_by_email:
            print "getting profile: ", email
            new_profiles = client.get_profiles([email])
            if not new_profiles:
                profiles_by_email.update({email: None})
            else:
                profile = new_profiles[email]
                new_email_entries = {e: profile for e in profile.content['emails']}
                profiles_by_email.update(new_email_entries)

with open('../data/reviewer-profiles.pkl', 'wb') as f:
    pickle.dump(profiles_by_email, f)
