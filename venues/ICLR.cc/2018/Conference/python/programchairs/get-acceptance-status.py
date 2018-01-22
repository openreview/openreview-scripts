#!/usr/bin/python

"""
Dump csv file of meta-review information to make final decision.
"""
import argparse
import openreview
import csv

## Argument handling
parser = argparse.ArgumentParser()
parser.add_argument('--baseurl', help="base url")
parser.add_argument('--username')
parser.add_argument('--password')
parser.add_argument('--ofile', help="output file name - default to status.csv")
args = parser.parse_args()

def init_paper_info(client):
    print "loading submissions"
    submissions = client.get_notes(invitation='ICLR.cc/2018/Conference/-/Blind_Submission')
    paper_info={}
    for n in submissions:
        paper_info[n.number] = {}
        paper_info[n.number]['title'] = n.content['title']
        paper_info[n.number]['AC_rec'] = ""
        paper_info[n.number]['AC_conf'] = ""
        paper_info[n.number]['AC_meta'] = ""
        paper_info[n.number]['AC_name'] = ""
        paper_info[n.number]['ave_score'] = 0
        paper_info[n.number]['reviews'] = []
        paper_info[n.number]['num_review'] = 0
    return paper_info

def get_activity(client, paper_info):
    # load in all notes from conference
    print "loading reviews"
    limit = 1000
    offset = 0
    notes = []
    batch = client.get_notes(invitation="ICLR.cc/2018/Conference/-/.*", limit=limit, offset=offset)
    notes += batch
    while len(batch) == limit:
        offset += limit
        batch = client.get_notes(invitation="ICLR.cc/2018/Conference/-/.*", limit=limit, offset=offset)
        notes += batch

    # grab necessary data from notes
    for n in notes:
        split = n.invitation.split('Paper')
        if len(split) > 1:
            split = split[1].split('/')
            if len(split) > 1:
                paper_number = int(split[0])
                event = split[1]
                if paper_number in paper_info:
                    if event == 'Meta_Review':
                        #fill in meta data
                        paper_info[paper_number]['AC_rec'] = n.content['recommendation']
                        paper_info[paper_number]['AC_conf'] = n.content['confidence'].split(':')[0]
                        paper_info[paper_number]['AC_meta'] = n.content['metareview']
                        profile = client.get_profile(n.tauthor)
                        paper_info[paper_number]['AC_name'] = profile.id
                    elif event == 'Official_Review':
                        #add review data
                        paper_info[paper_number]['num_review'] += 1
                        paper_info[paper_number]['reviews'].append({'rating':n.content['rating'].split(':')[0],
                                                                'conf':n.content['confidence'].split(':')[0]})

    return paper_info


# output all information needed to make a final decision on a paper
def output_paper_info(file_name, paper_info):
    print "writing to file "+file_name
    with open(file_name, 'wb') as outfile:
        csvwriter = csv.writer(outfile, delimiter=',')
        row = ['Paper #', 'Paper Title', 'AC Recommendation', 'AC Confidence', 'Ave Scores', 'R1 Score',
               'R1 Confidence', 'R2 Score', 'R2 Confidence', 'R3 Score', 'R3 Confidence', 'R4 Scores', 'R4 Confidence',
               'AC MetaReview', 'AC', 'Final Decision']
        csvwriter.writerow(row)

        for n in paper_info:
            row = []
            row.append(n)
            row.append(paper_info[n]['title'].encode('utf-8'))
            row.append(paper_info[n]['AC_rec'])
            row.append(paper_info[n]['AC_conf'])
            score = 0.0
            if paper_info[n]['num_review'] > 0:
                for rev in paper_info[n]['reviews']:
                    score += int(rev['rating'])
                score = score / paper_info[n]['num_review']
            row.append('%.2f' % score)
            for rev in paper_info[n]['reviews']:
                row.append(rev['rating'])
                row.append(rev['conf'])
            for index in range(paper_info[n]['num_review'], 4):
                row.append('')
                row.append('')
            row.append(paper_info[n]['AC_meta'].encode('utf-8'))
            row.append(paper_info[n]['AC_name'])
            csvwriter.writerow(row)


def main():
    ## Initialize the client library with username and password
    client = openreview.Client(baseurl=args.baseurl, username=args.username, password=args.password)

    paper_info = init_paper_info(client)
    paper_info = get_activity(client, paper_info)

    ## Initialize output file name
    file_name = "acceptances.csv"
    if args.ofile!=None:
        file_name = args.ofile
    output_paper_info(file_name, paper_info)

if __name__ == "__main__":
    main()