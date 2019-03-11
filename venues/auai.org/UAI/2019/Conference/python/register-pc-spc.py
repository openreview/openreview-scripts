import argparse
import openreview
import openreview.tools as tools
import datetime
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

    subj_desc = 'To properly assign papers to reviewers, we ask that reviewers provide their areas of expertise from among the provided list of subject areas. Please submit your areas of expertise by selecting the appropriate options from the "Subject Areas" list.\n\n'

    coi_desc = 'In order to avoid conflicts of interest in reviewing, we ask that all reviewers take a moment to update their OpenReview profiles with their latest information regarding work history and professional relationships. After you have updated your profile, please confirm that your OpenReview profile is up-to-date by selecting yes in the "Profile Confirmed" section.\n\n'

    tpms_desc = 'In addition to subject areas, we will be using the Toronto Paper Matching System (TPMS) to compute paper-reviewer affinity scores. Please take a moment to sign up for TPMS and/or update your TPMS account with your latest papers. Then, please ensure that the email address that is affiliated with your TPMS account is linked to your OpenReview profile. After you have done this, please confirm that your TPMS account is up-to-date by selecting yes in the "TPMS Account Confirmed" section.\n\n'

    registration_parent_invitation = client.post_invitation(openreview.Invitation(
        id = conference.get_id() + '/-/Parent/Registration',
        readers = ['everyone'],
        writers = [conference.get_id()],
        signatures = [conference.get_id()],
        invitees = [conference.get_area_chairs_id(), conference.get_reviewers_id() ],
        reply = {
            'forum': None,
            'replyto': None,
            'readers': {'values': [conference.get_area_chairs_id(), conference.get_reviewers_id() ]},
            'writers': {'values': [conference.get_id()]},
            'signatures': {'values': [conference.get_id()]},
            'content': {
                'title': {'value': 'UAI 2019 Registration'},
                'Subject Areas': {
                    'value': subj_desc,
                    'order': 1
                },
                'Profile Confirmed': {
                    'value': coi_desc,
                    'order': 2
                },
                'TPMS Account Confirmed': {
                    'value': tpms_desc,
                    'order': 3
                }
            }
        }
    ))

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
                'TPMS Account Confirmed': registration_parent_invitation.reply['content']['TPMS Account Confirmed']['value'],
            }
        })

    registration_parent = client.post_note(openreview.Note(**registration_parent_json))
    print ('posted :', registration_parent.id)
    # registration invitation
    
    registration_invitation = client.post_invitation(openreview.Invitation(
        id = conference.get_id() + '/-/Registration',
        duedate = tools.datetime_millis(datetime.datetime(2019, 3, 16, 10, 59)),
        expdate = tools.datetime_millis(datetime.datetime(2019, 3, 16, 10, 59)),
        readers = ['everyone'],
        writers = [conference.get_id()],
        signatures = [conference.get_id()],
        invitees = [
            conference.get_reviewers_id(),
            conference.get_area_chairs_id()],
        reply = {
            'forum': registration_parent.id,
            'replyto': registration_parent.id,
            'readers': {
                'description': 'Users who can read this',
                'values-copied': [
                    conference.get_id(),
                    '{signatures}'
                ]
            },
            'writers': {
                'description': 'How your identity will be displayed.',
                'values-copied': [
                    conference.get_id(),
                    '{signatures}'
                ]
            },
            'signatures': {
                'description': 'How your identity will be displayed.',
                'values-regex': '~.*'
            },
            'content': {
                'title': {
                    'value': 'UAI 2019 Registration',
                    'order': 1
                },
                'Subject Areas': {
                    'values-dropdown': conference.get_subject_areas(),
                    'required': True,
                    'order': 2
                },
                'Profile Confirmed': {
                    'value-dropdown': ['Yes', 'No'],
                    'required': True,
                    'order': 3
                },
                'TPMS Account Confirmed': {
                    'value-dropdown': ['Yes', 'No'],
                    'required': True,
                    'order': 4
                }
            }
        }
    ))

    print (registration_invitation.id)

    conference.set_reviewerpage_header({
        'instructions': '<p class="dark">This page provides information and status updates \
            for UAI 2019 reviewers. It will be regularly updated as the conference progresses, \
            so please check the "Reviewer Schedule" and "Review Tasks" section frequently for news and other updates.</p>',
        'schedule': '<h4>Registration Phase</h4>\
        <p>\
            <em><strong>Please do the following by 23:59 PM Samoa Time, Friday, March 15 2019</strong></em>:\
            <ul>\
                <li>Update your profile to include your most up-to-date information, including work history and relations, to ensure proper conflict-of-interest detection during the paper matching process.</li> \
                <li>Complete the UAI 2019 registration form (found in your "Reviewer Tasks").</li>\
                <li>Register subject areas indicating your expertise (through UAI 2019 registration form).</li>\
            </ul>\
        </p><br>\
        <h4>Bidding Phase</h4>\
        <p>\
            <em><strong>Please note that the bidding has begun. You are requested to do the\
            following by 23:59 PM Samoa Time, March 15th 2019</strong></em>:\
            <ul>\
                <li>Provide your reviewing preferences by bidding on papers using the Bidding \
                Interface.</li>\
                <li><strong><a href="/invitation?id=auai.org/UAI/2019/Conference/-/Bid">Go to \
                Bidding Interface</a></strong></li>\
            </ul>\
        </p><br>'
    })
    conference.set_areachairpage_header({
        'instructions': '<p class="dark">This page provides information and status updates \
            for UAI 2019 area chairs. It will be regularly updated as the conference progresses, \
            so please check the "Area Chair Schedule" and "Area Chair Tasks" sections frequently for news and other updates.</p>',
        'schedule': '<h4>Registration Phase</h4>\
            <p>\
            <em><strong>Please do the following by 23:59 PM Samoa Time, Friday, March 15 2019</strong></em>:\
            <ul>\
                <li>Update your profile to include your most up-to-date information, including work history and relations, to ensure proper conflict-of-interest detection during the paper matching process.</li> \
                <li>Complete the UAI 2019 registration form (found in your "Area Chair Tasks").</li>\
                <li>Register subject areas indicating your expertise (through UAI 2019 registration form).</li>\
            </ul>\
            </p>\
        <br>\
        <h4>Bidding Phase</h4>\
            <p>\
            <em><strong>Please note that the bidding has begun. You are requested to do the\
            following by 23:59 PM Samoa Time, March 15th 2019</strong></em>:\
            <ul>\
                <li>Provide your reviewing preferences by bidding on papers using the Bidding \
                Interface.</li>\
                <li><strong><a href="/invitation?id=auai.org/UAI/2019/Conference/-/Bid">Go to \
                Bidding Interface</a></strong></li>\
            </ul>\
            </p>\
        <br>'
    })


