#!/usr/bin/python

"""
Sends an email to the members of the group of your choice.

"""

## Import statements
import argparse
import openreview
import requests

## Handle the arguments
parser = argparse.ArgumentParser()
parser.add_argument('-v','--verbose', help="set to true if you want late users listed per-paper")
parser.add_argument('--baseurl', help="base URL")
parser.add_argument('--username')
parser.add_argument('--password')

args = parser.parse_args()

## Initialize the client library with username and password
client = openreview.Client(baseurl=args.baseurl, username=args.username, password=args.password)
print 'connecting to {0}'.format(client.baseurl)
verbose = True if args.verbose.lower()=='true' else False

#################################################
#                                               #
#   EDIT YOUR MESSAGE AND SUBJECT LINE BELOW    #
#                                               #
#################################################


subjectline = "Reviews due by Friday for ICLR 2018 workshop track"

message = """
Hi,

        This is a final reminder that your ICLR workshop paper reviews are due
by the end of Friday, 9 March. Time is tight, so we need them on time.

Tara, Marc’Aurelio, Iain and Oriol -- the ICLR 2018 program committee
"""


#################################################
#                                               #
#               END OF MESSAGE                  #
#                                               #
#################################################

####################################
## get all active reviewers
####################################
invitation = "Official_Review"
headers = {'User-Agent': 'test-create-script', 'Content-Type': 'application/json',
           'Authorization': 'Bearer ' + client.token}
anon_reviewers = requests.get(client.baseurl + '/groups?id=ICLR.cc/2018/Workshop/Paper.*/AnonReviewer.*',
                              headers=headers)
notes = client.get_notes(invitation='ICLR.cc/2018/Workshop/-/Paper.*/' + invitation)

# reviews[paper_num][reviewer_id]= note_id
reviews = {}

# reviewers[anon_id]= reviewer_id   (reviewer_id is email or ~id)
reviewers = {}

# convert AnonReview into ID
for r in anon_reviewers.json()['groups']:
    reviewer_id = r['id']
    members = r['members']
    if members:
        reviewers[reviewer_id] = members[0]
        # else this AnonReviewer deleted

# create reviews structure w/ paper_num reviewer_id
for id in reviewers:
    paper_num = id.split('Paper')[1].split('/')[0]
    if paper_num not in reviews:
        reviews[paper_num] = {}
    reviews[paper_num][reviewers[id]] = None

# fill in existing reviews
for n in notes:
    signature = n.signatures[0]
    paper_num = signature.split('Paper')[1].split('/')[0]
    reviews[paper_num][reviewers[signature]] = n.id


####################################
## get late reviewers
####################################
# collect reviewers missing reviews
late_users = set()
total_complete = 0
total_missing = 0
verbose = False
for paper_number in reviews:
    reviewers = reviews[paper_number]

    for reviewer in reviewers:
        if reviews[paper_number][reviewer]:
            total_complete += 1
        else:
            total_missing += 1
            if verbose:
                print "late users on paper %s: %s" % (paper_number, reviewer)
            late_users.add(reviewer)

####################################
## email late reviewers
####################################
response = client.send_mail(subjectline, list(late_users), message)
print "Emailing the following users:"
print response.json()['groups']

print "%s  missing" % (total_missing)
print "%s complete" % (total_complete)




