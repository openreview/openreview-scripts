import openreview
import config
import argparse

def post_blind_note(client, original_note, conference):
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

    blind_note = openreview.Note(
        original= original_note.id,
        invitation= conference.id + '/-/Blind_Submission',
        forum=None,
        signatures= [conference.id],
        writers= [conference.id],
        readers= [conference.id],
        content= {
            "authors": ['Anonymous'],
            "authorids": [conference.id],
            "_bibtex": None
        })

    posted_blind_note = client.post_note(blind_note)
    conference_id = conference.get_id()
    
    pc_group_id = "{conference_id}/Program_Committee".format(conference_id = conference_id)
    paper_group_id = "{conference_id}/Paper{number}".format(conference_id = conference_id, number = posted_blind_note.number)
    author_group_id = conference.id + "/Paper{}/Authors".format(posted_blind_note.number)
    reviewer_group_id = "{conference_id}/Paper{number}/Reviewers".format(conference_id = conference_id, number = posted_blind_note.number)
    reviewer_group_invited_id = "{conference_id}/Paper{number}/Reviewers/Invited".format(conference_id = conference_id, number = posted_blind_note.number)
    reviewer_group_declined_id = "{conference_id}/Paper{number}/Reviewers/Declined".format(conference_id = conference_id, number = posted_blind_note.number)

    # Reposting blind-note with correct authorid group, correct readers and updated bibtex
    posted_blind_note.content['authorids'] = [author_group_id]
    posted_blind_note.readers = [
        conference.id + '/Program_Chairs',
        pc_group_id, 
        author_group_id,
        reviewer_group_id,
        reviewer_group_invited_id,
        reviewer_group_declined_id,
        conference_id]
    posted_blind_note.content['_bibtex'] = "@inproceedings{\nanonymous2019" + original_note.content['title'].split(' ')[0] + ",\ntitle={" + original_note.content['title'] + "},\nauthor={Anonymous},    \nbooktitle={Submitted to Conference on Learning Theory},    \nyear={2019},    \nurl={https://openreview.net/forum?id=" + posted_blind_note.forum + "},    \nnote={under review}    \n}"
    posted_blind_note = client.post_note(posted_blind_note)

    client.post_group(openreview.Group(id = paper_group_id,
        readers = [conference_id, conference_id + '/Program_Chairs', pc_group_id],
        writers = [conference_id],
        signatures = [conference_id],
        signatories = []))
    client.post_group(openreview.Group(id = author_group_id,
        readers = [conference_id, conference_id + '/Program_Chairs', pc_group_id, author_group_id],
        writers = [conference_id],
        signatures = [conference_id],
        signatories = [author_group_id]))
    client.post_group(openreview.Group(id = reviewer_group_id,
        readers = [reviewer_group_id, conference_id, conference_id + '/Program_Chairs', pc_group_id],
        writers = [conference_id, pc_group_id],
        signatures = [conference_id],
        signatories = [reviewer_group_id]))
    client.post_group(openreview.Group(id = reviewer_group_invited_id,
        readers = [conference_id, conference_id + '/Program_Chairs', pc_group_id],
        writers = [conference_id, pc_group_id],
        signatures = [conference_id],
        signatories = [reviewer_group_invited_id]))
    client.post_group(openreview.Group(id = reviewer_group_declined_id,
        readers = [conference_id, conference.id + '/Program_Chairs', pc_group_id],
        writers = [conference_id, pc_group_id],
        signatures = [conference_id],
        signatories = [reviewer_group_declined_id]))

    official_review_invitation = client.post_invitation(
        openreview.Invitation.from_json(
            openreview.tools.fill_template(official_review_template, posted_blind_note)
        )
    )

if __name__ == '__main__':
    ## Argument handling
    parser = argparse.ArgumentParser()
    parser.add_argument('--baseurl', help="base url")
    parser.add_argument('--username')
    parser.add_argument('--password')
    args = parser.parse_args()

    client = openreview.Client(baseurl=args.baseurl, username=args.username, password=args.password)
    conference = config.get_conference(client)

    print ("Closing submissions")
    conference.close_submissions()

    print ("Updating webfield for ", conference.id)
    homepage = client.get_group(id = conference.id)
    with open('../webfield/homepage.js', 'r') as f:
        homepage.web = f.read()
    client.post_group(homepage)

    print ('Posting blinded notes')
    submissions = list(openreview.tools.iterget_notes(client, invitation=conference.get_submission_id()))
    for paper in submissions:
        post_blind_note(client, paper, conference)  
