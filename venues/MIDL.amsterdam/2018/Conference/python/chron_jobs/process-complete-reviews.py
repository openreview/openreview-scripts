#!/usr/bin/python

###############################################################################
# Send email to authors when all of their reviews are in.
###############################################################################

## Import statements
from openreview import *


CONFERENCE_ID = 'MIDL.amsterdam/2018/Conference'
SUBMISSION = CONFERENCE_ID + '/-/Submission'
SHORT_PHRASE = "MIDL 2018 Conference"

## Initialize the client library with username and password
client = Client()
print "connected to "+client.baseurl

reviewer_by_anon = {}
anon_groups = client.get_groups(id=CONFERENCE_ID+'/-/Paper.*/AnonReviewer.*')
for anon_group in anon_groups:
    if len(anon_group.members) > 0:
        reviewer_by_anon[anon_group.id] = anon_group.members[0]

# review_info[paper_num][reviewer_id] = review
reviews = client.get_notes(invitation=CONFERENCE_ID+'/-/Paper.*/Official/Review')
review_info = {}
for review in reviews:
    paper_number = int(review.invitation.split('Paper')[-1].split('/')[0])
    if paper_number not in review_info:
        review_info[paper_number]={}
    review_info[paper_number][reviewer_by_anon[review.signatures[0]]] = review

notes = client.get_notes(invitation=SUBMISSION)
## for all papers w/ completed reviews, inform author (once) and add author to read list
for paper in notes:
    author_group_name = CONFERENCE_ID+'/Paper'+str(paper.number)+'/Authors'
    # if any reviews for this paper
    if paper.number in review_info.keys():
        # grab any of the reviews for this paper
        review_note = review_info[paper.number][review_info[paper.number].keys()[0]]
        if author_group_name not in review_note.readers:
            # not already added for finished reviews, so check now if reviews finished
            reviewers = client.get_group(id = CONFERENCE_ID+'/Paper'+str(paper.number)+'/Reviewers')
            missing_review = False
            for reviewer in reviewers.members:
                if reviewer not in review_info[paper.number].keys():
                    missing_review = True
                    break

            if not missing_review:
                print "Completed Reviews!"
                invite = client.get_invitation(id=CONFERENCE_ID + '/-/Paper'+str(paper.number)+'/Official/Review')
                invite.reply['readers']['values'].append(author_group_name)
                client.post_invitation(invite)
                # newly finished reviews
                for review in review_info[paper.number].values():
                    review.readers.append(author_group_name)
                    client.post_note(review)
                    print "update "+review.invitation+" "+review.signatures[0]
                # send email
                author_msg = 'Your submission to ' + SHORT_PHRASE + ' has been reviewed.\n\nTitle: ' + paper.content['title'] + '\n\nTo view your submission, click here: ' + client.baseurl + '/forum?id=' + paper.forum

                print "send email to "+author_group_name
                response = client.send_mail("Your {0} submission received reviews".format(SHORT_PHRASE), [author_group_name], author_msg)