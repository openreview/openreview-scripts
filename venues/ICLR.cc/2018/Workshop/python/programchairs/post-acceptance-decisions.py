import openreview
import csv
import argparse

## with output flag, outputs csv file with paper number, title, decision (if known), comments
## without output flag, reads in csv file and posts new acceptance decisions
## Argument handling
parser = argparse.ArgumentParser()
parser.add_argument('file')
parser.add_argument('--baseurl', help="base url")
parser.add_argument('--username')
parser.add_argument('--password')
parser.add_argument('--output', action='store_true', help="output current status to file")
args = parser.parse_args()

client = openreview.Client(baseurl=args.baseurl, username=args.username, password=args.password)

print 'connecting to', client.baseurl

def get_decision_note(pc_decision, comment, forum):
    decision_note = openreview.Note(**{
            'forum': forum,
            'replyto': forum,
            'invitation': 'ICLR.cc/2018/Workshop/-/Acceptance_Decision',
            'signatures': ['ICLR.cc/2018/Workshop/Program_Chairs'],
            'writers': ['ICLR.cc/2018/Workshop/Program_Chairs'],
            'readers': ['ICLR.cc/2018/Workshop/Program_Chairs'],
            'content': {
                'title': "ICLR 2018 Workshop Acceptance Decision",
                'decision': pc_decision,
                'comment': comment
            }
        })
    return decision_note


if args.output:
    # output information
    decision_notes = client.get_notes(invitation='ICLR.cc/2018/Conference/-/Acceptance_Decision')
    decisions = {}
    for note in decision_notes:
        decisions[note.forumContent['paperhash']] = {'decision': note.content['decision'], 'comment': ''}

    # let Workshop acceptance overwrite Conference acceptance
    decision_notes = client.get_notes(invitation='ICLR.cc/2018/Workshop/-/Acceptance_Decision')
    for note in decision_notes:
        decisions[note.forumContent['paperhash']] = {'decision': note.content['decision'], 'comment': ''}
        if 'comment' in note.content:
            decisions[note.forumContent['paperhash']] ['comment']= note.content['comment']


    notes = client.get_notes(invitation='ICLR.cc/2018/Workshop/-/Submission')
    with open(args.file, 'wb') as outfile:
        csvwriter = csv.writer(outfile, delimiter=',')
        row = ['Paper #', 'Paper Title', 'Decision', 'Comment']
        csvwriter.writerow(row)

        for note in notes:
            decision = ""
            comment = ""
            # Check if paper already reviewed in Conference or Workshop
            if note.content['paperhash'] in decisions:
                conf_decision = decisions[note.content['paperhash']]['decision']
                if conf_decision == "Accept" or conf_decision == "Invite to Workshop Track":
                    decision = "Accept"
                elif conf_decision == "Reject":
                    decision = "Reject"
                comment = decisions[note.content['paperhash']]['comment']
            row = []
            row.append(note.number)
            row.append(note.content['title'])
            row.append(decision)
            row.append(comment)
            csvwriter.writerow(row)

else:
    # input file, post new acceptances
    submission_by_number = {n.number: n for n in client.get_notes(
        invitation='ICLR.cc/2018/Workshop/-/Submission')}

    decision_by_forum = {n.forum: n for n in client.get_notes(
        invitation='ICLR.cc/2018/Workshop/-/Acceptance_Decision')}

    with open(args.file) as f:
        # load header
        reader = csv.reader(f)
        print reader.next()
        for row in reader:
            paper_number = int(row[0])
            title = row[1]
            pc_decision = row[2]
            pc_comment = row[3]

            if pc_decision:
                try:
                    forum = submission_by_number[paper_number].forum

                    if forum not in decision_by_forum:
                        print "post "+forum
                        decision_note = get_decision_note(pc_decision, pc_comment, forum)
                        client.post_note(decision_note)

                except KeyError as e:
                    print "Submission not found: ", paper_number



