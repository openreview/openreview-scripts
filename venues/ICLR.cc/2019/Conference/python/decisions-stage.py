'''

'''

import argparse
import openreview
import iclr19
import invitations
import notes


def send_email(client, recipients, number, title, decision):

    message = '''
Dear Author,

We are pleased to inform you that your ICLR 2019 submission {number} - {title} has been accepted as a poster presentation.

You should now prepare the deanonymised camera ready version of your contribution, which should include inserting the statement \iclrfinalcopy in your LaTeX source file.

We ask that you update your paper on OpenReview with this latest version no later than February 23th, 2019.

https://openreview.net/group?id=ICLR.cc/2019/Conference

Please don't forget to make your travel arrangements. Registration for the conference will open on February 1, 2019, and you can register directly through the conference website https://iclr.cc/. There, you will also find suggestions for local accommodation.

Note that at least one author for each paper must be registered for ICLR 2019.

We received 1581 submissions! Out of these we accepted only 24 conference submissions for oral presentation (1.5%) and  501 conference submissions for poster presentation in the Conference Track (31%).

Congratulations and thank you for your contribution.

We look forward to seeing you in New Orleans!

Alexander, Karen, Sergey, and Shakir -- the ICLR 2019 program committee
'''.format(number = number, title = title)

    client.send_mail(subject = 'ICLR 2019 Decisions', recipients = recipients, message = message)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--baseurl', help="base url")
    parser.add_argument('--username')
    parser.add_argument('--password')
    args = parser.parse_args()

    client = openreview.Client(baseurl=args.baseurl, username=args.username, password=args.password)

    print('Update invitations...')
    decision_invitation = openreview.Invitation(
        id = iclr19.CONFERENCE_ID + '/-/Decision',
        readers = ['everyone'],
        writers = [iclr19.CONFERENCE_ID],
        invitees = [],
        signatures = [iclr19.CONFERENCE_ID],
        multiReply = True,
        reply = {
            'forum': None,
            'replyto': None,
            'invitation': iclr19.BLIND_SUBMISSION_ID,
            'readers': {
                'description': 'The users who will be allowed to read the above content.',
                'values': ['everyone']
            },
            'signatures': {
                'description': 'How your identity will be displayed with the above content.',
                'values': [iclr19.CONFERENCE_ID]
            },
            'content': {
                'tag': {
                    'order': 2,
                    'value-dropdown': [
                        'Oral',
                        'Poster',
                        'Reject'
                    ],
                    'required': True
                }
            }
        }
    )

    client.post_invitation(decision_invitation)

    # meta_reviews_invitations = list(openreview.tools.iterget_invitations(client, regex = 'ICLR.cc/2019/Conference/-/Paper.*/Meta_Review'))
    # for i in meta_reviews_invitations:
    #     i.reply['readers']['values'] = ['everyone']
    #     client.post_invitation(i)

    submissions = list(openreview.tools.iterget_notes(client, invitation = 'ICLR.cc/2019/Conference/-/Blind_Submission', details = 'original'))
    submissions_dict = {}
    for s in submissions:
        submissions_dict[s.id] = s

    meta_reviews = list(openreview.tools.iterget_notes(client, invitation = 'ICLR.cc/2019/Conference/-/Paper.*/Meta_Review'))

    #Post decisions
    print('Post decisions...')
    decisions = []
    for m in meta_reviews:
        if m.forum in submissions_dict:
            submission = submissions_dict[m.forum]
            tag = 'Reject'
            if 'Oral' in m.content['recommendation']:
                tag = 'Oral'
            if 'Poster' in m.content['recommendation']:
                tag = 'Poster'
            decision_tag = openreview.Tag(
                invitation = decision_invitation.id,
                forum = submission.forum,
                replyto = submission.forum,
                signatures = [iclr19.CONFERENCE_ID],
                readers = ['everyone'],
                tag = tag)
            decisions.append(client.post_tag(decision_tag))

            m.readers = ['everyone']
            if m.content['recommendation'] == 'Invite to Workshop Track':
                m.content['recommendation'] = 'Reject'
            client.post_note(m)


    # Release authors names
    print('Release author names...')
    for m in decisions:
        decision = m.tag
        submission = submissions_dict[m.forum]
        original_note = openreview.Note.from_json(submission.details['original'])
        if 'Reject' in decision:
            accepted = False

        if decision in ['Oral', 'Poster']:
            accepted = True

        overwriting_note = openreview.Note(
            id = submission.id,
            original = submission.original,
            invitation = iclr19.BLIND_SUBMISSION_ID,
            forum = submission.forum,
            signatures = [iclr19.CONFERENCE_ID],
            writers = [iclr19.CONFERENCE_ID],
            readers = ['everyone'],
            content = {
                '_bibtex': openreview.tools.get_bibtex(
                    original_note,
                    'International Conference on Learning Representations',
                    '2019',
                    url_forum=submission.forum,
                    accepted=accepted,
                    anonymous=False)
                })
        client.post_note(overwriting_note)

        revision_invitation = client.get_invitation(id = '{conference_id}/-/Paper{number}/Revision'.format(conference_id = iclr19.CONFERENCE_ID, number = submission.number))
        revision_invitation.expdate = 1576843200000
        client.post_invitation(revision_invitation)

    # Update home page
    print('update home page...')
    home_group = client.get_group(iclr19.CONFERENCE_ID)
    with open('../webfield/conferenceWebfield_decision_tabs.js') as f:
        content = f.read()
        home_group.web = content
        client.post_group(home_group)

    # Send emails to authors
    print('Send emails to authors...')
    for m in decisions:
        decision = m.tag
        submission = submissions_dict[m.forum]
        original_note = openreview.Note.from_json(submission.details['original'])
        send_email(client, original_note.content['authorids'], original_note.number, original_note.content['title'], decision)

