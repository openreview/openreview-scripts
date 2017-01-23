#!/usr/bin/python

"""
Get the amount of replies per paper for reviewers/areachairs. It doesn't count the reviews/meta-reviews

"""

## Import statements
import argparse
import csv
import sys
import openreview
import requests

## Handle the arguments
parser = argparse.ArgumentParser()
parser.add_argument('-t', '--type', help="reviewer or areachair, by default reviewer")
parser.add_argument('--baseurl', help="base URL")
parser.add_argument('--username')
parser.add_argument('--password')

args = parser.parse_args()

## Initialize the client library with username and password
if args.username!=None and args.password!=None:
    client = openreview.Client(baseurl=args.baseurl, username=args.username, password=args.password)
else:
    client = openreview.Client(baseurl=args.baseurl)


replies_by_author = {}
submissions = {}

iclrsubs = client.get_notes(invitation='ICLR.cc/2017/conference/-/submission')
for s in iclrsubs:
    submissions[s.id] = s

headers = {'User-Agent': 'test-create-script', 'Content-Type': 'application/json', 'Authorization': 'Bearer ' + client.token}

def get_replies_by_author(paper_number, author):

    if author not in replies_by_author:
        replies_by_author[author] = {}

    replies = replies_by_author[author]

    if paper_number in replies:
        return replies[paper_number]
    else:
        notes = client.get_notes(tauthor = author)
        for n in notes:
            submission = submissions.get(n.forum, None)
            invitation = str(n.invitation)
            if submission and not invitation.endswith('official/review') and not invitation.endswith('meta/review'):
                if submission.number not in replies_by_author[author]:
                    replies_by_author[author][submission.number] = set()
                replies_by_author[author][submission.number].add(n.id)
        return replies_by_author[author].get(paper_number, [])


def get_stats(anonGroup, currentGroup):

    anon_reviewers = requests.get(client.baseurl+'/groups?id=ICLR.cc/2017/conference/paper.*/' + anonGroup + '.*', headers = headers)
    current_reviewers = requests.get(client.baseurl+'/groups?id=ICLR.cc/2017/conference/paper.*/' + currentGroup, headers = headers)

    reviewers = {}
    reviewers_by_paper = {}

    for r in anon_reviewers.json():
        reviewer_id = r['id']
        members = r['members']
        if members:
            reviewers[reviewer_id] = members[0]

    for r in current_reviewers.json():
        reviewer_id = r['id']
        members = r['members']
        if members:
            paper_number = int(reviewer_id.split('paper')[1].split('/' + currentGroup)[0])
            if paper_number not in reviewers_by_paper:
                reviewers_by_paper[paper_number] = {}

            for m in members:
                reviewer_name = reviewers.get(m, m)
                reviewers_by_paper[paper_number][reviewer_name] = get_replies_by_author(paper_number, reviewer_name)

    return reviewers_by_paper

anonGroup = 'AnonReviewer'
currentGroup = 'reviewers'

if args.type != None and args.type == 'areachair':
    anonGroup = 'areachair'
    currentGroup = 'areachairs'

data = get_stats(anonGroup, currentGroup)

for paper_number, author_data in data.iteritems():

    for author, replies in author_data.iteritems():

        print str(paper_number) + ', ' + author.encode('utf-8') + ', ' + str(len(replies))






