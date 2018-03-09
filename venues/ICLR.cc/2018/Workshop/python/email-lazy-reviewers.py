#!/usr/bin/python

"""
Sends an email to the members of the group of your choice.

"""

## Import statements
import argparse
import openreview

## Handle the arguments
parser = argparse.ArgumentParser()
parser.add_argument('--baseurl', help="base URL")
parser.add_argument('--username')
parser.add_argument('--password')

args = parser.parse_args()

## Initialize the client library with username and password
client = openreview.Client(baseurl=args.baseurl, username=args.username, password=args.password)
print 'connecting to {0}'.format(client.baseurl)


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

(To those who have done their reviews: Thank you! Please ignore this email.)

Reminder: log into OpenReview using the same email address as used in
this email, and go to the "Tasks" tab at:
https://openreview.net/group?id=ICLR.cc/2018/Workshop

As usual, if you have any problems, please let us know immediately:
iclr2018.programchairs@gmail.com

Thanks,
Tara, Oriol, Iain and Marc'Aurelio - ICLR 2018 program chairs

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
anon_reviewers = client.get_groups(id='ICLR.cc/2018/Workshop/Paper.*/AnonReviewer.*')
notes = client.get_notes(invitation='ICLR.cc/2018/Workshop/-/Paper.*/' + invitation)

# reviews[paper_num][reviewer_id]= note_id
reviews = {}

# reviewers[anon_id]= reviewer_id   (reviewer_id is email or ~id)
reviewers = {}

# convert AnonReview into ID
for r in anon_reviewers:
    reviewer_id = r.id
    members = r.members
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
print response['groups']

print "{} reviews missing".format(total_missing)
print "{} reviews complete".format(total_complete)
print "{} users emailed".format(len(response['groups']))



