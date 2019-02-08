import openreview
import config
import argparse


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
        'invitees': [
            conference.id + '/Paper<number>/Reviewers', 
            conference.id + '/Paper<number>/Program_Committee'],
        'noninvitees': [],
        'signatures': [conference.id],
        'duedate': openreview.tools.timestamp_GMT(year=2019, month=3, day=21, hour=7),
        'multiReply': False,
        'process' : None,
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
                'values-regex': conference.id + '/Paper<number>/AnonReviewer[0-9]+|' + conference.id + '/Paper<number>/Program_Committee_Member[0-9]+'
            },
            'writers': {
                'description': 'Users that may modify this record.',
                'values-copied':  [
                    conference.id,
                    '{signatures}'
                ]
            },
            'nonreaders': {
                'description': 'Users not allowed to read the reply',
                'values': [
                    #  change below group to prog_committee/unsubmitted
                    conference.id + '/Paper<number>/Program_Committee/Program_Committee_Member3'
                ]
            },
            'content': openreview.invitations.content.review
        }
    }
    with open('../process/officialReviewProcess.js', 'r') as f:
        official_review_template['process'] = f.read()
    blind_notes = list(openreview.tools.iterget_notes(client, invitation=conference.get_id() + '/-/Blind_Submission'))
    for index, note in enumerate(blind_notes):
        official_review_invitation = client.post_invitation(
            openreview.Invitation.from_json(
                openreview.tools.fill_template(official_review_template, note)
            )
        )
        if (index+1)%10 == 0 :
            print ('Processed ', index+1)
    print ('Processed ', index+1)