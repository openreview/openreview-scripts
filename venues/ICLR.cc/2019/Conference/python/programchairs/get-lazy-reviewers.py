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
    current_reviewers = tools.iterget_groups(client, regex = paper_inv+'/Reviewers$')
    submissions = tools.iterget_notes(client, invitation = CONF + '/-/Blind_Submission')

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
# Format: reviewers_by_paper[paper_number][reviewer_tilde_id] = review note id
reviewers_by_paper = get_data(invitation)

# Format: late_reviewers[paper_number][reviewer_tilde_id] = reviewer_email
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
area_chairs_group = tools.iterget_groups(client, regex='ICLR.cc/2019/Conference/Paper[0-9]+/Area_Chairs$')
# area_chairs[paper_num] = area chair id
area_chairs = {}
for ac in area_chairs_group:
    paper_number = int(ac.id.split('Paper')[1].split('/Area_Chair')[0])
    if ac.members:
        area_chairs[paper_number] = ac.members[0]

def get_profile_email_map(cl, profile_id_list):
    profiles = cl.get_profiles(profile_id_list)
    map_profile_email = {}
    for prof in profiles:
        if prof :
            if (prof.content.get('preferredEmail', None) != None):
                map_profile_email[prof.id] = prof.content.get('preferredEmail')
            elif (prof.content.get('emailsConfirmed', None) != None):
                map_profile_email[prof.id] = prof.content.get('emailsConfirmed')[0]
            else:
                map_profile_email[prof.id] = prof.content.get('emails')[0]
        else : 
            map_profile_email[prof.id] = "No email found"
    return map_profile_email

# collect all emails
map_profile_email = {}
all_profiles = []
for paper_number in late_reviewers:
    all_profiles.append( str(area_chairs.get(paper_number, '')) )
    all_profiles.extend( [rev for rev in late_reviewers[paper_number]] )

map_profile_email = get_profile_email_map(client, all_profiles)

print ("All late reviewers by paper")
print ("Paper Number, AC, AC Email, Late Reviewers, Reviewer Emails")
for paper_number in sorted(late_reviewers):
    ac = area_chairs.get(paper_number, '')
    reviewer_emails = []
    for rev in late_reviewers[paper_number]:
        reviewer_emails.append( map_profile_email[rev] )

    print ("{0}, {1}, {2}, {3}, {4}".format(
        paper_number, 
        str(ac),
        map_profile_email[str(ac)],
        '(' + ', '.join(late_reviewers[paper_number]) + ')',
        '(' + str (', '.join(reviewer_emails)) + ')'
        )
    )
