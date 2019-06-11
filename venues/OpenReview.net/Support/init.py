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
        'description': 'By when do authors need to submit their manuscripts? Please use the following format (GMT Timezone): YYYY/MM/DD HH:MM(e.g. 2019/01/31 23:59)',
        'order': 8
    },
    'Venue Start Date': {
        'description': 'What date does the venue start? Please use the following format: YYYY/MM/DD (e.g. 2019/01/31)',
        'value-regex': '.*',
        'order': 9
    },
    'Review Deadline (GMT)': {
        'description': 'When does reviewing of submissions end? Please use the following format: YYYY/MM/DD HH:MM (e.g. 2019/01/31 23:59)',
        'value-regex': '.*',
        'order': 11
    },
    'Meta Review Deadline (GMT)': {
        'description': 'By when should the meta-reviews be in the system? Please use the following format: YYYY/MM/DD HH:MM (e.g. 2019/01/31 23:59)  (Skip this if your venue does not have Area Chairs)',
        'value-regex': '.*',
        'order': 12
    },
    'Decision Deadline (GMT)': {
        'description': 'By when should the decisions be in the system? Please use the following format: YYYY/MM/DD HH:MM(e.g. 2019/01/31 23:59)',
        'value-regex': '.*',
        'order': 13
    },
    'Location': {
        'description': 'Where is the event being held. For example: Amherst, Massachusetts, United States',
        'value-regex': '.*',
        'order': 14
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
        'order': 15
    },
    'Author and Reviewer Anonymity': {
        'description': 'What policy best describes your anonymity policy? (If none of the options apply then please describe your request below)',
        'value-radio': [
            'Double-blind',
            'Single-blind (Reviewers are anonymous)',
            'No anonymity'
        ],
        'order': 16
    },
    'Open Reviewing Policy': {
        'description': 'Should submitted papers and/or reviews be visible to the public? (This is independent of anonymity policy)',
        'value-radio': [
            'Submissions and reviews should both be private.',
            'Submissions should be public, but reviews should be private.',
            'Submissions and reviews should both be public.'
        ],
        'order': 17
    },
    'Public Commentary': {
        'description': 'Would you like to allow members of the public to comment on papers?',
        'value-radio': [
            'No, do not allow public commentary.',
            'Yes, allow members of the public to comment non-anonymously.',
            'Yes, allow members of the public to comment anonymously.',
        ],
        'order': 18
    },
    'Expected Submissions': {
        'value-regex': '[0-9]*',
        'description': 'How many submissions are expected in this venue? Please provide a number.',
        'order': 19
    },
    'Other Important Information': {
        'value-regex': '[\\S\\s]{1,5000}',
        'description': 'Please use this space to clarify any questions above for which you could not use any of the provide options, and to clarify any other information that you think we may need.',
        'order': 20
    },
    'How did you hear about us?': {
        'value-regex': '.*',
        'description': 'Please briefly describe how you heard about OpenReview.',
        'order': 21
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

client.post_invitation(request_inv)
client.post_invitation(revision_inv)
client.post_invitation(deploy_inv)

anonymize_submissions_content = {
    'title': {
        'value': 'Anonymize Submissions',
        'required': True,
        'order': 1
    },
    'anonymize_submissions': {
        'value-checkbox': 'Create anonymized versions of submissions',
        'description': 'This will only create anonymized versions of submissions posted since this feature was used last. If this is being used for the first time, it will create anonymized copies of all submissions in your conference',
        'required': True,
        'order': 2
    }
}

anonymize_submissions_invitation = client.post_invitation(openreview.Invitation(**{
    'id': 'OpenReview.net/Support/-/Anonymize_Submissions',
    'readers': ['everyone'],
    'writers': ['OpenReview.net/Support'],
    'signatures': ['OpenReview.net'],
    'invitees': ['OpenReview.net/Support'],
    'process': 'anonymizeSubmissions.py',
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
        'content': anonymize_submissions_content
    }
}))

deanonymize_submissions_content = {
    'title': {
        'value': 'Deanonymize Submissions',
        'required': True,
        'order': 1
    },
    'deanonymize_submission': {
        'value-checkbox': 'Deanonymize previously anonymized versions of submissions',
        'description': 'This feature will deanonymized anonymized versions of submissions created earlier in the conference to reveal author names to the readers of the submissions. Use this with care because you are revealing author information with this and the process is irreversible.',
        'required': True,
        'order': 2
    }
}

deanonymize_submissions_invitation = client.post_invitation(openreview.Invitation(**{
    'id': 'OpenReview.net/Support/-/Deanonymize_Submission',
    'readers': ['everyone'],
    'writers': ['OpenReview.net/Support'],
    'signatures': ['OpenReview.net/Support'],
    'invitees': ['OpenReview.net/Support'],
    'process': 'deanonymizeSubmissions.py',
    'multiReply': False,
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
        'content': deanonymize_submissions_content
    }
}))

bid_invitation_content = {
    'title': {
        'value': 'Configure Bidding',
        'required': True,
        'order': 1
    },
    'bidding_enabled_for': {
        'values-checkbox': ['Reviewers', 'Area Chairs'],
        'description': 'Select who should bid on submissions. Please only select reviewers if your venue does not have Area Chairs',
        'default': ['Reviewers'],
        'required': True,
        'order': 2
    },
    'bid_deadline_(GMT)': {
        'description': 'When does bidding on submissions end? Please use the following format: YYYY/MM/DD HH:MM (e.g. 2019/01/31 23:59) (Skip this if you are not using paper matching with reviewer bid scores)',
        'value-regex': '.*',
        'order': 10
    },
}

bid_invitation = client.post_invitation(openreview.Invitation(**{
    'id': 'OpenReview.net/Support/-/Configure_Bidding',
    'readers': ['everyone'],
    'writers': ['OpenReview.net/Support'],
    'signatures': ['OpenReview.net/Support'],
    'invitees': ['OpenReview.net/Support'],
    'multiReply': False,
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
        'content': bid_invitation_content
    }
}))