import argparse
import openreview
import csv

parser = argparse.ArgumentParser()
parser.add_argument('filename', help="input csv filename")
parser.add_argument('--baseurl', help="base url")
parser.add_argument('--username')
parser.add_argument('--password')
args = parser.parse_args()

client = openreview.Client(baseurl=args.baseurl, username=args.username, password=args.password)
conference_id = 'reproducibility-challenge.github.io/Reproducibility_Challenge/NeurIPS/2019'

with open(args.filename, "r") as in_file:
    file_reader = csv.reader(in_file, delimiter=',')
    for row in file_reader:
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
                    "title": row[0],
                    "authors": row[1],
                    "authorsids": row[2],
                    "abstract": row[3]
                }
            ))
            if posted_note:
                print(posted_note.id)
                #add paper group so we can add comments
                group = client.post_group(openreview.Group(
                    id='{conference_id}/NeurIPS{number}'.format(conference_id=conference_id, number=posted_note.number),
                    signatures=[conference_id], signatories=[conference_id],
                    readers=[conference_id], writers=[conference_id]))

                # add comment invite
                comment_inv = client.post_invitation(openreview.Invitation(
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
                    }
                ))
                #print(comment_inv)

        except openreview.OpenReviewException:
            pass

