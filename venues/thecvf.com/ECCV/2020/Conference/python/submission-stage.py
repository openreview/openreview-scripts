import openreview
import argparse

if __name__ == '__main__':
    ## Argument handling
    parser = argparse.ArgumentParser()
    parser.add_argument('--baseurl', help="base url")
    parser.add_argument('--username')
    parser.add_argument('--password')
    args = parser.parse_args()

    client = openreview.Client(baseurl=args.baseurl, username=args.username, password=args.password)

    conference = openreview.helpers.get_conference(client, 'Skx6tVahYB')

    ## Anonymize current submissions
    conference.create_blind_submissions()

    ## Setup paper groups
    conference.set_authors()
    conference.set_reviewers()
    conference.set_area_chairs()

    ## Create withdraw invitations
    conference.create_withdraw_invitations()

    ## Create desk reject invitations
    conference.create_desk_reject_invitations()

    ## Create reference invitation to upload video/appendix pdf
    submissions = conference.get_submissions()
    for submission in submissions:
        id = conference.get_invitation_id('Supplementary_Material', submission.number)
        invitation = openreview.Invitation(
            id = id,
            duedate = None, # TODO: define duedate
            readers = ['everyone'],
            writers = [conference.id],
            signatures = [conference.id],
            invitees = [conference.get_authors_id(number=submission.number)],
            reply = {
                'forum': submission.original,
                'referent': submission.original,
                'readers': {
                    'values': submission.readers
                },
                'writers': {
                    'values': submission.writers
                },
                'signatures': {
                    'values-regex': '~.*'
                },
                'content': {
                    'video': {
                        'order': 1,
                        'required': False,
                        'description': 'TODO: add description',
                        'value-file': {
                            'fileTypes': [
                                'mov',
                                'mp4',
                                'zip'
                            ],
                            'size': 50
                        }
                    },
                    'appendix': {
                        'order': 2,
                        'required': False,
                        'description': 'TODO: add description',
                        'value-file': {
                            'fileTypes': [
                                'pdf'
                            ],
                            'size': 50
                        }
                    }
                }
            }
        )
        client.post_invitation(invitation)