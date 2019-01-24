import argparse
import openreview
from openreview import invitations
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
        due_date = datetime.datetime(2019, 2, 2, 4, 00),
        public = False,
        additional_fields = {
            'STOC_id': {
                'description': 'If this submission (or its earlier version) is currently under consideration at STOC 2019, please enter its STOC identification number.',
                'values-regex': '.*',
                'required': False
            },
            'dual_submission': {
                'value-checkbox': 'This work is a short version of an unpublished paper that has been submitted to a journal.'
            },
            'student_submission': {
                'value-checkbox': 'The primary contributor is a full-time student at the time of submission.'
            }
        },
        additional_readers = [conference.get_area_chairs_id(), conference.get_program_chairs_id()]
    )

    # Create blind subission invitation
    client.post_invitation(invitations.Submission(
        id = conference.id + '/-/Blind_Submission',
        conference_id = conference.id,
        duedate = openreview.tools.timestamp_GMT(year=2019, month=2, day=1, hour=9),
        mask = {
            'authors': {
                'values': ['Anonymous']
            },
            'authorids': {
                'values-regex': '.*'
            }
        },
        reply_params = {
            'signatures': {
                'values': [conference.id]},
            'readers': {
                'values': ['everyone']
            }
        }
    ))

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

    program_chair_group = conference.set_program_chairs(emails=[])
    with open('../webfield/programChairWebfield.js') as f:
        program_chair_group.web = f.read()
        client.post_group(program_chair_group)

    area_chairs_group = conference.set_area_chairs(emails=[])
    with open(os.path.abspath('../webfield/programCommitteeWebfield_init.js')) as f:
        area_chairs_group.web = f.read()
        area_chairs_group.signatories.append(area_chairs_group.id)
        client.post_group(area_chairs_group)

    authors_group = client.get_group(conference.get_authors_id())
    with open(os.path.abspath('../webfield/authorWebfield.js')) as f:
        authors_group.web = f.read()
        client.post_group(authors_group)

    conference_group = client.get_group(conference.get_id())
    with open(os.path.abspath('../webfield/homepage.js')) as f:
        conference_group.web = f.read()
        client.post_group(conference_group)

    print('DONE.')
