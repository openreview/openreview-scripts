import argparse
import openreview
import json
import datetime
from random import randrange
from tqdm import tqdm

parser = argparse.ArgumentParser()
parser.add_argument('--baseurl', help="base url")
parser.add_argument('--username')
parser.add_argument('--password')
args = parser.parse_args()

client = openreview.Client(baseurl=args.baseurl, username=args.username, password=args.password)


## metadata for the home page
meta_data = {
    "date": "2020-05-01",
    "title": "ICLR 2020 Conference Virtual"
}

## metadata for the home/sponsor/organizer page
meta_data_home = {
    "date": "2020-05-01",
    "title": "ICLR 2020 Conference Virtual",
    "layout": [
        {
            "name": "Markdown",
            "option": " _ italic formatted with markdown _"
        },
        {
            "name": "Organizers"
        },
        {
            "name": "Sponsors"
        },
        {
            "name": "JumbotronImage"
        }
    ]
}

meta_data_sponsors={
    "layout":[
        {
            "name":"Markdown",
            "option":"~~content of sponsors page formatted with markdown~~"
        }
    ]
}

meta_data_organizers={
    "layout":[
        {
            "name":"Markdown",
            "option":"_ content of organizers page formatted with markdown _"
        }
    ]
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
                 web_string=json.dumps(meta_data_home)))


client.post_group(openreview.Group(id=f"{virtual_group_id}/Sponsors",
                 readers=['everyone'],
                 writers=[conference_id],
                 signatures=[conference_id],
                 signatories=[],
                 members=[f"{virtual_group_id}/Sponsors/Diamond", f"{virtual_group_id}/Sponsors/Gold", f"{virtual_group_id}/Sponsors/Silver"],
                 web_string=json.dumps(meta_data_sponsors)))

client.post_group(openreview.Group(id=f"{virtual_group_id}/Sponsors/Diamond",
                 readers=['everyone'],
                 writers=[conference_id],
                 signatures=[conference_id],
                 signatories=[],
                 members=["deepmind", "facebook", "googleresearch"]))

client.post_group(openreview.Group(id=f"{virtual_group_id}/Sponsors/Gold",
                 readers=['everyone'],
                 writers=[conference_id],
                 signatures=[conference_id],
                 signatories=[],
                 members=["amazon", "ibm", "openai"]))

client.post_group(openreview.Group(id=f"{virtual_group_id}/Sponsors/Silver",
                 readers=['everyone'],
                 writers=[conference_id],
                 signatures=[conference_id],
                 signatories=[],
                 members=["apple", "microsoft", "elementai"]))


client.post_group(openreview.Group(id=f"{virtual_group_id}/Organizers",
                 readers=['everyone'],
                 writers=[conference_id],
                 signatures=[conference_id],
                 signatories=[],
                 members=["~Alexander_Rush1", "~Shakir_Mohamed1", "~Martha_White1", "~Kyunghyun_Cho1", "~Dawn_Song1"],
                 web_string=json.dumps(meta_data_organizers)))

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
            'title': { 'value-regex': '.*' },
            'description': { 'value-regex': '.*' }
        }
    }
))


## Create two sessions
sessions = []
sessions.append(client.post_note(openreview.Note(
    invitation=session_invitation_id,
    readers=['everyone'],
    writers=[conference_id],
    signatures=[conference_id],
    content={
        'start': openreview.tools.datetime_millis(datetime.datetime(2020, 10, 2, 15, 0)),
        'end': openreview.tools.datetime_millis(datetime.datetime(2020, 10, 2, 18, 0)),
        'title': 'Session 1',
        'description':'this is the description of session 1'
    }
)))
sessions.append(client.post_note(openreview.Note(
    invitation=session_invitation_id,
    readers=['everyone'],
    writers=[conference_id],
    signatures=[conference_id],
    content={
        'start': openreview.tools.datetime_millis(datetime.datetime(2020, 10, 2, 18, 0)),
        'end': openreview.tools.datetime_millis(datetime.datetime(2020, 10, 2, 20, 0)),
        'title': 'Session 2',
        'description':'this is the description of session 2'
    }
)))
sessions.append(client.post_note(openreview.Note(
    invitation=session_invitation_id,
    readers=['everyone'],
    writers=[conference_id],
    signatures=[conference_id],
    content={
        'start': openreview.tools.datetime_millis(datetime.datetime(2020, 10, 5, 9, 0)),
        'end': openreview.tools.datetime_millis(datetime.datetime(2020, 10, 5, 10, 0)),
        'title': 'Session 3',
        'description':'this is the description of session 3'
    }
)))
sessions.append(client.post_note(openreview.Note(
    invitation=session_invitation_id,
    readers=['everyone'],
    writers=[conference_id],
    signatures=[conference_id],
    content={
        'start': openreview.tools.datetime_millis(datetime.datetime(2020, 10, 5, 10, 0)),
        'end': openreview.tools.datetime_millis(datetime.datetime(2020, 10, 5, 12, 0)),
        'title': 'Session 4',
        'description':'this is the description of session 4'
    }
)))


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
            'slideslive': { 'value-regex': '.*' },
            'chat': { 'value-regex': '.*' },
            'live': { 'value-regex': '.*' },
            'session': { 'value-regex': '.*' }
        }
    }
))


submissions = client.get_notes(invitation='ICLR.cc/2020/Conference/-/Submission')


for s in tqdm(submissions):
    ## Create presentations based on ICLR accepted papers
    presentation_1 = client.post_note(openreview.Note(
        invitation=presentation_invitation_id,
        original=s.id,
        readers=['everyone'],
        writers=[conference_id],
        signatures=[conference_id],
        content={
            'slideslive': '38915149',
            'chat': 'https://rocketchat.com/paper',
            'live': 'https://zoom.us/paper',
            'session': sessions[randrange(4)].id
        }
    ))
