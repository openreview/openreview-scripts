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

## Initialize the client library with username and password
if args.username!=None and args.password!=None:
    client = openreview.Client(baseurl=args.baseurl, username=args.username, password=args.password)
else:
    client = openreview.Client(baseurl=args.baseurl)
## Initialize output file name
file_name = "status.csv"
if args.ofile!=None:
    file_name = args.ofile


submissions = client.get_notes(invitation='ICLR.cc/2017/conference/-/submission')
metareviews = client.get_notes(invitation='ICLR.cc/2017/conference/-/paper.*/meta/review')
acceptances = client.get_notes(invitation='ICLR.cc/2017/conference/-/paper.*/acceptance')
acceptance_name = 'ICLR2017'

# paper_status[paper_num] dictionary w/ 'title','comment','recommendation','acceptance'
paper_status = {}

# initialize paper_status for each submission
for paper in submissions:
    paper_status[paper.number] = {}
    paper_status[paper.number]['title'] = paper.content['title']
    paper_status[paper.number]['comment'] = ""
    paper_status[paper.number]['recommendation'] = ""
    paper_status[paper.number]['acceptance'] = ""

# add area chair recommendations
for note in metareviews:
    paper_num = int(note.invitation.split('paper')[1].split('/meta/review')[0])
    paper_status[paper_num]['comment'] = note.content['metareview']
    paper_status[paper_num]['recommendation'] = note.content['recommendation']

# add PI acceptances
for note in acceptances:
    paper_num = int(note.invitation.split('paper')[1].split('/acceptance')[0])
    paper_status[paper_num]['acceptance'] = note.content[acceptance_name]
    # if acceptance, but no area chair recommendation, fill in with blanks so it prints properly
    # PAM better way to handle this at the append stage?
    if not paper_status[paper_num]['recommendation']:
        paper_status[paper_num]['recommendation'] =""
        paper_status[paper_num]['comment'] = ""

# print results
# csv
with open(file_name, 'wb') as outfile:
    csvwriter = csv.writer(outfile, delimiter=',')
    row = []
    # paper ids, title, comment, recommendation, acceptance
    row.append("Paper Number")
    row.append("Title")
    row.append("Comment")
    row.append("Recommendation")
    row.append("Acceptance")
    csvwriter.writerow(row)
    for paper_num in paper_status:
        row = []
        row.append(paper_num)
        row.append(paper_status[paper_num]['title'])
        row.append(paper_status[paper_num]['comment'])
        row.append(paper_status[paper_num]['recommendation'])
        row.append(paper_status[paper_num]['acceptance'])
        csvwriter.writerow(row)
