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
        'description': 'Please provide the email addresses of all the Program Chairs or Organizers (comma-separated)',
        'values-regex': '.*',
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
        'description': 'When would you (ideally) like to have your OpenReview submission portal opened? Please use the following format: YYYY/MM/DD HH:MM(e.g. 2019/01/31 23:59). (Skip this if only requesting paper matching service)',
        'value-regex': '.*',
        'order': 7
    },
    'Submission Deadline': {
        'value-regex': '.*',
        'description': 'By when do authors need to submit their manuscripts? Please use the following format: YYYY/MM/DD HH:MM(e.g. 2019/01/31 23:59)',
        'order': 8
    },
    'Venue Start Date': {
        'description': 'What date does the venue start? Please use the following format: YYYY/MM/DD (e.g. 2019/01/31)',
        'value-regex': '.*',
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
        'description': 'Please use this space to clarify any questions above for which you could not use any of the provide options, and to clarify any other information that you think we may need.',
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

remove_fields = ['Area Chairs (Metareviewers)', 'Author and Reviewer Anonymity', 'Open Reviewing Policy', 'Public Commentary']
revision_content = {key: request_content[key] for key in request_content if key not in remove_fields}
revision_content['Additional Submission Options'] = {
    'order' : 18,
    'value-regex': '[\\S\\s]{1,10000}',
    'description': 'Configure additional options in the submission form. Valid JSON expected.'
}

revision_invitation = client.post_invitation(openreview.Invitation(**{
    'id': 'OpenReview.net/Support/-/Revision',
    'readers': ['everyone'],
    'writers': [],
    'signatures': ['OpenReview.net'],
    'invitees': ['everyone'],
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

deploy_content = {'venue_id': {
    'value-regex': '.*', 'description': 'Venue id'}}

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
            'values-regex': '~.*',
        },
        'signatures': {
            'values-regex': '~.*'
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
    'invitee_emails': {
        'value-regex': '[\\S\\s]{1,20000}',
        'description': 'Please provide comma separated valid emails. (e.g.  captain_rogers@marvel.com, black_widow@mcu.com)',
        'required': True,
        'order': 3
    },
    'invitee_names': {
        'value-regex': '[\\S\\s]{1,20000}',
        'description': 'Please provide comma separated names in the *same order* as emails. (e.g. Steve Rogers, John, Natasha Romanoff)',
        'order': 4
    },
    'invitation_email_subject': {
        'value-regex': '.*',
        'description': 'Please carefully review the email subject for the recruitment emails. Make sure not to remove the parenthesized tokens.',
        'order': 5,
        'required': True,
        'default': '[{Abbreviated_Venue_Name}] Invitation to serve as {invitee_role}'
    },
    'invitation_email_content': {
        'value-regex': '[\\S\\s]{1,10000}',
        'description': 'Please carefully review the template below before you click submit to send out recruitment emails. Make sure not to remove the parenthesized tokens.',
        'order': 6,
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

If you accept, please make sure that your OpenReview account is updated and lists all the emails you are using.  Visit http://openreview.net/profile after logging in.

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
            'values-regex': '~.*',
        },
        'signatures': {
            'values-regex': '~.*'
        },
        'content': recruitment_content
    }
}))

bid_stage_content = {
    'bid_start_date': {
        'description': 'When does bidding on submissions begin? Please use the format: YYYY/MM/DD HH:MM (e.g. 2019/01/31 23:59)',
        'value-regex': '.*'
    },
    'bid_due_date': {
        'description': 'When does bidding on submissions end? Please use the format: YYYY/MM/DD HH:MM (e.g. 2019/01/31 23:59)',
        'value-regex': '.*'
    },
    'bid_count': {
        'description': 'Minimum bids a person needs to make to mark bidding task as completed for them. Default is 50.',
        'value-regex': '.*'
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
        'value-regex': '.*',
        'order': 10
    },
    'review_deadline': {
        'description': 'When does reviewing of submissions end? Please use the following format: YYYY/MM/DD HH:MM (e.g. 2019/01/31 23:59)',
        'value-regex': '.*',
        'order': 11
    },
    'release_reviews_to_authors': {
        'description': 'Should the reviews be visible immediately upon posting to paper\'s author? Default is "No".',
        'value-radio': ['Yes', 'No'],
        'default': 'No',
        'order': 24
    },
    'release_reviews_to_reviewers': {
        'description': 'Should the reviews be visible immediately upon posting to paper\'s reviewers regardless of whether they have submitted their reviews or not? Default is "No".',
        'value-radio': ['Yes', 'No'],
        'default': 'No',
        'order': 25
    },
    'email_program_chairs_about_reviews': {
        'description': 'Should Program Chairs be emailed when each review is posted? Default is "No".',
        'value-radio': ['Yes', 'No'],
        'default': 'No',
        'order': 26
    },
    'additional_review_options' : {
        'order' : 27,
        'value-regex': '[\\S\\s]{1,10000}',
        'description': 'Configure additional options in the review form. Valid JSON expected.'
    }
}

review_stage_invitation = client.post_invitation(openreview.Invitation(**{
    'id': 'OpenReview.net/Support/-/Review_Stage',
    'readers': ['everyone'],
    'writers': ['OpenReview.net/Support'],
    'signatures': ['OpenReview.net'],
    'invitees': ['everyone'],
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
        'content': review_stage_content
    }
}))

meta_review_stage_content = {
    'meta_review_start_date': {
        'description': 'When does the meta reviewing of submissions begin? Please use the following format: YYYY/MM/DD HH:MM (e.g. 2019/01/31 23:59) (Skip this if your venue does not have Area Chairs)',
        'value-regex': '.*',
        'order': 12
    },
    'meta_review_deadline': {
        'description': 'By when should the meta-reviews be in the system? Please use the following format: YYYY/MM/DD HH:MM (e.g. 2019/01/31 23:59) (Skip this if your venue does not have Area Chairs)',
        'value-regex': '.*',
        'order': 13
    },
    'make_meta_reviews_public': {
        'description': 'Should the meta reviews be visible publicly immediately upon creation? Default is "No".',
        'value-radio': ['Yes', 'No'],
        'default': 'No',
        'order': 28
    },
    'additional_meta_review_options' : {
        'order' : 29,
        'value-regex': '[\\S\\s]{1,10000}',
        'description': 'Configure additional options in the meta review form. Valid JSON expected.'
    }
}

meta_review_stage_invitation = client.post_invitation(openreview.Invitation(**{
    'id': 'OpenReview.net/Support/-/Meta_Review_Stage',
    'readers': ['everyone'],
    'writers': [],
    'signatures': ['OpenReview.net'],
    'invitees': ['everyone'],
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
        'content': meta_review_stage_content
    }
}))

decision_stage_content = {
    'decision_start_date': {
        'description': 'When does the decision be in the system? Please use the following format: YYYY/MM/DD HH:MM(e.g. 2019/01/31 23:59)',
        'value-regex': '.*',
        'order': 14
    },
    'decision_deadline': {
        'description': 'By when should the decisions be in the system? Please use the following format: YYYY/MM/DD HH:MM(e.g. 2019/01/31 23:59)',
        'value-regex': '.*',
        'order': 15
    },
    'decision_options': {
        'description': 'What are the decision options (provide comma separated values, e.g. Accept (Best Paper), Accept, Reject)? Leave empty for default options - "Accept (Oral)", "Accept (Poster)", "Reject"',
        'value-regex': '.*',
        'order': 30
    },
    'make_decisions_public': {
        'description': 'Should the decisions be visible publicly immediately upon creation? Default is "No". If "Yes", then next 2 questions need not be answered.',
        'value-radio': ['Yes', 'No'],
        'default': 'No',
        'order': 31
    },
    'release_decisions_to_authors': {
        'description': 'Should the decisions be visible immediately upon posting to paper\'s author? Default is "No".',
        'value-radio': ['Yes', 'No'],
        'default': 'No',
        'order': 32
    },
    'release_decision_to_reviewers': {
        'description': 'Should the decisions be visible immediately upon posting to paper\'s reviewers? Default is "No".',
        'value-radio': ['Yes', 'No'],
        'default': 'No',
        'order': 33
    },
    'additional_decision_options' : {
        'value-regex': '[\\S\\s]{1,10000}',
        'description': 'Configure additional options in the decision form. Valid JSON expected.',
        'order' : 34
    }
}

decision_stage_invitation = client.post_invitation(openreview.Invitation(**{
    'id': 'OpenReview.net/Support/-/Decision_Stage',
    'readers': ['everyone'],
    'writers': [],
    'signatures': ['OpenReview.net'],
    'invitees': ['everyone'],
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
        'content': decision_stage_content
    }
}))