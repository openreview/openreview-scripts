import argparse
import openreview

parser = argparse.ArgumentParser()
parser.add_argument('--baseurl', help="base url")
parser.add_argument('--username')
parser.add_argument('--password')
args = parser.parse_args()

client = openreview.Client(baseurl=args.baseurl, username=args.username, password=args.password)

service_requests = client.post_group(openreview.Group(**{
    'id': 'OpenReview.net/Service',
    'readers': ['everyone'],
    'writers': [],
    'signatures': ['OpenReview.net'],
    'signatories': [],
    'members': [],
    'web': './serviceRequestsWeb.js'
}))

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
        'required': True
    },
    'Abbreviated Conference Name': {
        'description': 'Please include the year as well. This will be used to identify your conference on OpenReview and in email subject lines. Example: "ICLR 2019"',
        'value-regex': '.*',
        'required': True
    },
    'Official Website URL': {
        'description': 'Please provide the official website URL of the conference.',
        'value-regex': '.*',
        'required': True
    },
    'Contact Emails': {
        'description': 'Please provide the email addresses of all the Program Chairs or Organizers (comma-separated)',
        'values-regex': '.*',
        'required': True
    },
    'Requested Services': {
        'description': 'Which of OpenReview\'s services are you requesting?',
        'values-checkbox': [
            'Peer Review Management',
            'OpenReview Paper Matching System',
            'Other (describe below)'
        ],
        'required': True
    },
    'Area Chairs (Metareviewers)': {
        'description': 'Does your conference have Area Chairs?',
        'value-radio': [
            'Yes, our conference has Area Chairs',
            'No, our conference does not have Area Chairs',
            'Other (describe below)'
        ],
        'required': True
    },
    'Submission Start Date': {
        'description': 'When would you (ideally) like to have your OpenReview submission portal opened? Please submit in the following format: YYYY/MM/DD (e.g. 2019/01/31). (Skip this if only requesting paper matching service)',
        'value-regex': '.*',
    },
    'Submission Deadline': {
        'value-regex': '.*',
        'description': 'By when do authors need to submit their manuscripts? Please submit in the following format: YYYY/MM/DD (e.g. 2019/01/31)',
    },
    'Conference Start Date': {
        'description': 'What is the start date of conference itself? Please submit in the following format: YYYY/MM/DD (e.g. 2019/01/31)',
        'value-regex': '.*'
    },
    'Peer Review Management': {
        'description': 'Select the peer review management options you would like to include for your conference. Leave this section blank if you do not wish to use our peer review management service. See the top of the page for a description of each option.',
        'values-checkbox': [
            'Reviewer Recruitment by Email',
            'Reviewer Bidding for Papers',
            'Reviewer Recommendations',
            'Other (describe below)'
        ]
    },
    'Paper Matching': {
        'description': 'Choose options for assigning papers to reviewers. If using the OpenReview Paper Matching System, see the top of the page for a description of each feature type.',
        'values-checkbox': [
            'OpenReview Affinity',
            'TPMS',
            'Reviewer Bid Scores',
            'Reviewer Recommendation Scores',
            'Organizers will assign papers manually',
            'Other (describe below)'
        ]
    },
    'Author and Reviewer Anonymity': {
        'description': 'What policy best describes your anonymity policy? (Select "Other" if none apply, and describe your request below)',
        'value-radio': [
            'Double-blind',
            'Single-blind (Reviewers are anonymous)',
            'No anonymity',
            'Other (describe below)'
        ]
    },
    'Open Reviewing Policy': {
        'description': 'Should submitted papers and/or reviews be visible to the public? (This is independent of anonymity policy)',
        'value-radio': [
            'Submissions and reviews should both be public.',
            'Submissions should be public, but reviews should be private.',
            'Submissions and reviews should both be private.',
            'Other (describe below)'
        ]
    },
    'Public Commentary': {
        'description': 'Would you like to allow members of the public to comment on papers?',
        'value-radio': [
            'Yes, allow members of the public to comment anonymously.',
            'Yes, allow members of the public to comment non-anonymously.',
            'No, do not allow public commentary.',
            'Other (describe below)'
        ]
    },
    'Other Important Information': {
        'value-regex': '[\\S\\s]{1,5000}',
        'description': 'Please use this space to clarify any questions above for which you responded "Other", and to clarify any other information that you think we may need.'
    },
    'How did you hear about us?': {
        'value-regex': '.*',
        'description': 'Please briefly describe how you heard about OpenReview.'
    }
}

request_inv = client.post_invitation(openreview.Invitation(**{
    'id': 'OpenReview.net/Service/-/Request_Form',
    'readers': ['everyone'],
    'writers': [],
    'signatures': ['OpenReview.net/Service'],
    'invitees': ['everyone'],
    'process': 'serviceProcess.js',
    'reply': {
        'readers': {
            'values-copied': ['OpenReview.net', '{content["Program Chair Emails"]}']
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
