import openreview
import argparse
import icml

def upload_submissions(client):
    # repost 20 papers from AKBC 2019
    # TODO: Change this to read from ICML papers
    for paper in client.get_notes(invitation='AKBC.ws/2019/Conference/-/Submission'):
        new_content = {key: value for key, value in paper.content.items() \
                       if key in icml.submission_inv.reply['content'].keys()}

        new_writers = [w.replace('AKBC.ws', 'ICML.cc') for w in paper.writers]

        posted_submission = client.post_note(openreview.Note(**{
            'writers': new_writers,
            'readers': [icml.CONFERENCE_ID],
            'content': new_content,
            'invitation': icml.SUBMISSION_ID,
            'signatures': [icml.CONFERENCE_ID]
        }))

        papergroup = client.post_group(openreview.Group.from_json({
            'id': 'ICML.cc/2019/Conference/Paper{}'.format(posted_submission.number),
            'readers': ['everyone'],
            'writers': [icml.CONFERENCE_ID],
            'signatures': [icml.CONFERENCE_ID],
            'signatories': [],
            'members': []
        }))

        posted_mask = client.post_note(openreview.Note(**{
            'original': posted_submission.id,
            'forum': None,
            'replyto': None,
            'readers': ['everyone'],
            'writers': [icml.CONFERENCE_ID],
            'signatures': [icml.CONFERENCE_ID],
            'invitation': icml.blind_submission_inv.id,
            'content': {
                key: entry.get('value') or entry.get('values') \
                for key, entry in icml.blind_submission_inv.reply['content'].items() \
                if 'value' in entry or 'values' in entry
           }
        }))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--baseurl', help="base url")
    parser.add_argument('--username')
    parser.add_argument('--password')
    args = parser.parse_args()

    client = openreview.Client(baseurl=args.baseurl, username=args.username, password=args.password)
    print('connecting to {} with username {}'.format(client.baseurl, client.username))

    upload_submissions(client)
