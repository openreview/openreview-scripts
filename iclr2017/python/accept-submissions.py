import argparse
import openreview
import csv

## Argument handling
parser = argparse.ArgumentParser()
parser.add_argument('--baseurl', help="base url")
parser.add_argument('--username')
parser.add_argument('--password')
parser.add_argument('--ifile', help="input file name - default to status.csv")
args = parser.parse_args()

## Initialize the client library with username and password
if args.username!=None and args.password!=None:
    client = openreview.Client(baseurl=args.baseurl, username=args.username, password=args.password)
else:
    client = openreview.Client(baseurl=args.baseurl)
## Initialize output file name
file_name = "acceptances.csv"
if args.ifile!=None:
    file_name = args.ifile


submissions = client.get_notes(invitation='ICLR.cc/2017/conference/-/submission')
acceptances = client.get_notes(invitation='ICLR.cc/2017/conference/-/paper.*/acceptance')
# valid acceptance values
valid_values = [
    "Accept (Oral)",
    "Accept (Poster)",
    "Reject",
    "Invite to Workshop Track"
]

any_errors = False
# accept_new[paper_num] dictionary w/ 'forum', 'acceptance'
accept_new = {}
# initialize accept_new from file
try:
    with open(file_name, "rb") as in_file:
        file_reader = csv.reader(in_file, delimiter=',')
        # skip top line
        file_reader.next()
        for row in file_reader:
            # first column is the paper number, last column is the needed acceptance status
            paper_num = int(row[0])
            if row[4] != "":
                print("add %s" %paper_num)
                if row[4] in valid_values:
                    accept_new[paper_num] = {}
                    accept_new[paper_num]['acceptance']=row[4]
                else:
                    any_errors = True
                    print("Paper%s invalid acceptance value '%s'" %(paper_num,row[4]))
except (OSError, IOError) as e:
    print(e)
    file_data =[]
    exit()

# if any of the acceptance values were set to unrecognized values, print the accepted values
if any_errors:
    print("Valid acceptance values are %s" %valid_values)

# Since csv files use paper numbers and acceptance notes use forum,
# need to translate between them.  Paper_numbers a dict w/ forum as key, and num as value
paper_numbers = {}
for paper in submissions:
    paper_numbers[paper.forum] = paper.number
    if paper.number in accept_new.keys():
        accept_new[paper.number]['forum'] = paper.forum

# Remove existing acceptance notes from the accept_new list.
for note in acceptances:
    paper_num = paper_numbers[note.forum]
    if paper_num in accept_new.keys():
        # Check if acceptance notes agree w/ spreadsheet values, throw error if problem
        if note.content['ICLR2017'] != accept_new[paper_num]['acceptance']:
            print("Cannot change previously accepted paper %s" % paper_num)
        # remove from the new acceptance list
        del accept_new[paper_num]


# fill in generic acceptance note info
note = openreview.Note()
note.signatures = ['ICLR.cc/2017/pcs']
note.writers = ['ICLR.cc/2017/pcs']
note.readers = ['ICLR.cc/2017/pcs','ICLR.cc/2017/areachairs','ICLR.cc/2017/conference']
# for all new acceptances, set paper specific info and post acceptance note
for paper_num in accept_new:
    invitation ='ICLR.cc/2017/conference/-/paper' +str(paper_num)+'/acceptance'
    note.invitation = invitation
    note.forum = accept_new[paper_num]['forum']
    note.replyto = accept_new[paper_num]['forum']
    note.content = {'ICLR2017':accept_new[paper_num]['acceptance']}
    client.post_note(note)
    print ("Paper %s: new acceptance" % paper_num)
