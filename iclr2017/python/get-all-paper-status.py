import argparse
import openreview
import requests
import csv
import sys, getopt

## Argument handling
parser = argparse.ArgumentParser()
parser.add_argument('--baseurl', help="base url")
parser.add_argument('--username')
parser.add_argument('--password')
parser.add_argument('--ofile', help="output file name")
args = parser.parse_args()

## Initialize the client library with username and password
if args.username!=None and args.password!=None:
    client = openreview.Client(baseurl=args.baseurl, username=args.username, password=args.password)
else:
    client = openreview.Client(baseurl=args.baseurl)
## Initialize output file name
file_name = "output.csv"
if args.ofile!=None:
    file_name = args.ofile
## Initialize output file type - check for valid values
output_type = 2

class PaperStatus:
    Unassigned, Assigned, Commented, Reviewed, FullyReviewed = range(5)

PaperStatusString = ["Unassigned", "Assigned", "Commented", "Reviewed", "FullyReviewed"]


# get the info from the review, return NA if not there
def get_score(content_type):
    string_var = note.content.get(content_type, "NA")
    string_var = string_var.split(':')[0]
    return string_var

# pull all needed info from the database
submissions = client.get_notes(invitation='ICLR.cc/2017/conference/-/submission')
invitation = "official/review"
headers = {'User-Agent': 'test-create-script', 'Content-Type': 'application/json',
           'Authorization': 'Bearer ' + client.token}
anon_reviewers = requests.get(client.baseurl + '/groups?id=ICLR.cc/2017/conference/paper.*/AnonReviewer.*',
                              headers=headers)
current_reviewers = requests.get(client.baseurl + '/groups?id=ICLR.cc/2017/conference/paper.*/reviewers',
                                 headers=headers)
notes = client.get_notes(invitation='ICLR.cc/2017/conference/-/paper.*/' + invitation)

# The following are dictionaries to connect the papers, reviewers and reviews
# 	the signature is the whole directory struct leading up to the Anonymized name
# 	ex ICLR.cc/2017/conference/-/paper203/AnonReviewer1
# reviews[signature] = the review note
reviews = {}
# reviewers[signature] = reviewer_name
reviewers = {}
# reviewers_by_paper[paper_num][reviewer_name] = review
reviewers_by_paper = {}
# paper_status[paper_num] dictionary w/ 'title' (paper title),'count'(number of reviewers),
#													 'reviewed',  'percent'(percentage reviewed)
paper_status = {}

# initialize paper_status for each submission and attach title to paper number
for paper in submissions:
    paper_status[paper.number] = {}
    paper_status[paper.number]['title'] = paper.content['title']
    paper_status[paper.number]['count'] = 0
    paper_status[paper.number]['reviewed'] = 0
    paper_status[paper.number]['percent'] = 0
    reviewers_by_paper[paper.number] = {}

# attach review note to the anonymized name
for n in notes:
    signature = n.signatures[0]
    reviews[signature] = n

# attach real name to the anonymized name
for r in anon_reviewers.json():
    reviewer_id = r['id']
    members = r['members']
    if members:
        reviewers[reviewer_id] = members[0]
    else:
        paper_num = int(reviewer_id.split('paper')[1].split('/Anon')[0])
        if paper_num in paper_status:
            # check if paper wasn't deleted then why is reviewer missing?
            if output_type == 1:
                my_file.write('Reviewer ' + reviewer_id + ' is anonymous\n')
            else:
                print('Reviewer ' + reviewer_id + ' is anonymous')

# attach reviewers to paper_num
# add review status paper_status
for r in current_reviewers.json():
    reviewer_id = r['id']
    members = r['members']
    if members:
        paper_num = int(reviewer_id.split('paper')[1].split('/reviewers')[0])
        if paper_num in paper_status:
            # if the number isn't in paper_status it means the submission was deleted
            for m in members:
                # add reviewers
                reviewer_name = reviewers.get(m, m)
                reviewers_by_paper[paper_num][reviewer_name] = reviews.get(m, None)
                paper_status[paper_num]['count'] += 1
                if reviewers_by_paper[paper_num][reviewer_name] != None:
                    paper_status[paper_num]['reviewed'] += 1

# now that all reviewers have been added to the paper_status
# for each paper determine how many reviewers have completed reviewing
for paper_num in paper_status:
    paper_status[paper_num]['percent'] = 100 * paper_status[paper_num]['reviewed'] / paper_status[paper_num][
        'count']

# sort on % complete (doesn't like being sorted in place)
paper_status_sorted = sorted(paper_status, key=lambda x: (paper_status[x]['percent'], x))


# print results
# csv
with open(file_name, 'wb') as outfile:
    csvwriter = csv.writer(outfile, delimiter=',')
    row = []
    row.append("Paper Number")
    row.append("Title")
    row.append("%Review Complete")
    row.append("Reviewer Name")
    row.append("Review Rating")
    row.append("Review Confidence")
    csvwriter.writerow(row)
    for paper_num in paper_status_sorted:
        reviewers = reviewers_by_paper[paper_num]
        for reviewer, note in reviewers.iteritems():
            row = []
            row.append(paper_num)
            row.append(paper_status[paper_num]['title'])
            row.append(paper_status[paper_num]['percent'])
            row.append(reviewer.encode('utf-8'))
            if note:
                row.append(get_score('rating'))
                row.append(get_score('confidence'))
            else:
                row.append(0)
                row.append(0)
            csvwriter.writerow(row)
