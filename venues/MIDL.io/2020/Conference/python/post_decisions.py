#!/usr/bin/python

###############################################################################
''' Post decisions for MIDL2020 and email decision to authors'''
###############################################################################

## Import statements
import argparse
import csv
import datetime
from openreview import *
from openreview import tools



## Argument handling
parser = argparse.ArgumentParser()
parser.add_argument('assignments', help="either (1) a csv file containing submission decisions or (2) a string of the format '<paper#>,<decision>' e.g. '23,Reject'")
parser.add_argument('--baseurl', help="base url")
parser.add_argument('--username')
parser.add_argument('--password')
args = parser.parse_args()

## Initialize the client library with username and password
client = Client(baseurl=args.baseurl, username=args.username, password=args.password)
print("Connecting to "+client.baseurl)

subject_line = "Decision for MIDL submission #{0}"
message = {}
message['Reject']='''Dear Author,


We regret to inform you that your submission #{0} has not been accepted to MIDL 2020. We understand that this decision might be disappointing. However, we received a large number of excellent submissions. When making our final decisions, we took all information into account, including the reviews, review scores, rebuttal, and AC meta-reviews, with the objective of putting together a high quality, competitive conference. 


The acceptance rate for full papers is 44.6% (66/148 submissions), 39.6% for short papers (42/106), 41.7% in total (106/254). There is a growth of 26% in full paper submissions from last year.


If you wish, you can withdraw your paper from the OpenReview system now. If this is the case, we recommend that you do so before April 16th.
After April 16th, author names will become visible and public comments will be enabled.  If you choose not to withdraw your paper from the system, you are welcome to update your pdf to de-anonymize it and to take into account the reviewers’ suggestions.


We hope that you will still participate in the MIDL 2020 conference. This year the conference will be fully virtual. We will inform everyone about the logistics, including registration information, soon.


Sincerely,
Program Chairs for MIDL 2020'''


message['Accept'] = '''Dear Author,
 
We are happy to inform you that your submission #{0} has been accepted for presentation for the MIDL 2020 conference. We will inform you about the format of presentation in the coming weeks.
 
The acceptance rate for full papers is 44.6% (66/148 submissions), 39.6% for short papers (42/106), 41.7% in total (106/254). There is a growth of 26% in full paper submissions from last year.
 
We encourage you to take into account the reviewers’ concerns and apply appropriate changes to your submission to improve its quality. As such, you can upload a new pdf onto the OpenReview system. If you need to go over the suggested page limit, you may do so while still aiming for conciseness. If you have not yet done so, please update your paper using the provided latex template: 
https://github.com/MIDL-Conference/MIDLLatexTemplate.
Further information on the process for submitting the camera-ready manuscript (only for full papers) for inclusion in the PMLR proceedings will be provided in due course.
 
Please note that public comments on your paper will become possible as of April 16th. At that point, we will also publicly release decisions and author names.   
 
Congratulations once again. We are looking forward to your participation in MIDL 2020.  This year, the conference will be fully virtual. We will inform everyone about the logistics, including registration information, soon. 
 
Sincerely,
Program Chairs for MIDL 2020
'''


iterator = client.get_notes(invitation='MIDL.io/2020/Conference/-/Blind_Submission')
submissions = {}
for paper in iterator:
    submissions[paper.number]=paper


def post_decision(paper_num, decision, add_text):
    if (decision == "Reject") or (decision == "Accept"):
        paper = submissions[int(paper_num)]

        # post decision note as Accept or Reject
        paperinv = 'MIDL.io/2020/Conference/Paper' + paper_num + '/-/Decision'
        decision_note= openreview.Note(
            invitation= paperinv,
            forum= submissions[int(paper_num)].id,
            signatures= ['MIDL.io/2020/Conference/Program_Chairs'],
            writers= ['MIDL.io/2020/Conference/Program_Chairs'],
            readers= ['MIDL.io/2020/Conference/Program_Chairs',
                    'MIDL.io/2020/Conference/Paper' + paper_num + '/Area_Chairs',
                    'MIDL.io/2020/Conference/Paper' + paper_num + '/Authors'],
            content= {
                'title':'Paper Decision',
                'decision':decision, 
                'comment': add_text
            }
        )
        client.post_note(decision_note)

        print("Post note: "+paper_num+decision)

        client.post_message(subject_line.format(paper_num), paper.content['authorids'],
                            message[decision].format(paper_num))

    else:
        print("Decision invalid: <"+decision+">")

##################################################################



if args.assignments.endswith('.csv'):
    with open(args.assignments, 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        # skip header row
        next(reader,None)
        for row in reader:
            paper_number = row[0]
            if len(row) >=2 :
                decision = row[1]
            if len(row) >= 3:
                add_text = row[2]
            else:
                add_text = ""
            post_decision(paper_number, decision, add_text)
