#!/usr/bin/python

## Import statements
import argparse
import csv
from openreview import *

## Argument handling
parser = argparse.ArgumentParser()
parser.add_argument('--mintcdate',help="mininum true creation date")
parser.add_argument('--baseurl', help="base url")
parser.add_argument('--username')
parser.add_argument('--password')
args = parser.parse_args()

## Initialize the client library with username and password
openreview = Client(baseurl=args.baseurl, username=args.username, password=args.password)

def get_activity(mintcdate):

    limit = 1000
    offset = 0
    references = []
    batch = openreview.get_references(invitation="ICLR.cc/2018/Conference/-/.*", mintcdate = mintcdate, limit = limit, offset = offset)
    references += batch
    while len(batch) == limit:
        offset += limit
        batch = openreview.get_references(invitation="ICLR.cc/2018/Conference/-/.*", mintcdate = mintcdate, limit = limit, offset = offset)
        references += batch

    activity = {}
    for r in references:
        split = r.invitation.split('Paper')
        if len(split) > 1:
            split = split[1].split('/')
            if len(split) > 1:
                paper_number = split[0]
                event = split[1]
                if paper_number not in activity:
                    activity[paper_number] = {}
                paper_activity = activity[paper_number]
                if event not in paper_activity:
                    paper_activity[event] = 0
                paper_activity[event] += 1

    return activity

with open('activity.out', 'wb') as outfile:

    csvwriter = csv.writer(outfile, delimiter=',')

    notes = openreview.get_notes(invitation='ICLR.cc/2018/Conference/-/Blind_Submission')
    activity = get_activity(args.mintcdate)

    row = ['Paper #', '# Paper Revision', '# Review Revision', '# Official Comment', '# Public Comment', '# Official Review', '# Meta Review']
    csvwriter.writerow(row)

    for n in notes:
        key = str(n.number)
        row = []
        if key in activity:
            paper_activity = activity[key]
            row.append(key)
            row.append(str(paper_activity.get('Add_Revision', 0)))
            row.append(str(paper_activity.get('Revise_Review', 0)))
            row.append(str(paper_activity.get('Official_Comment', 0)))
            row.append(str(paper_activity.get('Public_Comment', 0)))
            row.append(str(paper_activity.get('Official_Review', 0)))
            row.append(str(paper_activity.get('Meta_Review', 0)))
            csvwriter.writerow(row)
        # Uncomment if you want to get the list of all the papers
        # else:
        #     row.append(key)
        #     row.append('0')
        #     row.append('0')
        #     row.append('0')
        #     row.append('0')
        #     row.append('0')
        #     row.append('0')
        #     csvwriter.writerow(row)








