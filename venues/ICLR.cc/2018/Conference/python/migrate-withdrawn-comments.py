import openreview
import config
import csv
from collections import defaultdict
import time
import argparse

## Argument handling
parser = argparse.ArgumentParser()
parser.add_argument('--baseurl', help="base url")
parser.add_argument('--username')
parser.add_argument('--password')
args = parser.parse_args()

client = openreview.Client(baseurl=args.baseurl, username=args.username, password=args.password)
print 'connecting to:', client.baseurl

withdrawn_notes = client.get_notes(invitation='ICLR.cc/2018/Conference/-/Withdrawn_Submission')
print "# of withdrawn notes: ",len(withdrawn_notes)
all_blind_notes = client.get_notes(invitation='ICLR.cc/2018/Conference/-/Blind_Submission', includeTrash=True)
print "# of blind notes, including trash: ",len(all_blind_notes)
blind_notes = client.get_notes(invitation='ICLR.cc/2018/Conference/-/Blind_Submission')
print "# of blind notes, without trash: ",len(blind_notes)

blind_by_original = {n.original: n for n in all_blind_notes}

def get_migrated_note(old_note, withdrawn_forum_notes):
    migrated_notes = [n for n in withdrawn_forum_notes if old_note.content == n.content and old_note.tauthor == n.tauthor]
    if len(migrated_notes) > 0:
        return migrated_notes[0]
    else:
        return None

def migrate(old_note, blind_forum_notes, withdrawn_forum_notes, new_replyto_id):
    withdrawn_forum_root = [n for n in withdrawn_forum_notes if n.id == n.forum][0]

    migrated_note = get_migrated_note(old_note, withdrawn_forum_notes)

    if not migrated_note:
        note_json = old_note.to_json()
        note_id = note_json.pop('id')
        migrated_note = openreview.Note.from_json(note_json)

        migrated_note.replyto = new_replyto_id
        migrated_note.forum = withdrawn_forum_root.id
        migrated_note.tauthor = note.tauthor

        migrated_note = client.post_note(migrated_note)

        note.ddate = int(round(time.time() * 1000))
        deleted_note = client.post_note(note)
        print "deleting '{0}', created '{1}' with forum {2}),".format(deleted_note.id, migrated_note.id, migrated_note.forum)

    replies_to_migrate = [n for n in blind_forum_notes if n.replyto == old_note.id]
    for reply in replies_to_migrate:
        migrate(reply, blind_forum_notes, withdrawn_forum_notes, migrated_note.id)

for withdrawn_forum_root in withdrawn_notes:
    original_forum_root = client.get_note(withdrawn_forum_root.original)
    blind_forum_root = blind_by_original[original_forum_root.id]
    blind_forum_notes = client.get_notes(forum = blind_forum_root.forum, includeTrash=True)
    withdrawn_forum_notes = client.get_notes(forum = withdrawn_forum_root.forum)
    forum_invitations = client.get_invitations(replyForum = blind_forum_root.forum)

    for inv in forum_invitations:
        if 'replyto' in inv.reply and inv.reply['replyto'] == inv.reply['forum']:
            inv.reply['replyto'] = withdrawn_forum_root.forum
        inv.reply['forum'] = withdrawn_forum_root.forum
        inv.invitees = []
        inv.process = ''
        inv = client.post_invitation(inv)
        inv_notes = [n for n in blind_forum_notes if n.invitation == inv.id]

    for note in blind_forum_notes:
        if note.forum == note.replyto and note.forum != note.id and not note.ddate:
            migrate(note, blind_forum_notes, withdrawn_forum_notes, withdrawn_forum_root.id)
