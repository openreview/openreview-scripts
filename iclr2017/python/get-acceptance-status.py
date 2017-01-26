import argparse
import openreview
import requests
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
file_name = "acceptances.csv"
if args.ofile!=None:
    file_name = args.ofile


submissions = client.get_notes(invitation='ICLR.cc/2017/conference/-/submission')
metareviews = client.get_notes(invitation='ICLR.cc/2017/conference/-/paper.*/meta/review')
acceptances = client.get_notes(invitation='ICLR.cc/2017/conference/-/paper.*/acceptance')
reviews = client.get_notes(invitation='ICLR.cc/2017/conference/-/paper.*/official/review')

headers = {'User-Agent': 'test-create-script', 'Content-Type': 'application/json',
           'Authorization': 'Bearer ' + client.token}
anon_reviewers = requests.get(client.baseurl + '/groups?id=ICLR.cc/2017/conference/paper.*/AnonReviewer.*',
                              headers=headers)
area_chairs = requests.get(client.baseurl+'/groups?id=ICLR.cc/2017/conference/paper.*/areachair1.*', headers = headers)

acceptance_name = 'ICLR2017'

# initialize all values for each paper/reviewer pair
def paper_status_initialize(paper_dict):
    paper_dict['type'] = ""
    paper_dict['score'] = ""
    paper_dict['recommendation'] = ""
    paper_dict['comment'] = ""
    paper_dict['confidence'] = ""
    paper_dict['num_interactions'] = 0

# get the info from the review, return NA if not there
def get_score(note, content_type):
    string_var = note.content.get(content_type, "NA")
    string_var = string_var.split(':')[0]
    return string_var

# profile_by_email[email_id] = ~name
profile_by_email = {}
def check_profile(member):

    if member.startswith('~'):
        return member

    if '@' in member:
        if member in profile_by_email:
            return profile_by_email[member]

        response = requests.get(client.baseurl+'/user/profile?email=' + member, headers = headers)
        if 'profile' not in response.json():
            profile_by_email[member] = member
            return member
        profile = response.json()['profile']
        profile_by_email[member] = profile['id']
        return profile_by_email[member]

    return member

# paper_status[paper_num][reviewer] dictionary
paper_status = {}

# get the entry in the paper_status dict - initialize new entry if needed
def get_paper_status_entry(note, note_type):
    paper_num = int(note.invitation.split('paper')[1].split(note_type)[0])
    reviewer = note.writers[0]
    if paper_num not in paper_status:
        # if paper not in submissions it was probably deleted
        return None
    else:
        if reviewer not in paper_status[paper_num]:
            # create new entry
            paper_status[paper_num][reviewer] = {}
            paper_status_initialize(paper_status[paper_num][reviewer])
        else:
            print("overwriting %s %s" % (paper_num,reviewer))
        return paper_status[paper_num][reviewer]

# attach real name to the anonymized name for reviewers
reviewers = {}
for r in anon_reviewers.json():
    reviewer_id = r['id']
    members = r['members']
    if members:
        reviewers[reviewer_id] = check_profile(members[0])

# attach real name to the anonymized name for area chairs
# and convert email ids to names
for r in area_chairs.json():
    reviewer_id = r['id']
    members = r['members']
    if members:
        reviewers[reviewer_id] = check_profile(members[0])

for paper in submissions:
    paper_status[paper.number] = {}

# official reviews
for note in reviews:
    paper_entry = get_paper_status_entry(note, '/official/review')
    if paper_entry is not None:
        paper_entry['type'] = "review"
        paper_entry['score'] = get_score(note, 'rating')
        paper_entry['confidence'] = get_score(note, 'confidence')

# add area chair recommendations
for note in metareviews:
    paper_entry = get_paper_status_entry(note, '/meta/review')
    paper_entry['type'] = "meta-review"
    paper_entry['recommendation'] = note.content['recommendation']
    paper_entry['comment'] = note.content['metareview']

# add PI acceptances
for note in acceptances:
    paper_entry = get_paper_status_entry(note, '/acceptance')
    paper_entry['type'] = "acceptance"
    paper_entry['recommendation'] = note.content[acceptance_name]

# print results
# csv
with open(file_name, 'wb') as outfile:
    csvwriter = csv.writer(outfile, delimiter=',')
    row = []
    # paper ids, title, comment, recommendation, acceptance
    row.append("PaperID")
    row.append("Type")
    row.append("Name")
    row.append("Score")
    row.append("Recommendation")
    row.append("Confidence")
    row.append("Comment")
#    row.append("#OfficalInteractions")
    csvwriter.writerow(row)
    for paper_num in paper_status:
        for rev_id in paper_status[paper_num]:
            row = []
            row.append(paper_num)
            row.append(paper_status[paper_num][rev_id]['type'].encode('utf-8'))
            row.append(reviewers[rev_id].encode('utf-8'))
            row.append(paper_status[paper_num][rev_id]['score'].encode('utf-8'))
            row.append(paper_status[paper_num][rev_id]['recommendation'].encode('utf-8'))
            row.append(paper_status[paper_num][rev_id]['confidence'].encode('utf-8'))
            row.append(paper_status[paper_num][rev_id]['comment'].encode('utf-8'))
#            row.append(paper_status[paper_num][rev_id]['num_interactions'])
            csvwriter.writerow(row)
