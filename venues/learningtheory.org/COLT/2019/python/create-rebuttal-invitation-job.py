import openreview
import config
import json

client = openreview.Client()

all_reviews = list(openreview.tools.iterget_notes(
    client,
    invitation = 'learningtheory.org/COLT/2019/Conference/-/Paper.*/Official_Review'
))

all_rebuttal_invis = list(openreview.tools.iterget_invitations(
    client,
    regex = 'learningtheory.org/COLT/2019/Conference/-/Paper[0-9]+/Review[0-9]+/Rebuttal'
))

print (len(all_rebuttal_invis))
print (len(all_reviews))

map_paper_reviews = {}
for review in all_reviews:
    paper_number = int(review.invitation.split('Paper')[1].split('/')[0])
    if paper_number not in map_paper_reviews:
        map_paper_reviews[paper_number] = []
    map_paper_reviews[paper_number].append(review)

print ([review for review in map_paper_reviews if len(map_paper_reviews[review]) < 3])

# map_paper_rebuttal_invi = {}
# for rebuttal in all_rebuttal_invis:
#     paper_number = str(review.invitation.split('Paper')[1].split('/')[0])
#     if paper_number not in map_paper_rebuttal_invi:
#         map_paper_rebuttal_invi[paper_number] = []
#     map_paper_rebuttal_invi[paper_number].append(rebuttal.reply['replyto'])

# print (map_paper_rebuttal_invi['2'])

# new_reviews = {}
# map_paper_max_review_number = {}

# # ####### Temporary
# new_reviews = all_reviews
# ######################

# for review in new_reviews:
#     paper_number = str(review.invitation.split('Paper')[1].split('/')[0])

#     next_review_number = str(map_paper_max_review_number.get(paper_number, 0) + 1)

#     # Post author rebuttal invitation
#     rebuttal_invitation = openreview.Invitation(
#         id = 'learningtheory.org/COLT/2019/Conference/-/Paper' + paper_number + '/Review_' + next_review_number + '/Rebuttal',
#         invitees = [
#             'learningtheory.org/COLT/2019/Conference/Paper' + paper_number + '/Authors'
#         ],
#         duedate = 1553742000000,
#         signatures = ['learningtheory.org/COLT/2019/Conference'],
#         readers = [
#             'learningtheory.org/COLT/2019/Conference/Program_Chairs',
#             'learningtheory.org/COLT/2019/Conference/Paper' + paper_number + '/Program_Committee',
#             'learningtheory.org/COLT/2019/Conference/Paper' + paper_number + '/Authors'
#         ],
#         writers = ['learningtheory.org/COLT/2019/Conference'],
#         multiReply = False,
#         reply = {
#             'forum': review.forum,
#             'replyto': review.id,
#             'readers': {'values': [
#                 'learningtheory.org/COLT/2019/Conference/Paper' + paper_number + '/Authors',
#                 'learningtheory.org/COLT/2019/Conference/Paper' + paper_number + '/Program_Committee',
#                 'learningtheory.org/COLT/2019/Conference/Program_Chairs'
#                 ]
#             },
#             'writers': {
#                 'values': ['learningtheory.org/COLT/2019/Conference/Paper' + paper_number + '/Authors']
#             },
#             'signatures': {
#                 'values-regex': 'learningtheory.org/COLT/2019/Conference/Paper' + paper_number + '/Authors'
#             },
#             'content': {
#                 'title': {
#                     'order': 1,
#                     'value-regex': '.{0,500}',
#                     'description': 'Title of the rebuttal.',
#                     'required': True
#                 },
#                 'rebuttal': {
#                     'order': 2,
#                     'value-regex': '[\\S\\s]{1,200000}',
#                     'description': 'Maximum 200000 characters.',
#                     'required': True
#                 }
#             }
#         }
#     )
#     map_paper_max_review_number[paper_number] = int(next_review_number)
#     posted_rebuttal_invitation = client.post_invitation(rebuttal_invitation)
#     print ("Rebuttal invitation posted with id: ", posted_rebuttal_invitation.id )
