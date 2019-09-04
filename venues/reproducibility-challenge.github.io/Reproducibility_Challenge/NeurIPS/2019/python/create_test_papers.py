import argparse
import openreview

parser = argparse.ArgumentParser()
parser.add_argument('--baseurl', help="base url")
parser.add_argument('--username')
parser.add_argument('--password')
args = parser.parse_args()

#client = openreview.Client(baseurl='https://openreview.net', username=args.username, password='theindiankinginvitesthepatriarch')
client = openreview.Client(baseurl=args.baseurl, username=args.username, password=args.password)
neurips_papers = client.get_notes(invitation='dblp.org/-/record', content={'venueid': 'dblp.org/conf/NIPS/2018'})

#client = openreview.Client(baseurl=args.baseurl, username=args.username, password=args.password)
conference_id = 'reproducibility-challenge.github.io/Reproducibility_Challenge/NeurIPS/2019'
accepted_info = [{'title': n.content['title'], 'abstract': n.content['abstract'], 'authors': n.content['authors']} for n in neurips_papers if 'abstract' in n.content]

post_count = 0
for info in accepted_info:
    try:
        posted_note = client.post_note(openreview.Note(
            id=None,
            original=None,
            invitation=conference_id+"/-/NeurIPS_Submission",
            forum=None,
            signatures=[conference_id+"/Program_Chairs"],
            writers=[conference_id],
            readers=['everyone'],
            content={
                "title": info['title'],
                "authors": info['authors'],
                "abstract": info['abstract']
            }
        ))
        if posted_note:
            post_count += 1

            #add paper group so we can add comments
            group = client.post_group(openreview.Group(
                id='{conference_id}/NeurIPS{number}'.format(conference_id=conference_id, number=posted_note.number),
                signatures=[conference_id], signatories=[conference_id],
                readers=[conference_id], writers=[conference_id]))

            # add comment invite
            comment_inv = openreview.Invitation(
                id='{}/NeurIPS{}/-/Comment'.format(conference_id, posted_note.number),
                readers=['everyone'],
                invitees=['~'],
                writers=[conference_id],
                signatures=[conference_id],
                reply={
                    'forum': posted_note.forum,
                    'replyto': None,
                    'content': {
                        'title': {
                            'value-regex': '.*',
                            'order': 0,
                            'required': True
                        },
                        'comment': {
                            'description': 'Your comment or reply (max 5000 characters).',
                            'order': 1,
                            'required': True,
                            'value-regex': '[\\S\\s]{1,5000}'
                        }
                    },
                    'signatures': {
                        'description': 'Your authorized identity to be associated with the above content.',
                        'values-regex': '~.*'
                    },
                    'readers': {
                        'description': 'The users who will be allowed to read the above content.',
                        'values': ['everyone']
                    },
                    'writers': {
                        'values-copied': [conference_id, '{signatures}']
                    }
                },
                # TODO who should the commentProcess email
                # process='../process/commentProcess.py'
            )
            client.post_invitation(comment_inv)

    except openreview.OpenReviewException:
        pass

    if post_count >= 100:
        break

print(post_count)