#!/usr/bin/python

"""
Output review information for all papers to a csv file.
Paper Num, Title, Area Chair, reviews complete/total, Reviewer1, rating, confidence, Reviewer2...

"""

## Import statements
import argparse
from openreview import *
import csv
import sys
sys.path.insert(0, "./..")
import config

## Handle the arguments
parser = argparse.ArgumentParser()
parser.add_argument('--baseurl', help="base URL")
parser.add_argument('--username')
parser.add_argument('--password')
parser.add_argument('-f', '--file',help="specify an output file otherwise defaults to info.csv")
parser.add_argument('--ac',help="specify area chair")
args = parser.parse_args()
if args.file == None:
    args.file = 'info.csv'

## Initialize the client library with username and password
client = Client(baseurl=args.baseurl, username=args.username, password=args.password)

reviews_total =0
reviews_complete = 0
# paper_data structure
#   paper_data[paper_num]['title'] = title
#   paper_data[paper_num]['reviewers'][reviewer]['rating'/'confidence'] = rating
#   paper_data[paper_num]['AC']= Area Chair id
#   paper_data[paper_num]['meta_recommendation']= meta review recommendation
#   paper_data[paper_num]['meta_confidence']= meta review confidence
#   paper_data[paper_num]['reviewer_count']= # of assigned reviewers
#   paper_data[paper_num]['review_count']= # of reviews complete
paper_data = {}

# fill in submission information
print "Filling in submissions"
submissions = client.get_notes(invitation=config.BLIND_SUBMISSION)
for note in submissions:
    paper_data[note.number] = {}
    paper_data[note.number]['title']= note.content['title']
    paper_data[note.number]['reviewers'] = {}
    paper_data[note.number]['AC'] = ""
    paper_data[note.number]['reviewer_count'] = 0
    paper_data[note.number]['review_count'] = 0
    paper_data[note.number]['meta_recommendation'] = ""
    paper_data[note.number]['meta_confidence'] = ""
# fill in area chairs per paper
print "Filling in Area Chairs"
area_chairs = client.get_groups(config.CONF+'/Paper.*/Area_Chair')
for ac in area_chairs:
    paper_number = int(ac.id.split('Paper')[1].split('/Area_Chair')[0])
    if paper_number in paper_data and ac.members:
        paper_data[paper_number]['AC'] = ac.members[0]


# fill in reviewers per paper
print "Filling in reviewers"
reviewers = client.get_groups(config.CONF+'/Paper.*/Reviewers')
for paper_reviewers in reviewers:
    paper_number = int(paper_reviewers.id.split('Paper')[1].split('/Reviewers')[0])
    if paper_number in paper_data:
        for reviewer in paper_reviewers.members:
            paper_data[paper_number]['reviewers'][reviewer] = {}
            paper_data[paper_number]['reviewers'][reviewer]['rating'] = -1
            paper_data[paper_number]['reviewers'][reviewer]['confidence'] = -1
            paper_data[paper_number]['reviewer_count'] += 1
            reviews_total += 1


# translate anon reviewers into ids
print "Filling in anonymous reviewers"
anon_reviewers = client.get_groups(id = config.CONF+'/Paper.*/AnonReviewer.*')
# reviewers[anon_name]=id
reviewers = {}
for anon in anon_reviewers:
    if anon.members:
        reviewers[anon.id]=anon.members[0]

# fill in reviews per review/paper
print "Filling in reviews"
# can download max of 1k notes at a time
reviews = []
limit = 1000
offset = 0
notes_call_finished = False
while not notes_call_finished:
    notes_batch = client.get_notes(invitation='ICLR.cc/2018/Conference/-/Paper.*/Official_Review', offset=offset, limit=limit)
    reviews += notes_batch
    offset += limit
    if len(notes_batch) < limit:
        notes_call_finished = True

for review in reviews:
    paper_number = int(review.invitation.split('Paper')[1].split('/Official_Review')[0])
    # check for review.signatures in reviewers for odd case where there was a review submitted before the reviewer was removed.
    if paper_number in paper_data and review.signatures[0] in reviewers:
        reviewer = reviewers[review.signatures[0]]
        if reviewer in paper_data[paper_number]['reviewers']:
            paper_data[paper_number]['reviewers'][reviewer]['rating'] = review.content['rating'].split(':')[0]
            paper_data[paper_number]['reviewers'][reviewer]['confidence'] = review.content['confidence'].split(':')[0]
            paper_data[paper_number]['review_count'] += 1
            reviews_complete += 1
        else:
            print "Error missing reviewer? "+reviewer

# fill in meta reviews per paper
print "Filling in meta reviews"
meta_reviews = client.get_notes(invitation= config.CONF + '/-/Paper.*/Meta_Review')
for meta_review in meta_reviews:
    paper_number = int(meta_review.invitation.split('Paper')[1].split('/Meta_Review')[0])
    # check for review.writers in reviewers for odd case where there was a review submitted before the reviewer was removed.
    if paper_number in paper_data:
        paper_data[paper_number]['meta_recommendation'] = meta_review.content['recommendation']
        paper_data[paper_number]['meta_confidence'] = meta_review.content['confidence'].split(':')[0]


# print to file reviewer, number of papers assigned and list of paper numbers
with open(args.file, 'wb') as outfile:

    csvwriter = csv.writer(outfile, delimiter=',')
    # write header row
    row = ['Paper Num', 'Title', 'Area Chair', 'reviews complete','total reviews', 'meta review recommendation', 'meta review confidence','Reviewer1', 'rating', 'confidence', 'Reviewer2', 'rating', 'confidence', 'Reviewer3', 'rating', 'confidence']
    csvwriter.writerow(row)

    for number in paper_data:
        if args.ac == None or args.ac == paper_data[number]['AC']:
            row = []
            row.append(number)
            row.append(paper_data[number]['title'].encode('UTF-8'))
            row.append(paper_data[number]['AC'].encode('UTF-8'))
            row.append(paper_data[number]['review_count'])
            row.append(paper_data[number]['reviewer_count'])
            row.append(paper_data[number]['meta_recommendation'])
            row.append(paper_data[number]['meta_confidence'])
            for reviewer in paper_data[number]['reviewers']:
                row.append(reviewer.encode('UTF-8'))
                if paper_data[number]['reviewers'][reviewer]['rating'] >=0:
                    row.append(paper_data[number]['reviewers'][reviewer]['rating'])
                    row.append(paper_data[number]['reviewers'][reviewer]['confidence'])
                else:
                    row.append('')
                    row.append('')
            csvwriter.writerow(row)


print "reviews completed: {0}, requested: {1}".format(reviews_complete, reviews_total)
