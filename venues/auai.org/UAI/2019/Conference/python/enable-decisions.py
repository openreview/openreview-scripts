import argparse
import openreview
import datetime
import config
import csv

if __name__ == '__main__':
    ## Argument handling
    parser = argparse.ArgumentParser()
    parser.add_argument('--baseurl', help="base url")
    parser.add_argument('--username')
    parser.add_argument('--password')
    parser.add_argument('decisions_file')
    args = parser.parse_args()

    client = openreview.Client(baseurl=args.baseurl, username=args.username, password=args.password)
    conference = config.get_conference(client)

    conference.open_decisions(
        options = ['Accept', 'Reject'],
        start_date = datetime.datetime(2019, 5, 12, 11, 59),
        due_date = datetime.datetime(2019, 5, 14, 23, 59))

    paper_number_to_decisions = {int(metarev.invitation.split('Paper')[1].split('/')[0]): metarev for metarev in \
    openreview.tools.iterget_notes(
        client,
        invitation = conference.id + '/-/Paper.*/Decision'
    )}
    failures = []
    new_decisions = 0
    with open(args.decisions_file) as f:
        for row in csv.reader(f):
            if row[0] and row[0] != 'Area Chair':
                paper_number = int(row[1])
                if paper_number not in paper_number_to_decisions:
                    decision = row[6].strip()
                    decision_text = row[7].strip()
                    if not decision:
                        if row[5].strip() in ['Accept (Poster)', 'Accept (Oral)']:
                            decision = 'Accept'
                        elif row[5].strip() in ['Weak Reject', 'Reject']:
                            decision = 'Reject'
                        else:
                            failures.append(str(paper_number))
                    else:
                        print ('Change found for paper {0}, decision: {1} and decision-text:{2}'.format(
                            paper_number,
                            decision,
                            decision_text)
                        )

                    # post decision note for this paper
                    decision_note = client.post_note(openreview.Note(
                        invitation = conference.id + '/-/Paper{0}/Decision'.format(paper_number),
                        content = {
                            'title' : 'Final Decision',
                            'decision' : decision,
                            'comment' : decision_text
                        }
                    ))
                    new_decisions += 1

    print ('Posted {0} new decisions'.format(new_decisions))
    print ('Failed to post decisions for ', ', '.join(failures))
