import config
import argparse
import openreview
import datetime
from Crypto.Hash import HMAC, SHA256
hash_seed = "1234"


def post_blind_note(client, original_note, conference):
    blind_note = openreview.Note(
        original= original_note.id,
        invitation= conference.id + '/-/Blind_Submission',
        forum= None,
        signatures= [conference.id],
        writers= [conference.id],
        readers= ['everyone'],
        content= {
            "authors": ['Anonymous'],
            "authorids": [],
            "_bibtex": None
        })

    paper_group_id = conference.id + "/Paper{}".format(original_note.number)
    author_group_id = conference.id + "/Paper{}/Authors".format(original_note.number)

    blind_note.content = {
        "authors": ['Anonymous'],
        "authorids": [author_group_id],
    }

    return client.post_note(blind_note)

if __name__ == '__main__':
    ## Argument handling
    parser = argparse.ArgumentParser()
    parser.add_argument('--baseurl', help="base url")
    parser.add_argument('--username')
    parser.add_argument('--password')
    args = parser.parse_args()

    client = openreview.Client(baseurl=args.baseurl, username=args.username, password=args.password)
    conference = config.get_conference(client)


    official_review_template = {
        'id': conference.id + '/-/Paper<number>/Official_Review',
        'readers': ['everyone'],
        'writers': [conference.id],
        'invitees': [conference.id + '/Paper<number>/Reviewers'],
        'noninvitees': [],
        'signatures': [conference.id],
        'duedate': openreview.tools.timestamp_GMT(year=2019, month=2, day=25),
        'multiReply': False,
        'reply': {
            'forum': '<forum>',
            'replyto': '<forum>',
            'readers': {
                'description': 'The users who will be allowed to read the reply content.',
                'values': [
                    conference.id + '/Paper<number>/Program_Committee',
                    conference.id + '/Program_Chairs'
                    ]
            },
            'signatures': {
                'description': 'How your identity will be displayed with the above content.',
                'values-regex': conference.id + '/Paper<number>/AnonReviewer[0-9]+'
            },
            'writers': {
                'description': 'Users that may modify this record.',
                'values-copied':  [
                    conference.id,
                    '{signatures}'
                ]
            },
            'content': openreview.invitations.content.review
        }
    }

    program_committee_member = 'ebrun@cs.stanford.edu'

    # Create paper groups and assign them to a program committee
    for n in openreview.tools.iterget_notes(client, invitation = conference.get_submission_id()):
        print('n.id', n.id)
        pc_group_id = "{conference_id}/Paper{number}/Program_Committee".format(conference_id = conference.get_id(), number = n.number)
        papergroup_id = "{conference_id}/Paper{number}".format(conference_id = conference.get_id(), number = n.number)
        group_id = "{conference_id}/Paper{number}/Reviewers".format(conference_id = conference.get_id(), number = n.number)
        group_invited_id = "{conference_id}/Paper{number}/Reviewers/Invited".format(conference_id = conference.get_id(), number = n.number)
        group_declined_id = "{conference_id}/Paper{number}/Reviewers/Declined".format(conference_id = conference.get_id(), number = n.number)

        client.post_group(openreview.Group(id = papergroup_id,
                                        readers = [conference.get_id(), pc_group_id],
                                        writers = [conference.get_id(), pc_group_id],
                                        signatures = [conference.get_id()],
                                        signatories = []))
        client.post_group(openreview.Group(id = group_id,
                                        readers = [group_id, conference.get_id(), pc_group_id],
                                        writers = [conference.get_id(), pc_group_id],
                                        signatures = [conference.get_id()],
                                        signatories = [group_id]))
        client.post_group(openreview.Group(id = group_invited_id,
                                        readers = [conference.get_id(), pc_group_id],
                                        writers = [conference.get_id(), pc_group_id],
                                        signatures = [conference.get_id()],
                                        signatories = [conference.get_id()]))
        client.post_group(openreview.Group(id = group_declined_id,
                                        readers = [conference.get_id(), pc_group_id],
                                        writers = [conference.get_id(), pc_group_id],
                                        signatures = [conference.get_id()],
                                        signatories = [conference.get_id()]))

        blind_note = post_blind_note(client, n, conference)

        official_review_invitation = client.post_invitation(
            openreview.Invitation.from_json(
                openreview.tools.fill_template(official_review_template, blind_note)
            )
        )

        print(official_review_invitation.id)

        result = openreview.tools.assign(
            client=client,
            conference=conference.get_id(),
            paper_number=n.number,
            reviewer_to_add=program_committee_member,
            parent_label = 'Program_Committee',
            individual_label = 'Program_Committee_Member',
            individual_group_params = {
                'readers': [
                    conference.get_id(),
                    conference.get_program_chairs_id(),
                    'learningtheory.org/COLT/2019/Conference/Paper{0}/Program_Committee'.format(n.number)
                ],
                'signatories': ['learningtheory.org/COLT/2019/Conference/Paper{0}/Program_Committee'.format(n.number)]
                },
            parent_group_params = {
                'readers': [
                    conference.get_id(),
                    conference.get_program_chairs_id(),
                        'learningtheory.org/COLT/2019/Conference/Paper{0}/Program_Committees'.format(n.number)
                ],
                'signatories': ['learningtheory.org/COLT/2019/Conference/Paper{0}/Program_Committee'.format(n.number)]
            })

        print('result', result)
    print('DONE.')
