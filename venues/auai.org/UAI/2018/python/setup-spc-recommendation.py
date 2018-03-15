'''
Set up the SPC recommendation widget
'''

import openreview
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--baseurl', help="base URL")
parser.add_argument('--username')
parser.add_argument('--password')

args = parser.parse_args()

client = openreview.Client(baseurl=args.baseurl, username=args.username, password=args.password)
print 'connecting to {0}'.format(client.baseurl)

blind_notes = client.get_notes(invitation='auai.org/UAI/2018/-/Blind_Submission')

for n in blind_notes:

    groupid = 'auai.org/UAI/2018/Paper{}/Area_Chairs'.format(n.number)

    client.post_invitation(openreview.Invitation(**{
        'id': 'auai.org/UAI/2018/-/Paper{}/Veto_Reviewer'.format(n.number),
        'invitees': [groupid],
        'multiReply': True,
        'readers': ['everyone'],
        'writers': ['auai.org/UAI/2018'],
        'signatures': ['auai.org/UAI/2018'],
        'reply': {
            'forum': n.id,
            'readers': {
                'description': 'The users who will be allowed to read the above content.',
                'values-copied': ['auai.org/UAI/2018', '{signatures}']
            },
            'signatures': {
                'description': 'How your identity will be displayed with the above content.',
                'values-regex': '~.*'
            },
            'content': {
                'tag': {
                    'description': 'Veto a reviewer from reviewing this paper',
                    'order': 1,
                    'required': True,
                    'values-url': '/groups?id=auai.org/UAI/2018/Program_Committee'
                }
            }
        }
    }))

    client.post_invitation(openreview.Invitation(**{
        'id': 'auai.org/UAI/2018/-/Paper{}/Recommend_Reviewer'.format(n.number),
        'invitees': [groupid],
        'multiReply': True,
        'readers': ['everyone'],
        'writers': ['auai.org/UAI/2018'],
        'signatures': ['auai.org/UAI/2018'],
        'reply': {
            'forum': n.id,
            'readers': {
                'description': 'The users who will be allowed to read the above content.',
                'values-copied': ['auai.org/UAI/2018', '{signatures}']
            },
            'signatures': {
                'description': 'How your identity will be displayed with the above content.',
                'values-regex': '~.*'
            },
            'content': {
                'tag': {
                    'description': 'Recommend a reviewer to review this paper',
                    'order': 1,
                    'required': True,
                    'values-url': '/groups?id=auai.org/UAI/2018/Program_Committee'
                }
            }
        }
    }))

    print groupid
