import openreview
import csv
import argparse
import akbc19 as conference_config

## Argument handling
parser = argparse.ArgumentParser()
parser.add_argument('file')
parser.add_argument('--baseurl', help="base url")
parser.add_argument('--username')
parser.add_argument('--password')
args = parser.parse_args()

client = openreview.Client(baseurl=args.baseurl, username=args.username, password=args.password)

print ('connecting to', client.baseurl)

def post_decision_note(pc_decision, comment, forum, paper_number):
    decision_note = openreview.Note(**{
            'forum': forum,
            'replyto': forum,
            'invitation': 'AKBC.ws/2019/Conference/-/Paper' + str(paper_number) + '/Decision',
            'signatures': ['AKBC.ws/2019/Conference/Program_Chairs'],
            'writers': ['AKBC.ws/2019/Conference/Program_Chairs'],
            'readers': ['AKBC.ws/2019/Conference/Program_Chairs'],
            'content': {
                'title': "AKBC 2019 Conference Decision",
                'decision': pc_decision,
                'comment': comment
            }
        })
    print ('Posting decision for paper: ', forum, ' ::: Decision: ', pc_decision)
    return client.post_note(decision_note)


decision_invitation_template = {
    'id': conference_config.CONFERENCE_ID + '/-/Paper<number>/Decision',
    'readers': [conference_config.PROGRAM_CHAIRS_ID],
    'writers': [conference_config.CONFERENCE_ID],
    'invitees': [conference_config.PROGRAM_CHAIRS_ID],
    'noninvitees': [],
    'signatures': [conference_config.CONFERENCE_ID],
    'reply': {
        'forum': None,
        'replyto': None,
        'readers': {
            'description': 'The users who will be allowed to read the reply content.',
            'values': [conference_config.PROGRAM_CHAIRS_ID]
        },
        'signatures': {
            'description': 'How your identity will be displayed with the above content.',
            'values': [conference_config.PROGRAM_CHAIRS_ID]
        },
        'writers': {
            'description': 'Users that may modify this record.',
            'values':  [conference_config.PROGRAM_CHAIRS_ID]
        },
        'content': {
            "title": {
                "required": True,
                "order": 1,
                "value": "AKBC 2019 Conference Decision"
            },
            "comment": {
                "required": False,
                "order": 3,
                "description": "(optional) Comment on this decision.",
                "value-regex": "[\\S\\s]{0,5000}"
            },
            "decision": {
                "required": True,
                "order": 2,
                "value-dropdown": [
                    "Accept",
                    "Reject"
                ]
            }
        }
    },
    "nonreaders": []
}

print ('Posting decision invitations.')
blind_notes = list(openreview.tools.iterget_notes(client, invitation=conference_config.BLIND_SUBMISSION_ID))
for index, note in enumerate(blind_notes):
    decision_invitation = client.post_invitation(
        openreview.Invitation.from_json(
            openreview.tools.fill_template(decision_invitation_template, note)
        )
    )
print ('Posted ', index+1, ' invitations')

submission_by_number = {n.number: n for n in client.get_notes(
    invitation='AKBC.ws/2019/Conference/-/Blind_Submission')}

decision_by_forum = {n.forum: n for n in client.get_notes(
    invitation='AKBC.ws/2019/Conference/-/Paper.*/Decision')}


with open(args.file) as f:
    reader = csv.reader(f)

    for row in reader:
        paper_number = int(row[0])
        pc_decision = row[1]
        comment = row[2].strip().strip('"')
        try:
            blind_note = submission_by_number[paper_number]
            forum = blind_note.forum

            if forum not in decision_by_forum:
                decision_note = post_decision_note(pc_decision, '', forum, paper_number)

        except KeyError as e:
            print ("Submission not found: ", paper_number)

print ('Done!')