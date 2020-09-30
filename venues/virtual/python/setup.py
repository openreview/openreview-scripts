import argparse
import openreview
import json
import datetime

parser = argparse.ArgumentParser()
parser.add_argument('--baseurl', help="base url")
parser.add_argument('--username')
parser.add_argument('--password')
args = parser.parse_args()

client = openreview.Client(baseurl=args.baseurl, username=args.username, password=args.password)


## metadata for the home page
meta_data = {
    "date": "2020-05-01",
    "title": "ICLR 2020 Conference Virtual",
    "sponsors": ["microsoft", "amazon"]
}

## Main conference virtual group
conference_id='ICLR.cc/2020/Conference'
virtual_group_id='ICLR.cc/2020/Conference/Virtual'
client.post_group(openreview.Group(id=virtual_group_id,
                 readers=['everyone'],
                 writers=[conference_id],
                 signatures=[conference_id],
                 signatories=[],
                 members=[],
                 web_string=json.dumps(meta_data)))


## Session invitation
session_invitation_id=f"{virtual_group_id}/-/Session"
client.post_invitation(openreview.Invitation(
    id=session_invitation_id,
    readers=['everyone'],
    writers=[conference_id],
    invitees=[conference_id],
    signatures=[conference_id],
    reply={
        'readers': { 'values': ['everyone'] },
        'writers': { 'values': [conference_id] },
        'signatures': { 'values': [conference_id] },
        'content': {
            'start': { 'value-regex': '.*' },
            'end': { 'value-regex': '.*' },
            'title': { 'value-regex': '.*' }
        }
    }
))


## Create two sessions
session_1 = client.post_note(openreview.Note(
    invitation=session_invitation_id,
    readers=['everyone'],
    writers=[conference_id],
    signatures=[conference_id],
    content={
        'start': openreview.tools.datetime_millis(datetime.datetime(2020, 10, 2, 15, 0)),
        'end': openreview.tools.datetime_millis(datetime.datetime(2020, 10, 2, 18, 0)),
        'title': 'Session 1'
    }
))
session_2 = client.post_note(openreview.Note(
    invitation=session_invitation_id,
    readers=['everyone'],
    writers=[conference_id],
    signatures=[conference_id],
    content={
        'start': openreview.tools.datetime_millis(datetime.datetime(2020, 10, 2, 18, 0)),
        'end': openreview.tools.datetime_millis(datetime.datetime(2020, 10, 2, 20, 0)),
        'title': 'Session 1'
    }
))


## Presentation invitation
presentation_invitation_id=f"{virtual_group_id}/-/Presentation"
client.post_invitation(openreview.Invitation(
    id=presentation_invitation_id,
    readers=['everyone'],
    writers=[conference_id],
    invitees=[conference_id],
    signatures=[conference_id],
    reply={
        'readers': { 'values': ['everyone'] }, ## should be restricted?
        'writers': { 'values': [conference_id] },
        'signatures': { 'values': [conference_id] },
        'content': {
            'video': { 'value-regex': '.*' },
            'slides': { 'value-regex': '.*' },
            'chat': { 'value-regex': '.*' },
            'live': { 'value-regex': '.*' },
            'session': { 'value-regex': '.*' }
        }
    }
))

## Create presentations based on ICLR accepted papers
presentation_1 = client.post_note(openreview.Note(
    invitation=presentation_invitation_id,
    original='rylb7mnqIB', ## CATER: A diagnostic dataset for Compositional Actions & TEmporal Reasoning
    readers=['everyone'],
    writers=[conference_id],
    signatures=[conference_id],
    content={
        'video': 'https://youtube.com/paper',
        'slides': 'https://slideslive.com/paper',
        'chat': 'https://rocketchat.com/paper',
        'live': 'https://zoom.us/paper',
        'session': session_1.id
    }
))

print(presentation_1.id)