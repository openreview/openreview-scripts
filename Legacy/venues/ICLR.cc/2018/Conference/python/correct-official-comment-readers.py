'''
When a reviewer posts a comment and sets the readership to
"reviewers and higher", authors can see the comment if they
are general conference reviewers.

This script goes through the existing official comments and
adds the author group as a nonreader, if the author group
was not the author of the comment.
'''
import openreview
import argparse

## Argument handling
parser = argparse.ArgumentParser()
parser.add_argument('--baseurl', help="base url")
parser.add_argument('--username')
parser.add_argument('--password')
args = parser.parse_args()

client = openreview.Client(baseurl=args.baseurl, username=args.username, password=args.password)
print 'connecting to:', client.baseurl

official_comments = []
finished = False
offset = 0
while not finished:
    batch = client.get_notes(invitation='ICLR.cc/2018/Conference/-/Paper.*/Official_Comment',
                                    offset=offset, limit=2000)
    official_comments += batch
    if len(batch) < 2000:
        print "len batch: ", len(batch)
        finished = True
    else:
        offset += 2000

blind_notes = client.get_notes(invitation='ICLR.cc/2018/Conference/-/Blind_Submission')

submissions_by_forum = {n.forum: n for n in blind_notes}

modified_notes = []
for n in official_comments:
    try:
        submission = submissions_by_forum[n.forum]
        note_modified = False

        if "ICLR.cc/2018/Conference/Authors_and_Higher" in n.readers:
            n.readers.remove("ICLR.cc/2018/Conference/Authors_and_Higher")
            n.readers.append('ICLR.cc/2018/Conference/Paper{number}/Authors_and_Higher'.format(number=submission.number))
            note_modified = True

        if "ICLR.cc/2018/Conference/Reviewers_and_Higher" in n.readers:
            n.readers.remove("ICLR.cc/2018/Conference/Reviewers_and_Higher")
            n.readers.append('ICLR.cc/2018/Conference/Paper{number}/Reviewers_and_Higher'.format(number=submission.number))
            note_modified = True

        if "ICLR.cc/2018/Conference/Area_Chairs_and_Higher" in n.readers:
            n.readers.remove("ICLR.cc/2018/Conference/Area_Chairs_and_Higher")
            n.readers.append('ICLR.cc/2018/Conference/Paper{number}/Area_Chairs_and_Higher'.format(number=submission.number))
            note_modified = True

        if note_modified:
            posted_n = client.post_note(n)
            modified_notes.append(posted_n)

    except KeyError as e:
        print 'paper with comment id = {note_id} has been deleted'.format(note_id=n.id)

print 'modified {number} official comments'.format(number=len(modified_notes))
