import argparse
import openreview
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

# paper_status[paper_num]['pdf'] = url to the submission pdf
# paper_status[paper_num][note_id] dictionary including author, timestamp, type and content
paper_status = {}
# initialize paper_status for each submission
for paper in submissions:
    paper_status[paper.number] = {}
    paper_status[paper.number]['paper_id'] = paper.id

# add each note to the associated paper in paper_status
for note in allnotes:
    paper_num0 = note.invitation.split('paper')[1].split('/')[0]
    note_type = note.invitation.split('paper' + str(paper_num0))[1]
    # WHY does paper_num work and paper_num0 not?
    paper_num = int(note.invitation.split('paper')[1].split(note_type)[0])
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
            note_type = note.invitation.split('paper' + str(paper_num))[1]
            print("%s %s MISSED %s for %s" % (paper_num, author, note_type,
                                              paper_status[paper_num][id_str]['type']))

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
                row.append(paper_status[paper_num][note_id]['author'].encode('utf-8'))
                row.append(paper_status[paper_num][note_id]['content'])
                row.append('https://openreview.net/pdf?id='+paper_status[paper_num]['paper_id'].encode('utf-8'))
                csvwriter.writerow(row)

