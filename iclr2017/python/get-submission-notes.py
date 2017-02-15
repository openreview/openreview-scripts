import argparse
import openreview
import requests
import csv

#####################################################################################
# This script produces a csv file with information on all notes associated with a paper
# that includes the paper number, timestamp, note type, author, note content, pdf_url.
#####################################################################################

## Argument handling
parser = argparse.ArgumentParser()
parser.add_argument('--baseurl', help="base url")
parser.add_argument('--username')
parser.add_argument('--password')
parser.add_argument('--ifile', help="input file name - default to submission_notes.csv")
args = parser.parse_args()

## Initialize the client library with username and password
if args.username!=None and args.password!=None:
    client = openreview.Client(baseurl=args.baseurl, username=args.username, password=args.password)
else:
    client = openreview.Client(baseurl=args.baseurl)
## Initialize output file name
file_name = "submission_notes.csv"
if args.ifile!=None:
    file_name = args.ifile

submissions = client.get_notes(invitation='ICLR.cc/2017/conference/-/submission')
allnotes = client.get_notes(invitation='ICLR.cc/2017/conference/-/paper.*/*')

headers = {'User-Agent': 'test-create-script', 'Content-Type': 'application/json',
           'Authorization': 'Bearer ' + client.token}
anon_reviewers = requests.get(client.baseurl + '/groups?id=ICLR.cc/2017/conference/paper.*/AnonReviewer.*',
                              headers=headers)
area_chairs = requests.get(client.baseurl+'/groups?id=ICLR.cc/2017/conference/paper.*/areachair.*', headers = headers)

# paper_status[paper_num]['pdf'] = url to the submission pdf
# paper_status[paper_num][note_id] dictionary including author, timestamp, type and content
paper_status = {}
# initialize paper_status for each submission
for paper in submissions:
    paper_status[paper.number] = {}
    paper_status[paper.number]['paper_id'] = paper.id

# add each note to the associated paper in paper_status
for note in allnotes:
    paper_num = int(note.invitation.split('paper')[1].split('/')[0])
    note_type = note.invitation.split('paper'+str(paper_num))[1]
    if paper_num in paper_status:
        author = note.signatures[0]
        id_str = note.id
        if id_str not in paper_status[paper_num]:
            paper_status[paper_num][id_str] = {}
            paper_status[paper_num][id_str]['author'] = author
            paper_status[paper_num][id_str]['timestamp'] = note.tcdate
            paper_status[paper_num][id_str]['type'] = note_type
            paper_status[paper_num][id_str]['content'] = note.content
        else:
            note_type = note.invitation.split('paper'+str(paper_num))[1]
            print("%s %s MISSED %s for %s" %(paper_num,author, note_type,
                                                           paper_status[paper_num][id_str]['type']))

# in order to come up with one set of anonymous names even thought the same person might be
# reviewer1 on paper 324 and reviewer2 on paper 444, we find all of the real names,
# then convert them each into a number

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
    # only look at areachair1,2... not "areachairs"
    if not reviewer_id.endswith('areachairs'):
        members = r['members']
        if members:
            reviewers[reviewer_id] = check_profile(members[0])

# make sure ALL names are in
for paper_num in paper_status:
    for note_id in paper_status[paper_num]:
        if note_id != 'pdf':
            name = paper_status[paper_num][note_id]['author']
            if name not in reviewers:
                reviewers[name] = name

# now that we know the real ID of everyone, we hide all of the names....
new_val = 0
for r in reviewers:
    name = reviewers[r]
    if type(name) != int:
        new_val += 1
        # it would be nice to start from 'r' and move forward
        for y in reviewers:
            if reviewers[y] == name:
                reviewers[y] = new_val

# print csv file
with open(file_name, 'wb') as outfile:
    csvwriter = csv.writer(outfile, delimiter=',', quoting=csv.QUOTE_NONNUMERIC)
    row = []
    # paper ids, title, comment, recommendation, acceptance
    row.append("PaperNum")
    row.append("Timestamp")
    row.append("Type")
    row.append("Author")
    row.append("Content")
    row.append("PdfUrl")
    csvwriter.writerow(row)
    for paper_num in paper_status:
        for note_id in paper_status[paper_num]:
            if note_id != 'paper_id':
                row = []
                row.append(paper_num)
                row.append(paper_status[paper_num][note_id]['timestamp'])
                row.append(paper_status[paper_num][note_id]['type'].encode('utf-8'))
                row.append('reviewer'+reviewers[paper_status[paper_num][note_id]['author']])
                row.append(paper_status[paper_num][note_id]['content'])
                row.append('https://openreview.net/pdf?id='+paper_status[paper_num]['paper_id'].encode('utf-8'))
                csvwriter.writerow(row)

