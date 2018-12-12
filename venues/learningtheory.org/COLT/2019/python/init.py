import argparse
import openreview
import datetime
import os
import config

if __name__ == '__main__':
    ## Argument handling
    parser = argparse.ArgumentParser()
    parser.add_argument('--baseurl', help="base url")
    parser.add_argument('--username')
    parser.add_argument('--password')
    args = parser.parse_args()

    client = openreview.Client(baseurl=args.baseurl, username=args.username, password=args.password)
    conference = config.get_conference(client)
    conference.open_submissions(
        due_date = datetime.datetime(2019, 2, 1, 18, 00),
        public = True,
        additional_fields = {
            'STOC_id': {
                'description': 'If this submission (or its earlier version) is currently under consideration at STOC 2019, please enter its STOC identification number.',
                'values-regex': '.*',
                'required': False
            }
        }
    )

    # Create super invitation
    recruit_invitation = openreview.Invitation(
        id = 'learningtheory.org/COLT/2019/Conference/-/Recruit_Reviewers',
        readers = ['everyone'],
        writers = ['learningtheory.org/COLT/2019/Conference'],
        signatures = ['learningtheory.org/COLT/2019/Conference'],
        process = '../process/recruitReviewersProcess.js',
        web = '../webfield/recruitResponseWebfield.js',
        reply = {
            'forum': None,
            'replyto': None,
            'readers': {
                'values': ['~Super_User1']
            },
            'signatures': {
                'values-regex': '\\(anonymous\\)'
            },
            'writers': {
                'values': []
            },
            'content': {
                'title': {
                    'order': 1,
                    'value': 'Invitation to review response'
                },
                'email': {
                    'description': 'email address',
                    'order': 2,
                    'value-regex': '.*@.*',
                    'required':True
                },
                'key': {
                    'description': 'Email key hash',
                    'order': 3,
                    'value-regex': '.{0,100}',
                    'required':True
                },
                'response': {
                    'description': 'Invitation response',
                    'order': 4,
                    'value-radio': ['Yes', 'No'],
                    'required':True
                }
            }
        })
    recruit_invitation = client.post_invitation(recruit_invitation)

    conference.set_program_chairs(emails=[])
    area_chairs = conference.set_area_chairs(emails=[])
    with open(os.path.abspath('../webfield/programCommitteeWebfield.js')) as f:
        area_chairs.web = f.read()
        area_chairs.signatories.append(area_chairs.id)
        client.post_group(area_chairs)
    print('DONE.')
