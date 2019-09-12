import argparse
import openreview

parser = argparse.ArgumentParser()
parser.add_argument('--baseurl', help='base url')
parser.add_argument('--username')
parser.add_argument('--password')
args = parser.parse_args()

client = openreview.Client(
    baseurl=args.baseurl, username=args.username, password=args.password)

support = openreview.Group(**{
    'id': 'OpenReview.net/Support',
    'readers': ['everyone'],
    'writers': ['OpenReview.net/Support'],
    'signatures': ['OpenReview.net'],
    'signatories': ['OpenReview.net/Support'],
    'members': [],
    'web': './supportRequestsWeb.js'
})

request_content = {
    'title': {
        'value-copied': '{content[\'Official Venue Name\']}',
        'description': 'Used for display purposes. This is copied from the Official Venue Name',
        'order': 1
    },
    'Official Venue Name': {
        'description': 'This will appear on your venue\'s OpenReview page. Example: "Seventh International Conference on Learning Representations"',
        'value-regex': '.*',
        'required': True,
        'order': 2
    },
    'Abbreviated Venue Name': {
        'description': 'Please include the year as well. This will be used to identify your venue on OpenReview and in email subject lines. Example: "ICLR 2019"',
        'value-regex': '.*',
        'required': True,
        'order': 3
    },
    'Official Website URL': {
        'description': 'Please provide the official website URL of the venue.',
        'value-regex': '.*',
        'required': True,
        'order': 4
    },
    'Contact Emails': {
        'description': 'Please provide *lower-cased* email addresses of all the Program Chairs or Organizers (comma-separated) including yourself.',
        'values-regex': '([a-z0-9_\-\.]{2,}@[a-z0-9_\-\.]{2,}\.[a-z]{2,},){0,}([a-z0-9_\-\.]{2,}@[a-z0-9_\-\.]{2,}\.[a-z]{2,})',
        'required': True,
        'order': 5
    },
    'Area Chairs (Metareviewers)': {
        'description': 'Does your venue have Area Chairs?',
        'value-radio': [
            'Yes, our venue has Area Chairs',
            'No, our venue does not have Area Chairs'
        ],
        'required': True,
        'order': 6
    },
    'Submission Start Date': {
        'description': 'When would you (ideally) like to have your OpenReview submission portal opened? Please specify the date and time in GMT using the following format: YYYY/MM/DD HH:MM(e.g. 2019/01/31 23:59). (Skip this if only requesting paper matching service)',
        'value-regex': '.*',
        'order': 7
    },
    'Submission Deadline': {
        'value-regex': '^[0-9]{4}\/([1-9]|0[1-9]|1[0-2])\/([1-9]|0[1-9]|[1-2][0-9]|3[0-1])(\s+)?((2[0-3]|[01][0-9]|[0-9]):[0-5][0-9])?(\s+)?$',
        'description': 'By when do authors need to submit their manuscripts? Please specify the due date in GMT using the following format: YYYY/MM/DD HH:MM(e.g. 2019/01/31 23:59)',
        'order': 8
    },
    'Venue Start Date': {
        'description': 'What date does the venue start? Please use the following format: YYYY/MM/DD (e.g. 2019/01/31)',
        'value-regex': '^[0-9]{4}\/([1-9]|0[1-9]|1[0-2])\/([1-9]|0[1-9]|[1-2][0-9]|3[0-1])(\s+)?((2[0-3]|[01][0-9]|[0-9]):[0-5][0-9])?(\s+)?$',
        'order': 9
    },
    'Location': {
        'description': 'Where is the event being held. For example: Amherst, Massachusetts, United States',
        'value-regex': '.*',
        'order': 16
    },
    'Paper Matching': {
        'description': 'Choose options for assigning papers to reviewers. If using the OpenReview Paper Matching System, see the top of the page for a description of each feature type.',
        'values-checkbox': [
            'Organizers will assign papers manually',
            'Reviewer Bid Scores',
            'Reviewer Recommendation Scores',
            'OpenReview Affinity',
            'TPMS'
        ],
        'order': 17
    },
    'Author and Reviewer Anonymity': {
        'description': 'What policy best describes your anonymity policy? (If none of the options apply then please describe your request below)',
        'value-radio': [
            'Double-blind',
            'Single-blind (Reviewers are anonymous)',
            'No anonymity'
        ],
        'order': 18
    },
    'Open Reviewing Policy': {
        'description': 'Should submitted papers and/or reviews be visible to the public? (This is independent of anonymity policy)',
        'value-radio': [
            'Submissions and reviews should both be private.',
            'Submissions should be public, but reviews should be private.',
            'Submissions and reviews should both be public.'
        ],
        'order': 19
    },
    'Public Commentary': {
        'description': 'Would you like to allow members of the public to comment on papers?',
        'value-radio': [
            'No, do not allow public commentary.',
            'Yes, allow members of the public to comment non-anonymously.',
            'Yes, allow members of the public to comment anonymously.',
        ],
        'order': 20
    },
    'Expected Submissions': {
        'value-regex': '[0-9]*',
        'description': 'How many submissions are expected in this venue? Please provide a number.',
        'order': 21
    },
    'Other Important Information': {
        'value-regex': '[\\S\\s]{1,5000}',
        'description': 'Please use this space to clarify any questions for which you could not use any of the provided options, and to clarify any other information that you think we may need.',
        'order': 22
    },
    'How did you hear about us?': {
        'value-regex': '.*',
        'description': 'Please briefly describe how you heard about OpenReview.',
        'order': 23
    }
}

request_invitation = client.post_invitation(openreview.Invitation(**{
    'id': 'OpenReview.net/Support/-/Request_Form',
    'readers': ['everyone'],
    'writers': [],
    'signatures': ['OpenReview.net'],
    'invitees': ['everyone'],
    'process': 'supportProcess.js',
    'reply': {
        'readers': {
            'values-copied': [
                'OpenReview.net/Support',
                '{signatures}',
                '{content["Contact Emails"]}'
            ]
        },
        'writers': {
            'values-copied': [
                'OpenReview.net/Support',
                '{signatures}',
                '{content["Contact Emails"]}'
            ]
        },
        'signatures': {
            'values-regex': '~.*|OpenReview.net/Support'
        },
        'content': request_content
    }
}))

comment_invitation = client.post_invitation(openreview.Invitation(**{
    'id': 'OpenReview.net/Support/-/Comment',
    'readers': ['everyone'],
    'writers': ['OpenReview.net/Support'],
    'signatures': ['OpenReview.net/Support'],
    'invitees': ['everyone'],
    'process': 'commentProcess.js',
    'reply': {
        'forum': None,
        'replyto': None,
        'readers': {
            'description': 'Select all user groups that should be able to read this comment.',
            'values': ['OpenReview.net/Support']
        },
        'writers': {
            'values-copied': [
                '{signatures}'
            ]
        },
        'signatures': {
            'values-regex': '~.*|OpenReview.net/Support',
            'description': 'How your identity will be displayed.'
        },
        'content': {
            'title': {
                'order': 0,
                'value-regex': '.{1,500}',
                'description': 'Brief summary of your comment.',
                'required': True
            },
            'comment': {
                'order': 1,
                'value-regex': '[\\S\\s]{1,5000}',
                'description': 'Your comment or reply (max 5000 characters).',
                'required': True
            }
        }
    }
}))

remove_fields = ['Area Chairs (Metareviewers)', 'Author and Reviewer Anonymity', 'Open Reviewing Policy', 'Public Commentary', 'Paper Matching']
revision_content = {key: request_content[key] for key in request_content if key not in remove_fields}
revision_content['Additional Submission Options'] = {
    'order' : 18,
    'value-dict': {},
    'description': 'Configure additional options in the submission form. Valid JSON expected.'
}

revision_invitation = client.post_invitation(openreview.Invitation(**{
    'id': 'OpenReview.net/Support/-/Revision',
    'readers': ['everyone'],
    'writers': [],
    'signatures': ['OpenReview.net'],
    'invitees': ['everyone'],
    'multiReply': True,
    'process': 'revisionProcess.py',
    'reply': {
        'readers': {
            'values-copied': [
                'OpenReview.net/Support',
                '{content["Contact Emails"]}'
            ]
        },
        'writers': {
            'values-regex': '~.*',
        },
        'signatures': {
            'values-regex': '~.*'
        },
        'content': revision_content
    }
}))

deploy_content = {
    'venue_id': {
        'value-regex': '.*',
        'required': True,
        'description': 'Venue id'
    }
}

deploy_invitation = client.post_invitation(openreview.Invitation(**{
    'id': 'OpenReview.net/Support/-/Deploy',
    'readers': ['everyone'],
    'writers': [],
    'signatures': ['OpenReview.net/Support'],
    'invitees': ['OpenReview.net/Support'],
    'process': 'deployProcess.py',
    'multiReply': False,
    'reply': {
        'readers': {
            'values': ['OpenReview.net/Support']
        },
        'writers': {
            'values-regex': '~.*'
        },
        'signatures': {
            'values': ['OpenReview.net/Support']
        },
        'content': deploy_content
    }
}))

recruitment_content = {
    'title': {
        'value': 'Recruitment',
        'required': True,
        'order': 1
    },
    'invitee_role': {
        'description': 'Please select the role of the invitees in the venue.',
        'value-radio': ['reviewer', 'area chair'],
        'default': 'reviewer',
        'required': True,
        'order': 2
    },
    'invitee_details': {
        'value-regex': '[\\S\\s]{1,50000}',
        'description': 'Email,Name pairs expected with each line having only one invitee\'s details. E.g. captain_rogers@marvel.com, Captain America',
        'required': True,
        'order': 3
    },
    'invitation_email_subject': {
        'value-regex': '.*',
        'description': 'Please carefully review the email subject for the recruitment emails. Make sure not to remove the parenthesized tokens.',
        'order': 4,
        'required': True,
        'default': '[{Abbreviated_Venue_Name}] Invitation to serve as {invitee_role}'
    },
    'invitation_email_content': {
        'value-regex': '[\\S\\s]{1,10000}',
        'description': 'Please carefully review the template below before you click submit to send out recruitment emails. Make sure not to remove the parenthesized tokens.',
        'order': 5,
        'required': True,
        'default': '''Dear {name},

You have been nominated by the program chair committee of {Abbreviated_Venue_Name} to serve as {invitee_role}. As a respected researcher in the area, we hope you will accept and help us make {Abbreviated_Venue_Name} a success.

You are also welcome to submit papers, so please also consider submitting to {Abbreviated_Venue_Name}.

We will be using OpenReview.net and a reviewing process that we hope will be engaging and inclusive of the whole community.

To ACCEPT the invitation, please click on the following link:

{accept_url}

To DECLINE the invitation, please click on the following link:

{decline_url}

Please answer within 10 days.

If you accept, please make sure that your OpenReview account is updated and lists all the emails you are using. Visit http://openreview.net/profile after logging in.

If you have any questions, please contact us at info@openreview.net.

Cheers!

Program Chairs
'''
    }
}

recruitment_invitation = client.post_invitation(openreview.Invitation(**{
    'id': 'OpenReview.net/Support/-/Recruitment',
    'readers': ['everyone'],
    'writers': [],
    'signatures': ['OpenReview.net/Support'],
    'invitees': ['OpenReview.net/Support'],
    'process': 'recruitmentProcess.py',
    'multiReply': True,
    'reply': {
        'readers': {
            'values': ['everyone']
        },
        'writers': {
            'values':[],
        },
        'signatures': {
            'values-regex': '~.*|OpenReview.net/Support'
        },
        'content': recruitment_content
    }
}))

bid_stage_content = {
    'bid_start_date': {
        'description': 'When does bidding on submissions begin? Please use the format: YYYY/MM/DD HH:MM (e.g. 2019/01/31 23:59)',
        'value-regex': '^[0-9]{4}\/([1-9]|0[1-9]|1[0-2])\/([1-9]|0[1-9]|[1-2][0-9]|3[0-1])(\s+)?((2[0-3]|[01][0-9]|[0-9]):[0-5][0-9])?(\s+)?$'
    },
    'bid_due_date': {
        'description': 'When does bidding on submissions end? Please use the format: YYYY/MM/DD HH:MM (e.g. 2019/01/31 23:59)',
        'value-regex': '^[0-9]{4}\/([1-9]|0[1-9]|1[0-2])\/([1-9]|0[1-9]|[1-2][0-9]|3[0-1])(\s+)?((2[0-3]|[01][0-9]|[0-9]):[0-5][0-9])?(\s+)?$',
        'required': True
    },
    'bid_count': {
        'description': 'Minimum bids one should make to mark bidding task completed for them. Default is 50.',
        'value-regex': '[0-9]*'
    }
}

bid_stage_invitation = client.post_invitation(openreview.Invitation(**{
    'id': 'OpenReview.net/Support/-/Bid_Stage',
    'readers': ['everyone'],
    'writers': ['OpenReview.net/Support'],
    'signatures': ['OpenReview.net/Support'],
    'invitees': ['everyone'],
    'multiReply': True,
    'process': 'revisionProcess.py',
    'reply': {
        'readers': {
            'values-copied': [
                'OpenReview.net/Support',
                '{content["Contact Emails"]}'
            ]
        },
        'writers': {
            'values-regex': '~.*',
        },
        'signatures': {
            'values-regex': '~.*'
        },
        'content': bid_stage_content
    }
}))

review_stage_content = {
    'review_start_date': {
        'description': 'When does reviewing of submissions begin? Please use the following format: YYYY/MM/DD HH:MM (e.g. 2019/01/31 23:59)',
        'value-regex': '^[0-9]{4}\/([1-9]|0[1-9]|1[0-2])\/([1-9]|0[1-9]|[1-2][0-9]|3[0-1])(\s+)?((2[0-3]|[01][0-9]|[0-9]):[0-5][0-9])?(\s+)?$',
        'order': 10
    },
    'review_deadline': {
        'description': 'When does reviewing of submissions end? Please use the following format: YYYY/MM/DD HH:MM (e.g. 2019/01/31 23:59)',
        'value-regex': '^[0-9]{4}\/([1-9]|0[1-9]|1[0-2])\/([1-9]|0[1-9]|[1-2][0-9]|3[0-1])(\s+)?((2[0-3]|[01][0-9]|[0-9]):[0-5][0-9])?(\s+)?$',
        'required': True,
        'order': 11
    },
    'make_reviews_public': {
        'description': 'Should the reviews be made public immediately upon posting? Default is "No, reviews should NOT be revealed publicly when they are posted".',
        'value-radio': [
            'Yes, reviews should be revealed publicly when they are posted',
            'No, reviews should NOT be revealed publicly when they are posted'
        ],
        'required': True,
        'default': 'No, reviews should NOT be revealed publicly when they are posted',
        'order': 24
    },
    'release_reviews_to_authors': {
        'description': 'Should the reviews be visible to paper\'s authors immediately upon posting? Default is "No, reviews should NOT be revealed when they are posted to the paper\'s authors".',
        'value-radio': [
            'Yes, reviews should be revealed when they are posted to the paper\'s authors',
            'No, reviews should NOT be revealed when they are posted to the paper\'s authors'
        ],
        'required': True,
        'default': 'No, reviews should NOT be revealed when they are posted to the paper\'s authors',
        'order': 25
    },
    'release_reviews_to_reviewers': {
        'description': 'Should the reviews be visible immediately upon posting to paper\'s reviewers regardless of whether they have submitted their review or not? Default is "No, reviews should be immediately revealed only to the reviewers who have already reviewed the paper".',
        'value-radio': [
            'Yes, reviews should be immediately revealed to the all paper\'s reviewers',
            'No, reviews should be immediately revealed only to the reviewers who have already reviewed the paper'
        ],
        'required': True,
        'default': 'No, reviews should be immediately revealed only to the reviewers who have already reviewed the paper',
        'order': 26
    },
    'email_program_chairs_about_reviews': {
        'description': 'Should Program Chairs be emailed when each review is received? Default is "No, do not email program chairs about received reviews".',
        'value-radio': [
            'Yes, email program chairs for each review received',
            'No, do not email program chairs about received reviews'],
        'required': True,
        'default': 'No, do not email program chairs about received reviews',
        'order': 27
    },
    'additional_review_form_options': {
        'order' : 28,
        'value-dict': {},
        'required': False,
        'description': 'Configure additional options in the review form. Valid JSON expected.'
    },
    'remove_review_form_options': {
        'order': 29,
        'value-regex': '^[^,]+(,\s*[^,]*)*$',
        'required': False,
        'description': 'Comma separated list of fields that you want removed from the review form.'
    }
}

review_stage_invitation = client.post_invitation(openreview.Invitation(**{
    'id': 'OpenReview.net/Support/-/Review_Stage',
    'readers': ['everyone'],
    'writers': ['OpenReview.net/Support'],
    'signatures': ['OpenReview.net'],
    'invitees': ['everyone'],
    'multiReply': True,
    'process': 'revisionProcess.py',
    'reply': {
        'readers': {
            'values-copied': [
                'OpenReview.net/Support',
                '{content["Contact Emails"]}'
            ]
        },
        'writers': {
            'values-copied': ['{signatures}'],
        },
        'signatures': {
            'values-regex': '~.*|OpenReview.net/Support'
        },
        'content': review_stage_content
    }
}))

meta_review_stage_content = {
    'meta_review_start_date': {
        'description': 'When does the meta reviewing of submissions begin? Please use the following format: YYYY/MM/DD HH:MM (e.g. 2019/01/31 23:59) (Skip this if your venue does not have Area Chairs)',
        'value-regex': '^[0-9]{4}\/([1-9]|0[1-9]|1[0-2])\/([1-9]|0[1-9]|[1-2][0-9]|3[0-1])(\s+)?((2[0-3]|[01][0-9]|[0-9]):[0-5][0-9])?(\s+)?$',
        'order': 12
    },
    'meta_review_deadline': {
        'description': 'By when should the meta-reviews be in the system? Please use the following format: YYYY/MM/DD HH:MM (e.g. 2019/01/31 23:59) (Skip this if your venue does not have Area Chairs)',
        'value-regex': '^[0-9]{4}\/([1-9]|0[1-9]|1[0-2])\/([1-9]|0[1-9]|[1-2][0-9]|3[0-1])(\s+)?((2[0-3]|[01][0-9]|[0-9]):[0-5][0-9])?(\s+)?$',
        'order': 13
    },
    'make_meta_reviews_public': {
        'description': 'Should the meta reviews be visible publicly immediately upon posting? Default is "No, meta reviews should NOT be revealed publicly when they are posted".',
        'value-radio': [
            'Yes, meta reviews should be revealed publicly when they are posted',
            'No, meta reviews should NOT be revealed publicly when they are posted'
        ],
        'required': True,
        'default': 'No, meta reviews should NOT be revealed publicly when they are posted',
        'order': 28
    }
}

meta_review_stage_invitation = client.post_invitation(openreview.Invitation(**{
    'id': 'OpenReview.net/Support/-/Meta_Review_Stage',
    'readers': ['everyone'],
    'writers': [],
    'signatures': ['OpenReview.net'],
    'invitees': ['everyone'],
    'multiReply': True,
    'process': 'revisionProcess.py',
    'reply': {
        'readers': {
            'values-copied': [
                'OpenReview.net/Support',
                '{content["Contact Emails"]}'
            ]
        },
        'writers': {
            'values-copied': ['{signatures}'],
        },
        'signatures': {
            'values-regex': '~.*|OpenReview.net/Support'
        },
        'content': meta_review_stage_content
    }
}))

decision_stage_content = {
    'decision_start_date': {
        'description': 'When will the program chairs start posting decisions? Please use the following format: YYYY/MM/DD HH:MM(e.g. 2019/01/31 23:59)',
        'value-regex': '^[0-9]{4}\/([1-9]|0[1-9]|1[0-2])\/([1-9]|0[1-9]|[1-2][0-9]|3[0-1])(\s+)?((2[0-3]|[01][0-9]|[0-9]):[0-5][0-9])?(\s+)?$',
        'order': 14
    },
    'decision_deadline': {
        'description': 'By when should all the decisions be in the system? Please use the following format: YYYY/MM/DD HH:MM(e.g. 2019/01/31 23:59)',
        'value-regex': '^[0-9]{4}\/([1-9]|0[1-9]|1[0-2])\/([1-9]|0[1-9]|[1-2][0-9]|3[0-1])(\s+)?((2[0-3]|[01][0-9]|[0-9]):[0-5][0-9])?(\s+)?$',
        'order': 15
    },
    'decision_options': {
        'description': 'What are the decision options (provide comma separated values, e.g. Accept (Best Paper), Accept, Reject)? Leave empty for default options - "Accept (Oral)", "Accept (Poster)", "Reject"',
        'value-regex': '.*',
        'order': 30
    },
    'make_decisions_public': {'description': 'Should the decisions be made public immediately upon posting? Default is "No, decisions should NOT be revealed publicly when they are posted".',
        'value-radio': [
            'Yes, decisions should be revealed publicly when they are posted',
            'No, decisions should NOT be revealed publicly when they are posted'
        ],
        'required': True,
        'default': 'No, decisions should NOT be revealed publicly when they are posted',
        'order': 31
    },
    'release_decisions_to_authors': {
        'description': 'Should the decisions be visible to paper\'s authors immediately upon posting? Default is "No, decisions should NOT be revealed when they are posted to the paper\'s authors".',
        'value-radio': [
            'Yes, decisions should be revealed when they are posted to the paper\'s authors',
            'No, decisions should NOT be revealed when they are posted to the paper\'s authors'
        ],
        'required': True,
        'default': 'No, decisions should NOT be revealed when they are posted to the paper\'s authors',
        'order': 32
    },
    'release_decision_to_reviewers': {
        'description': 'Should the decisions be immediately revealed to paper\'s reviewers? Default is "No, decisions should not be immediately revealed to the paper\'s reviewers"',
        'value-radio': [
            'Yes, decisions should be immediately revealed to the paper\'s reviewers',
            'No, decisions should not be immediately revealed to the paper\'s reviewers'
        ],
        'required': True,
        'default': 'No, decisions should not be immediately revealed to the paper\'s reviewers',
        'order': 33
    }
}

decision_stage_invitation = client.post_invitation(openreview.Invitation(**{
    'id': 'OpenReview.net/Support/-/Decision_Stage',
    'readers': ['everyone'],
    'writers': [],
    'signatures': ['OpenReview.net'],
    'invitees': ['everyone'],
    'multiReply': True,
    'process': 'revisionProcess.py',
    'reply': {
        'readers': {
            'values-copied': [
                'OpenReview.net/Support',
                '{content["Contact Emails"]}'
            ]
        },
        'writers': {
            'values-copied': ['{signatures}'],
        },
        'signatures': {
            'values-regex': '~.*|OpenReview.net/Support'
        },
        'content': decision_stage_content
    }
}))
