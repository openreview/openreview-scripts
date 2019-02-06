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

request_inv = client.post_invitation(openreview.Invitation(**{
    'id': 'OpenReview.net/Service/-/Request_Form',
    'readers': ['everyone'],
    'writers': [],
    'signatures': ['OpenReview.net/Service'],
    'invitees': ['everyone'],
    'reply': {
        'readers': {
            'values': ['OpenReview.net']
        },
        'writers': {
            'values-regex': '~.*',
        },
        'signatures': {
            'values-regex': '~.*'
        },
        'content': {
            'Name of contact': {
                'value-regex': '.*',
                'required': True
            },
            'Contact email': {
                'value-regex': '.*',
                'required': True
            },
            'Service requested': {
                'value-regex': '[\\S\\s]{1,5000}',
                'description': 'Please describe the type of service you are requesting (peer review, paper matching, both, etc.). Please include as much detail as possible.'
            },
            'Submission start date': {
                'value-regex': '.*',
                'description': 'When would you (ideally) like to have your OpenReview submission portal opened? (Skip this if only requesting paper matching service)'
            },
            'Submission deadline': {
                'value-regex': '.*',
            },
            'Other important dates': {
                'value-regex': '[\\S\\s]{1,5000}',
                'description': 'Please describe any other key dates that we should be aware of.'
            }

        }
    }
}))
