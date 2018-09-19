#!/usr/bin/python

"""
A script for managing groups with parameters that depend on the papers to which
they are attached.

Usage:

python groups.py Reviewers
python groups.py Reviewers --overwrite
"""

import openreview
import argparse
import iclr19

def getBibtex(client, note):
    firstWord = note.content["title"].split(' ')[0].lower();
    url = client.baseurl + '/forums?id=' + note.forum
    return '@article{\
    \nanonymous2019' + firstWord + ',\
    \ntitle={' + note.content["title"] + '},\
    \nauthor={Anonymous},\
    \njournal={International Conference on Learning Representations},\
    \nyear={2019},\
    \nurl={' + url + '}\
    \n}'

def create_blind_note(note):
    return openreview.Note(
        original= note.id,
        invitation= iclr19.BLIND_SUBMISSION_ID,
        forum= None,
        signatures= [iclr19.CONFERENCE_ID],
        writers= [iclr19.CONFERENCE_ID],
        readers= ['everyone'],
        content= {
            "authors": ['Anonymous'],
            "authorids": [],
            "_bibtex": None
        })

def freeze_note(note, writers=[iclr19.CONFERENCE_ID]):
    note.writers = writers
    return note

def freeze_and_post(client, notes):
    for note in notes:
        client.post_note(freeze_note(note))

def post_blind_notes(client, original_notes):
    blind_notes = []
    for original_note in original_notes:
        blind_note = client.post_note(create_blind_note(original_note))
        paper_group_id = iclr19.CONFERENCE_ID + "/Paper{}".format(blind_note.number)
        author_group_id = iclr19.CONFERENCE_ID + "/Paper{}/Authors".format(blind_note.number)

        # Update Blind note's contents, repost the updated blind note, and freeze and post the original note
        blind_note.content["authorids"] = [author_group_id]
        blind_note.content["_bibtex"] = getBibtex(client, blind_note)
        blind_notes.append(client.post_note(blind_note))
    return blind_notes

if __name__ == '__main__':
    # Argument handling
    parser = argparse.ArgumentParser()
    parser.add_argument('notes', nargs='*', help="any of the following: " + ", ".join(group_templates.keys()))
    parser.add_argument('--overwrite', action='store_true', help="if present, overwrites the members of the groups")
    parser.add_argument('--baseurl', help="base url")
    parser.add_argument('--username')
    parser.add_argument('--password')
    args = parser.parse_args()

    client = openreview.Client(baseurl=args.baseurl, username=args.username, password=args.password)

