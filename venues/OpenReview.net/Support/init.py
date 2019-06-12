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
        'description': 'Used for display purposes. Will be copied from the Official Venue Name',
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
        'description': 'When would you (ideally) like to have your OpenReview submission portal opened? Please submit in the following format: YYYY/MM/DD HH:MM(e.g. 2019/01/31 23:59). (Skip this if only requesting paper matching service)',
        'value-regex': '.*',
        'order': 7
    },
    'Submission Deadline': {
        'value-regex': '.*',
        'description': 'By when do authors need to submit their manuscripts? Please submit in the following format: YYYY/MM/DD HH:MM(e.g. 2019/01/31 23:59)',
        'order': 8
    },
    'Venue Start Date': {
        'description': 'What date does the venue start? Please submit in the following format: YYYY/MM/DD (e.g. 2019/01/31)',
        'value-regex': '.*',
        'order': 9
    },
    'Location': {
        'description': 'Where is the event being held. For example: Amherst, Massachusetts, United States',
        'value-regex': '.*',
        'order': 10
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
        'order': 11
    },
    'Author and Reviewer Anonymity': {
        'description': 'What policy best describes your anonymity policy? (If none of the options apply then please describe your request below)',
        'value-radio': [
            'Double-blind',
            'Single-blind (Reviewers are anonymous)',
            'No anonymity'
        ],
        'order': 12
    },
    'Open Reviewing Policy': {
        'description': 'Should submitted papers and/or reviews be visible to the public? (This is independent of anonymity policy)',
        'value-radio': [
            'Submissions and reviews should both be private.',
            'Submissions should be public, but reviews should be private.',
            'Submissions and reviews should both be public.'
        ],
        'order': 13
    },
    'Public Commentary': {
        'description': 'Would you like to allow members of the public to comment on papers?',
        'value-radio': [
            'No, do not allow public commentary.',
            'Yes, allow members of the public to comment non-anonymously.',
            'Yes, allow members of the public to comment anonymously.',
        ],
        'order': 14
    },
    'Expected Submissions': {
        'value-regex': '[0-9]*',
        'description': 'How many submissions are expected in this venue? Please provide a number.',
        'order': 15
    },
    'Other Important Information': {
        'value-regex': '[\\S\\s]{1,5000}',
        'description': 'Please use this space to clarify any questions above for which you could not use any of the provide options, and to clarify any other information that you think we may need.',
        'order': 16
    },
    'How did you hear about us?': {
        'value-regex': '.*',
        'description': 'Please briefly describe how you heard about OpenReview.',
        'order': 17
    }
}

request_inv = client.post_invitation(openreview.Invitation(**{
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

comment_inv = client.post_invitation(openreview.Invitation(**{
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

revision_inv = client.post_invitation(openreview.Invitation(**{
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

deploy_inv = client.post_invitation(openreview.Invitation(**{
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

reviewer_recruitment_content = {
    'title': {
        'value': 'Reviewer recruitment',
        'required': True,
        'order': 1
    },
    'reviewer_emails': {
        'value-regex': '[\\S\\s]{1,20000}',
        'description': 'Please provide comma separated valid reviewer emails. (e.g.  captain_rogers@marvel.com, black_widow@mcu.com)',
        'required': True,
        'order': 2
    },
    'reviewer_names': {
        'value-regex': '[\\S\\s]{1,20000}',
        'description': 'Please provide comma separated reviewer names in the *same order* as emails. (e.g. Steve Rogers, Natasha Romanoff)',
        'order': 3
    },
    'invitation_email_subject': {
        'value-regex': '.*',
        'description': 'Please carefully review the email subject for the recruitment emails. Make sure not to remove the parenthesized tokens.',
        'order': 4,
        'required': True,
        'default': '[{Abbreviated_Venue_Name}] Invitation to serve as a reviewer'
    },
    'invitation_email_content': {
        'value-regex': '[\\S\\s]{1,10000}',
        'description': 'Please carefully review the template below before you click submit to send out recruitment emails. Make sure not to remove the parenthesized tokens.',
        'order': 5,
        'required': True,
        'default': '''Dear {name},

You have been nominated by the program chair committee of {Abbreviated_Venue_Name} to serve as a reviewer.  As a respected researcher in the area, we hope you will accept and help us make {Abbreviated_Venue_Name} a success.

Reviewers are also welcome to submit papers, so please also consider submitting to {Abbreviated_Venue_Name}.

We will be using OpenReview.net and a reviewing process that we hope will be engaging and inclusive of the whole community.

The success of the {Abbreviated_Venue_Name} depends on the quality of the reviewing process and ultimately on the quality and dedication of the reviewers. We hope you will accept our invitation.

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

reviewer_recruitment_inv = client.post_invitation(openreview.Invitation(**{
    'id': 'OpenReview.net/Support/-/Reviewer_Recruitment',
    'readers': ['everyone'],
    'writers': [],
    'signatures': ['OpenReview.net/Support'],
    'invitees': ['OpenReview.net/Support'],
    'process': 'reviewerRecruitmentProcess.py',
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
        'content': reviewer_recruitment_content
    }
}))

ac_recruitment_content = {
    'title': {
        'value': 'Area chair recruitment',
        'required': True,
        'order': 1
    },
    'area_chair_emails': {
        'value-regex': '.*',
        'description': 'Please provide comma separated valid area chair emails to be invited',
        'required': True,
        'order': 2
    },
    'area_chair_names': {
        'value-regex': '.*',
        'description': 'Please provide comma separated area chair names in the *same order* as emails above.',
        'order': 3
    },
    'invitation_email_subject': {
        'value-regex': '.*',
        'description': 'Please carefully review the subject for the recruitment emails. Make sure not to remove the parenthesized tokens.',
        'order': 4,
        'required': True,
        'default': '[{Abbreviated_Venue_Name}] Invitation to serve as an area chair'
    },
    'invitation_email_content': {
        'value-regex': '[\\S\\s]{1,10000}',
        'description': 'Please carefully review the template below before you click submit to send out the recruitment emails. Make sure not to remove the parenthesized tokens.',
        'order': 5,
        'required': True,
        'default': '''Dear {name},

You have been nominated by the program chair committee of {Abbreviated_Venue_Name} to serve as an area chair.  As a respected researcher in the area, we hope you will accept and help us make {Abbreviated_Venue_Name} a success.

Area chairs are also welcome to submit papers, so please also consider submitting to {Abbreviated_Venue_Name}.

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

ac_recruitment_inv = client.post_invitation(openreview.Invitation(**{
    'id': 'OpenReview.net/Support/-/Area_Chair_Recruitment',
    'readers': ['everyone'],
    'writers': [],
    'signatures': ['OpenReview.net/Support'],
    'invitees': ['OpenReview.net/Support'],
    'process': 'areaChairRecruitmentProcess.py',
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
        'content': ac_recruitment_content
    }
}))