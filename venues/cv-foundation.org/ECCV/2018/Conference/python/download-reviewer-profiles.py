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
cmt_conflicts = defaultdict(list)
with open('../data/reviewer-conflicts.csv') as f:
    reader = csv.reader(f)
    reader.next()
    for line in reader:
        email = line[2].strip().lower()
        paperid = line[3].strip().lower()
        if paperid in forum_by_paperId:
            conflicted_forum = forum_by_paperId[paperid]
            if not email in profiles_by_email:
                print "getting profile: ", email
                new_profiles = client.get_profiles([email])
                if not new_profiles:
                    profiles_by_email.update({email: None})
                else:
                    profiles_by_email.update(new_profiles)

            if email in profiles_by_email and profiles_by_email[email]:
                userid = profiles_by_email[email].id
            else:
                print "no profile found while updating CMT conflicts: ", email
            if userid:
                cmt_conflicts[conflicted_forum].append(userid)
        else:
            print "couldn't find paper with id ", paperid

with open('../data/cmt_conflicts.pkl', 'wb') as f:
    pickle.dump(cmt_conflicts, f)
