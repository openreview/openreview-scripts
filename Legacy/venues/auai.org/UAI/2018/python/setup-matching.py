import openreview
import openreview_matcher
import random
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--baseurl', help="base URL")
parser.add_argument('--username')
parser.add_argument('--password')

args = parser.parse_args()

client = openreview.Client(baseurl=args.baseurl, username=args.username, password=args.password)
print 'connecting to {0}'.format(client.baseurl)

metadata_inv = client.post_invitation(openreview.Invitation(**{
    'id': 'auai.org/UAI/2018/-/Paper_Metadata',
    'readers': [
        'auai.org/UAI/2018',
        'auai.org/UAI/2018/Program_Chairs',
        'auai.org/UAI/2018/Program_Committee',
        'auai.org/UAI/2018/Senior_Program_Committee'
    ],
    'writers': ['auai.org/UAI/2018'],
    'signatures': ['auai.org/UAI/2018'],
    'reply': {
        'forum': None,
        'replyto': None,
        'invitation': 'auai.org/UAI/2018/-/Blind_Submission',
        'readers': {'values': [
            'auai.org/UAI/2018',
            'auai.org/UAI/2018/Program_Chairs',
            'auai.org/UAI/2018/Program_Committee',
            'auai.org/UAI/2018/Senior_Program_Committee'
            ]},
        'writers': {'values': ['auai.org/UAI/2018']},
        'signatures': {'values': ['auai.org/UAI/2018']},
        'content': {}
    }
}))


print "posting assignment invitation..."
assignment_inv = client.post_invitation(openreview.Invitation(**{
    'id': 'auai.org/UAI/2018/-/Paper_Assignment',
    'readers': [
        'auai.org/UAI/2018',
        'auai.org/UAI/2018/Program_Chairs',
        'auai.org/UAI/2018/Program_Committee',
        'auai.org/UAI/2018/Senior_Program_Committee'
    ],
    'writers': ['auai.org/UAI/2018'],
    'signatures': ['auai.org/UAI/2018'],
    'reply': {
        'forum': None,
        'replyto': None,
        'invitation': 'auai.org/UAI/2018/-/Blind_Submission',
        'readers': {'values': [
            'auai.org/UAI/2018',
            'auai.org/UAI/2018/Program_Chairs',
            'auai.org/UAI/2018/Program_Committee',
            'auai.org/UAI/2018/Senior_Program_Committee']
        },
        'writers': {'values': ['auai.org/UAI/2018']},
        'signatures': {'values': ['auai.org/UAI/2018']},
        'content': {
            # assignment
            # label
        }
    }
}))

print "posting configuration invitation..."
config_inv = client.post_invitation(openreview.Invitation(**{
    'id': 'auai.org/UAI/2018/-/Assignment_Configuration',
    'readers': [
        'auai.org/UAI/2018',
        'auai.org/UAI/2018/Program_Chairs'
    ],
    'writers': [
        'auai.org/UAI/2018'
    ],
    'signatures': ['auai.org/UAI/2018'],
    'reply': {
        'forum': None,
        'replyto': None,
        'invitation': None,
        'readers': {'values': [
            'auai.org/UAI/2018',
            'auai.org/UAI/2018/Program_Chairs'
        ]},
        'writers': {'values': ['auai.org/UAI/2018']},
        'signatures': {'values': ['auai.org/UAI/2018']},
        'content': {
            # label = label
            # configuration = configuration
            # paper_invitation = 'auai.org/UAI/2018/-/Blind_Submission'
            # metadata_invitation = 'auai.org/UAI/2018/-/Paper_Metadata'
            # assignment_invitation = 'auai.org/UAI/2018/-/Paper_Assignment'
            # match_group = 'auai.org/UAI/2018/Program_Committee'
            # statistics = {fill in later}
        }
    }

}))
