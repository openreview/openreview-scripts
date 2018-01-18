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

withdrawn_notes = client.get_notes(invitation='ICLR.cc/2018/Conference/-/Withdrawn_Submission')
print "withdrawn notes: ",len(withdrawn_notes)
all_blind_notes = client.get_notes(invitation='ICLR.cc/2018/Conference/-/Blind_Submission', includeTrash=True)
print "blind notes, including trash: ",len(all_blind_notes)
blind_notes = client.get_notes(invitation='ICLR.cc/2018/Conference/-/Blind_Submission')
print "blind notes, without trash: ",len(blind_notes)

submissions_by_forum = {n.forum: n for n in all_blind_notes}
withdrawn_by_forum = {n.forum: n for n in withdrawn_notes}
submissions_by_forum.update(withdrawn_by_forum)

modified_notes = []
for n in official_comments:
    try:
        submission = submissions_by_forum[n.forum]
    except KeyError as e:
        print n.id
        raise(e)
    if ("ICLR.cc/2018/Conference/Reviewers_and_Higher" in n.readers or
        "ICLR.cc/2018/Conference/Area_Chairs_and_Higher" in n.readers or
        "ICLR.cc/2018/Conference/Program_Chairs" in n.readers):

        n.nonreaders = submission.content['authorids']
        posted_n = client.post_note(n)
        modified_notes.append(posted_n)

print 'modified {number} official comments'.format(number=len(modified_notes))
