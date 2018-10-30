#!/usr/bin/python

"""
Lists all reviewers that have not submitted official reviews.

"""

## Import statements
import argparse
from openreview import *
import openreview.tools as tools


## Handle the arguments
parser = argparse.ArgumentParser()
parser.add_argument('--baseurl', help="base URL")
parser.add_argument('--username')
parser.add_argument('--password')

args = parser.parse_args()

## Initialize the client library with username and password
client = Client(baseurl=args.baseurl, username=args.username, password=args.password)


# create dictionary for reviewers_by_paper[paper_number][reviewer_tilde_id] = review note id
def get_data(invitation):

    CONF = 'ICLR.cc/2019/Conference'
    paper_inv = CONF + '/Paper.*'
    anon_reviewers = tools.iterget_groups(client, regex = paper_inv+'/AnonReviewer.*')
    current_reviewers = tools.iterget_groups(client, regex = paper_inv+'/Reviewers')
    submissions = client.get_notes(invitation = CONF + '/-/Blind_Submission')

    notes = tools.iterget_notes(client, invitation= CONF + '/-/Paper.*/' + invitation)

    papers = {}
    reviews = {}
    reviewers = {}
    reviewers_by_paper = {}

    for paper in submissions:
        papers[paper.number] = paper.id

    # reviews[reviewer name] = review note id
    for n in notes:
        signature = n.signatures[0]
        reviews[signature] = n.id

    # reviewers[paper_num+reviewer_name] = anonymous reviewer name
    for r in anon_reviewers:
        reviewer_id = r.id
        paper_number = reviewer_id.split('Paper')[1].split('/AnonReviewer')[0]
        members = r.members
        if members:
            reviewers[paper_number+ '_' + members[0]] = reviewer_id
        # otherwise the reviewer was removed

    # reviewers_by_paper[paper_number][reviewer name]=review id
    for r in current_reviewers:
        reviewer_id = r.id
        members = r.members
        if members:
            paper_number = int(reviewer_id.split('Paper')[1].split('/Reviewers')[0])
            # check if paper is current
            if paper_number in papers:
                if paper_number not in reviewers_by_paper:
                    reviewers_by_paper[paper_number] = {}
                for m in members:
                    reviewer_id = reviewers.get(str(paper_number) + '_' + m, m)
                    reviewers_by_paper[paper_number][m] = reviews.get(reviewer_id, None)

    return reviewers_by_paper


## Main ##
invitation = 'Official_Review'
# reviewers_by_paper[paper_number][reviewer_tilde_id] = review note id
reviewers_by_paper = get_data(invitation)

# late_reviewers[paper_number][reviewer_tilde_id] = reviewer_email
late_reviewers = {}
print ("Collecting users that did not submit their {}".format(invitation))

total_complete = 0
total_missing = 0
reviewer_set = set()
complete_per_paper ={}
num_required_reviewers = 3
for paper_number in reviewers_by_paper:

    reviewers = reviewers_by_paper[paper_number]
    complete_per_paper[paper_number] = 0
    for reviewer, note_id in reviewers.items():

        if note_id:
            total_complete += 1
            complete_per_paper[paper_number] += 1
        else:
            total_missing += 1
            if paper_number not in late_reviewers:
                late_reviewers[paper_number] = []
            late_reviewers[paper_number].append(reviewer)
            reviewer_set.add(reviewer)


# associate area chairs with paper number
area_chairs_group = client.get_groups(id='ICLR.cc/2019/Conference/Paper.*/Area_Chair')
# area_chairs[paper_num] = area chair id
area_chairs = {}
for ac in area_chairs_group:
    paper_number = int(ac.id.split('Paper')[1].split('/Area_Chair')[0])
    if ac.members:
        area_chairs[paper_number] = ac.members[0]

##print results

print ("All late reviewers by paper")
print ("Paper Number, AC, Reviewers")
for paper_number in sorted(late_reviewers):
    print ("{0}, {1}, {2}".format(paper_number, area_chairs.get(paper_number, ''),','.join(late_reviewers[paper_number])))

print ("")
print ("All late reviewers {0}".format(len(reviewer_set)))
print (','.join(reviewer_set))
print ("")
print ("%s: %s missing" % (invitation,total_missing))
print ("%s: %s complete" % (invitation,total_complete))
print ("")
print ("Papers with less than three reviews")
print ("Paper Number, AC, Late Reviewers")
late_required_reviews = 0
for paper_number in sorted(complete_per_paper):
    if complete_per_paper[paper_number] < num_required_reviewers:
        print ("{0}, {1}, {2}".format(paper_number, area_chairs.get(paper_number, ''),','.join(late_reviewers[paper_number])))
        late_required_reviews += 1
print ("")
print ("%s: %s papers missing reviews" % (invitation, late_required_reviews))


