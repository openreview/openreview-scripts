import openreview
import csv
import argparse

## Argument handling
parser = argparse.ArgumentParser()
parser.add_argument('file')
parser.add_argument('--baseurl', help="base url")
parser.add_argument('--username')
parser.add_argument('--password')
args = parser.parse_args()

client = openreview.Client(baseurl=args.baseurl, username=args.username, password=args.password)

print 'connecting to', client.baseurl

def get_decision_note(pc_decision, comment, forum):
    decision_note = openreview.Note(**{
            'forum': forum,
            'replyto': forum,
            'invitation': 'ICLR.cc/2018/Conference/-/Acceptance_Decision',
            'signatures': ['ICLR.cc/2018/Conference/Program_Chairs'],
            'writers': ['ICLR.cc/2018/Conference/Program_Chairs'],
            'readers': ['ICLR.cc/2018/Conference/Program_Chairs'],
            'content': {
                'title': "ICLR 2018 Conference Acceptance Decision",
                'decision': pc_decision,
                'comment': comment
            }
        })
    return decision_note

submission_by_number = {n.number: n for n in client.get_notes(
    invitation='ICLR.cc/2018/Conference/-/Blind_Submission')}

decision_by_forum = {n.forum: n for n in client.get_notes(
    invitation='ICLR.cc/2018/Conference/-/Acceptance_Decision')}


with open(args.file) as f:
    reader = csv.reader(f)
    print reader.next()
    for row in reader:
        paper_number = int(row[0])
        title = row[1]
        ac_metareview = row[7]
        pc_decision = row[10]
        pc_metareview = row[12]

        comment = pc_metareview if pc_metareview else ac_metareview
        try:
            forum = submission_by_number[paper_number].forum

            if forum not in decision_by_forum:
                decision_note = get_decision_note(pc_decision, comment, forum)
                client.post_note(decision_note)

        except KeyError as e:
            print "Submission not found: ", paper_number



