'''
This is a one time script to deduplicate ICLR 2018 submissions.
'''

import openreview
import config
import csv
import argparse
from collections import defaultdict


parser = argparse.ArgumentParser()
parser.add_argument('--baseurl', help="base URL")
parser.add_argument('--username')
parser.add_argument('--password')

args = parser.parse_args()

client = openreview.Client(baseurl=args.baseurl, username=args.username, password=args.password)
print client.baseurl


# delete all but the latest version of all papers
submissions = client.get_notes(invitation=config.SUBMISSION)
blind_submissions = client.get_notes(invitation=config.BLIND_SUBMISSION)
print "there are {0} submissions and {1} blind submissions".format(len(submissions), len(blind_submissions))



# collect notes by paperhash
notes_by_paperhash = defaultdict(list)
for n in submissions:
    notes_by_paperhash[n.content['paperhash']].append(n)

# find duplicates by looking for paperhashes with more than one note
duplicates_by_paperhash = {paperhash: notes for paperhash, notes in notes_by_paperhash.iteritems() if len(notes)>1}


# collect all the blind references keyed by original ID
blindrefs_by_original = {}

for b in blind_submissions:
    references = client.get_revisions(referent=b.id)
    blindrefs_by_original[b.original] = [r for r in references if r.id == r.referent][0]

print "there are {0} duplicate hashes".format(len(duplicates_by_paperhash))

# iterate through the duplicates
for paperhash, notes in duplicates_by_paperhash.iteritems():

    # for every paperhash, sort the notes by tcdate.
    # the first note should be the one posted last.
    latest_note = sorted(notes, key=lambda n: n.tcdate, reverse=True)[0]
    assert latest_note.tcdate == max([n.tcdate for n in notes])

    print "keeping ",latest_note.id
    for n in notes:
        if n != latest_note:
            n.ddate = 1509138000000

            try:
                deleted_n = client.post_note(n)
                print "--> deleting original ", deleted_n.id
            except openreview.OpenReviewException as e:
                print 'ERROR on {0}:{1} '.format(n.id, e)


            try:
                blind_ref = blindrefs_by_original[n.id]
                blind_ref.ddate = 1509138000000
                deleted_ref = client.post_note(blind_ref)
                print "--> deleting blind", deleted_ref.id
            except KeyError as e:
                print "--> already deleted blind ", deleted_ref.id

# check again
submissions = client.get_notes(invitation=config.SUBMISSION)
blind_submissions = client.get_notes(invitation=config.BLIND_SUBMISSION)
print "there are {0} submissions and {1} blind submissions".format(len(submissions), len(blind_submissions))



# check to see if there are any duplicates remaining
notes_by_paperhash = defaultdict(list)

for n in submissions:
    notes_by_paperhash[n.content['paperhash']].append(n)

duplicates_by_paperhash = {paperhash: notes for paperhash, notes in notes_by_paperhash.iteritems() if len(notes)>1}

print "there are {0} remaining duplicate hashes:".format(len(duplicates_by_paperhash))
for k, v in duplicates_by_paperhash.iteritems():
    print k
    for note in v: print note.id
