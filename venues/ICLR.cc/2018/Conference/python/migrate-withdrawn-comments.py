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

for withdrawn_note in withdrawn_notes:
    original_note = [n for n in client.get_notes(forum=withdrawn_note.original) if n.forum == n.id][0]
    blind_note = blind_by_original[original_note.id]
    forum_notes = client.get_notes(forum=blind_note.forum)
    forum_invitations = client.get_invitations(replyForum=blind_note.forum)

    for inv in forum_invitations:
        if 'replyto' in inv.reply and inv.reply['replyto'] == inv.reply['forum']:
            inv.reply['replyto'] = withdrawn_note.forum
        inv.reply['forum'] = withdrawn_note.forum
        inv.invitees = []
        inv.process = ''
        inv = client.post_invitation(inv)
        inv_notes = [n for n in forum_notes if n.invitation == inv.id]

        for note in inv_notes:
            note_json = note.to_json()
            note_id = note_json.pop('id')
            new_note = openreview.Note.from_json(note_json)


            if new_note.replyto == new_note.forum:
                new_note.replyto = withdrawn_note.forum
            new_note.forum = withdrawn_note.forum
            new_note.tauthor = note.tauthor
            new_note = client.post_note(new_note)
            note.ddate = int(round(time.time() * 1000))
            deleted_note = client.post_note(note)
            print "deleting '{0}', created '{1}'),".format(deleted_note.id, new_note.id)
