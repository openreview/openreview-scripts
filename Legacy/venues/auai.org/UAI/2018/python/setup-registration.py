import openreview
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--baseurl')
parser.add_argument('--username')
parser.add_argument('--password')
parser.add_argument('--invitees',
    nargs='*',
    default=['auai.org/UAI/2018'],
    help='enter all the group IDs that should be invited to complete the registration. \
    e.g. \'python setup-registration.py --invitees auai.org/UAI/2018/Program_Committee auai.org/UAI/2018/Senior_Program_Committee\'.\
    Defaults to auai.org/UAI/2018 (the admin account)')

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

tpms_desc = ''.join([
    'In addition to subject areas, we will be using the Toronto Paper Matching System (TPMS) to compute paper-reviewer affinity scores. ',
    'Please take a moment to sign up for TPMS and/or update your TPMS account with your latest papers. ',
    'Then, please ensure that the email address that is affiliated with your TPMS account is linked to your OpenReview profile. ',
    'After you have done this, please confirm that your TPMS account is up-to-date by clicking the "TPMS Account Confirmed" button below. ',
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
        'readers': {'values': args.invitees},
        'writers': {'values': ['auai.org/UAI/2018']},
        'signatures': {'values': ['auai.org/UAI/2018']},
        'content': {
            'title': {'value': 'UAI 2018 Registration'},
            'Subject Areas': {
                'value': subj_desc,
                'order': 1
            },
            'Profile Confirmed': {
                'value': coi_desc,
                'order': 2
            },
            'Consent Response': {
                'value': data_consent_desc,
                'order': 9
            },
            'TPMS Account Confirmed': {
                'value': tpms_desc,
                'order': 3
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
            'Subject Areas': registration_parent_invitation.reply['content']['Subject Areas']['value'],
            'Profile Confirmed': registration_parent_invitation.reply['content']['Profile Confirmed']['value'],
            'Consent Response': registration_parent_invitation.reply['content']['Consent Response']['value'],
            'TPMS Account Confirmed': registration_parent_invitation.reply['content']['TPMS Account Confirmed']['value'],
        }
    })

registration_parent = client.post_note(openreview.Note(**registration_parent_json))

consent_response_invitation = client.post_invitation(openreview.Invitation(**{
    'id': 'auai.org/UAI/2018/-/Registration/Consent/Response', # I would like for this to be Consent_Response, but right now the prettyId function is taking the last TWO segments. It should only take the last.
    'readers': ['everyone'],
    'writers': ['auai.org/UAI/2018'],
    'signatures': ['auai.org/UAI/2018'],
    'invitees': args.invitees,
    'duedate': 1520639999000, # March 9, 2018
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
    'invitees': args.invitees,
    'duedate': 1520639999000, # March 9, 2018,
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
    'invitees': args.invitees,
    'duedate': 1520639999000, # March 9, 2018,
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

tpms_confirmed_invitation = client.post_invitation(openreview.Invitation(**{
    'id': 'auai.org/UAI/2018/-/Registration/TPMS_Account/Confirmed',
    'readers': ['everyone'],
    'writers': ['auai.org/UAI/2018'],
    'signatures': ['auai.org/UAI/2018'],
    'invitees': args.invitees,
    'duedate': 1520639999000, # March 9, 2018,
    'process': '../process/registrationProcess.js',
    'reply': {
        'forum': registration_parent.id,
        'replyto': registration_parent.id,
        'readers': {'values': ['auai.org/UAI/2018']},
        'writers': {'values-regex': '~.*'},
        'signatures': {'values-regex': '~.*'},
        'content': {
            'title': {'value': 'TPMS Account Confirmed Response'},
            'confirmation': {
                'value': 'I confirm that I have signed up and/or updated my TPMS account with my latest publications, and that I have linked the email affiliated with my TPMS account to my OpenReview profile.',
                'required': True,
            }
        }
    }
}))
