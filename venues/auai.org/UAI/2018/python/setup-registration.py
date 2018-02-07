import openreview
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--baseurl', help="base URL")
parser.add_argument('--username')
parser.add_argument('--password')

args = parser.parse_args()

client = openreview.Client(baseurl=args.baseurl, username=args.username, password=args.password)
print 'connecting to {0}'.format(client.baseurl)

subj_desc = ''.join([
    'To properly assign papers to reviewers, we ask that reviewers provide their areas ',
    'of expertise from among the provided list of subject areas. ',
    'Please submit your areas of expertise by clicking on the "Subject Areas" button below.',
    '\n\n'
    ])

coi_desc = ''.join([
    'In order to avoid conflicts of interest in reviewing, we ask that all reviewers take a moment to ',
    'update their OpenReview profiles with their latest information regarding work history and professional relationships. ',
    'After you have updated your profile, please confirm that your profile is up-to-date by clicking on ',
    'the "Profile Confirmed" button below.',
    '\n\n'
    ])

data_consent_desc = ''.join([
    'One of the missions of OpenReview is to enable the study of the scientific peer review process itself. ',
    'In accordance with that mission, OpenReview is collecting a dataset of peer reviews and ',
    'discussions between authors and reviewers for research purposes. ',
    'This dataset will include the contents of peer reviews and comments between authors, reviewers, and area chairs. ',
    'The dataset will be anonymized, and will not include your true identity, but may include non-identifiable metadata related to your profile (e.g. years of experience, field of expertise). ',
    'The dataset may be released to the public domain ',
    'after the final accept/reject decisions are made. ',
    'Do you agree to having your reviews and comments included in this dataset? ',
    'Please indicate your response by clicking on the "Consent Response" button below. ',
    '\n\n'
    ])

registration_parent_invitation = client.post_invitation(openreview.Invitation(**{
    'id': 'auai.org/UAI/2018/-/Registration',
    'readers': ['everyone'],
    'writers': ['auai.org/UAI/2018'],
    'signatures': ['auai.org/UAI/2018'],
    'invitees': ['auai.org/UAI/2018'],
    'reply': {
        'forum': None,
        'replyto': None,
        'readers': {'values': ['auai.org/UAI/2018/Program_Committee']},
        'writers': {'values': ['auai.org/UAI/2018']},
        'signatures': {'values': ['auai.org/UAI/2018']},
        'content': {
            'title': {'value': 'UAI 2018 Registration'},
            'subject areas': {
                'value': subj_desc,
                'order': 1
            },
            'conflicts of interest': {
                'value': coi_desc,
                'order': 2
            },
            'data consent': {
                'value': data_consent_desc,
                'order': 9
            }
        }
    }
}))

existing_reg_parents = client.get_notes(invitation=registration_parent_invitation.id)

if existing_reg_parents:
    registration_parent_json = existing_reg_parents[0].to_json()
else:
    registration_parent_json = {}

registration_parent_json.update({
        'invitation': registration_parent_invitation.id,
        'readers': registration_parent_invitation.reply['readers']['values'],
        'writers': registration_parent_invitation.reply['writers']['values'],
        'signatures': registration_parent_invitation.reply['signatures']['values'],
        'replyto': None,
        'forum': None,
        'content': {
            'title': registration_parent_invitation.reply['content']['title']['value'],
            'subject areas': registration_parent_invitation.reply['content']['subject areas']['value'],
            'conflicts of interest': registration_parent_invitation.reply['content']['conflicts of interest']['value'],
            'data consent': registration_parent_invitation.reply['content']['data consent']['value']
        }
    })

registration_parent = client.post_note(openreview.Note(**registration_parent_json))

consent_response_invitation = client.post_invitation(openreview.Invitation(**{
    'id': 'auai.org/UAI/2018/-/Registration/Consent/Response', # I would like for this to be Consent_Response, but right now the prettyId function is taking the last TWO segments. It should only take the last.
    'readers': ['everyone'],
    'writers': ['auai.org/UAI/2018'],
    'signatures': ['auai.org/UAI/2018'],
    'invitees': ['auai.org/UAI/2018/Program_Committee'],
    'duedate': 0,
    'process': '../process/registrationProcess.js',
    'reply': {
        'forum': registration_parent.id,
        'replyto': registration_parent.id,
        'readers': {'values': ['auai.org/UAI/2018']},
        'writers': {'values-regex': '~.*'},
        'signatures': {'values-regex': '~.*'},
        'content': {
            'title': {'value': 'Consent Form Response'},
            'consent': {
                'value-dropdown': [
                    'Yes, I agree to participate.',
                    'No, I do not agree to participate.'
                ],
                'required': True,
            }
        }
    }
}))

with open('../data/subject_areas.csv') as f:
    subject_areas = f.read().split(',\n')

subj_response_invitation = client.post_invitation(openreview.Invitation(**{
    'id': 'auai.org/UAI/2018/-/Registration/Subject/Areas', # same here, see comment above
    'readers': ['everyone'],
    'writers': ['auai.org/UAI/2018'],
    'signatures': ['auai.org/UAI/2018'],
    'invitees': ['auai.org/UAI/2018/Program_Committee'],
    'duedate': 0,
    'process': '../process/registrationProcess.js',
    'reply': {
        'forum': registration_parent.id,
        'replyto': registration_parent.id,
        'readers': {'values': ['auai.org/UAI/2018']},
        'writers': {'values-regex': '~.*'},
        'signatures': {'values-regex': '~.*'},
        'content': {
            'title': {'value': 'Subject Area Response'},
            'subject_areas': {
                'values-dropdown': subject_areas,
                'required': True,
            }
        }
    }
}))

profile_confirmed_invitation = client.post_invitation(openreview.Invitation(**{
    'id': 'auai.org/UAI/2018/-/Registration/Profile/Confirmed',
    'readers': ['everyone'],
    'writers': ['auai.org/UAI/2018'],
    'signatures': ['auai.org/UAI/2018'],
    'invitees': ['auai.org/UAI/2018/Program_Committee'],
    'duedate': 0,
    'process': '../process/registrationProcess.js',
    'reply': {
        'forum': registration_parent.id,
        'replyto': registration_parent.id,
        'readers': {'values': ['auai.org/UAI/2018']},
        'writers': {'values-regex': '~.*'},
        'signatures': {'values-regex': '~.*'},
        'content': {
            'title': {'value': 'Profile Confirmed Response'},
            'confirmation': {
                'value': 'I confirm that I have updated my profile sufficiently to capture my conflicts of interest.',
                'required': True,
            }
        }
    }
}))
