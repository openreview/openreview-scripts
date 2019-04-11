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

reader_options = [
    'Program Chairs',
    'Assigned Area Chairs/Metareviewers',
    'Assigned Reviewers',
    'All Area Chairs/Metareviewers',
    'All Reviewers',
    'All Authors',
    'Everyone directly involved in the Conference',
    'Logged-in OpenReview Users',
    'General Public',
    'Other'
]

request_content = {
    'title': {
        'value-copied': '{content[\'Official Conference Name\']}',
        'description': 'Used for display purposes. Will be copied from the Official Conference Name'
    },
    'Official Conference Name': {
        'description': 'This will appear on your conference\'s OpenReview page. Example: "Seventh International Conference on Learning Representations"',
        'value-regex': '.*',
        'required': True,
        'order': 1
    },
    'Abbreviated Conference Name': {
        'description': 'Please include the year as well. This will be used to identify your conference on OpenReview and in email subject lines. Example: "ICLR 2019"',
        'value-regex': '.*',
        'required': True,
        'order': 2
    },
    'Official Website URL': {
        'description': 'Please provide the official website URL of the conference.',
        'value-regex': '.*',
        'required': True,
        'order': 3
    },
    'Contact Emails': {
        'description': 'Please provide the email addresses of all the Program Chairs or Organizers (comma-separated)',
        'values-regex': '.*',
        'required': True,
        'order': 4
    },
    'Area Chairs (Metareviewers)': {
        'description': 'Does your conference have Area Chairs?',
        'value-radio': [
            'Yes, our conference has Area Chairs',
            'No, our conference does not have Area Chairs',
            'Other (describe below)'
        ],
        'required': True,
        'order': 5
    },
    'Submission Start Date': {
        'description': 'When would you (ideally) like to have your OpenReview submission portal opened? Please submit in the following format: YYYY/MM/DD HH:MM(e.g. 2019/01/31 23:59). (Skip this if only requesting paper matching service)',
        'value-regex': '.*',
        'order': 6
    },
    'Submission Deadline': {
        'value-regex': '.*',
        'description': 'By when do authors need to submit their manuscripts? Please submit in the following format: YYYY/MM/DD HH:MM(e.g. 2019/01/31 23:59)',
        'order': 7
    },
    'Conference Start Date': {
        'description': 'What is the start date of conference itself? Please submit in the following format: YYYY/MM/DD (e.g. 2019/01/31)',
        'value-regex': '.*',
        'order': 8
    },
    'Conference Location': {
        'description': 'Where the conference is going to be held. For example: Amherst, Massachusetts, United States',
        'value-regex': '.*',
        'order': 9
    },
    'Paper Matching': {
        'description': 'Choose options for assigning papers to reviewers. If using the OpenReview Paper Matching System, see the top of the page for a description of each feature type.',
        'values-checkbox': [
            'Organizers will assign papers manually',
            'Reviewer Bid Scores',
            'Reviewer Recommendation Scores',
            'OpenReview Affinity',
            'TPMS',
            'Other (describe below)'
        ],
        'order': 10
    },
    'Author and Reviewer Anonymity': {
        'description': 'What policy best describes your anonymity policy? (Select "Other" if none apply, and describe your request below)',
        'value-radio': [
            'Double-blind',
            'Single-blind (Reviewers are anonymous)',
            'No anonymity',
            'Other (describe below)'
        ],
        'order': 11
    },
    'Open Reviewing Policy': {
        'description': 'Should submitted papers and/or reviews be visible to the public? (This is independent of anonymity policy)',
        'value-radio': [
            'Submissions and reviews should both be public.',
            'Submissions should be public, but reviews should be private.',
            'Submissions and reviews should both be private.',
            'Other (describe below)'
        ],
        'order': 12
    },
    'Public Commentary': {
        'description': 'Would you like to allow members of the public to comment on papers?',
        'value-radio': [
            'Yes, allow members of the public to comment anonymously.',
            'Yes, allow members of the public to comment non-anonymously.',
            'No, do not allow public commentary.',
            'Other (describe below)'
        ],
        'order': 13
    },
    'Other Important Information': {
        'value-regex': '[\\S\\s]{1,5000}',
        'description': 'Please use this space to clarify any questions above for which you responded "Other", and to clarify any other information that you think we may need.',
        'order': 14
    },
    'How did you hear about us?': {
        'value-regex': '.*',
        'description': 'Please briefly describe how you heard about OpenReview.',
        'order': 15
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
            'values': ['OpenReview.net/Support'],
        },
        'signatures': {
            'values-regex': '~.*'
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

revision_inv = client.post_invitation(openreview.Invitation(**{
    'id': 'OpenReview.net/Support/-/Revision',
    'readers': ['everyone'],
    'writers': [],
    'signatures': ['OpenReview.net/Support'],
    'invitees': ['everyone'],
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
        'content': request_content
    }
}))

deploy_content = {'conference_id': {
    'value-regex': '.*', 'description': 'Conference id'}}

admin_revision_inv = client.post_invitation(openreview.Invitation(**{
    'id': 'OpenReview.net/Support/-/Deploy',
    'readers': ['everyone'],
    'writers': [],
    'signatures': ['OpenReview.net/Support'],
    'invitees': ['OpenReview.net/Support'],
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
        'content': deploy_content
    }
}))

client.post_invitation(request_inv)
client.post_invitation(revision_inv)
client.post_invitation(admin_revision_inv)
