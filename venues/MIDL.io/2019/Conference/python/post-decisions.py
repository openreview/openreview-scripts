#!/usr/bin/python

###############################################################################
''' Assigns reviewers to papers - run in same directory as config.py
 ex. python assign-reviewers.py --baseurl http://localhost:3000
       --username admin --password admin_pw 'reviewer@gmail.com,3'

 Checks paper number is an integer.
 Check reviewer email address or domain is not on the conflicts list.
 Check reviewer is in the system.
 If reviewer is not in conference reviewers group (config.CONF/Reviewers), add it.
 If reviewer not already assigned to this paper:
	Determine AnonReviewer number
	Create Paper#/AnonReviewer#  group with this reviewer as a member
    Assign Paper#/AnonReviewer# to the Paper#/Reviewers group for this paper'''
###############################################################################

## Import statements
import argparse
import csv
import config
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
conference = config.get_conference(client)

iterator = client.get_notes(invitation=conference.get_submission_id())
submissions = {}
for paper in iterator:
    submissions[paper.number]=paper

subject_line = "MIDL Submission decision"
message = {}
message['Reject']='''Dear Author,

We regret to inform you that your submission to MIDL 2019 has been rejected for the full paper tract. This year, we received a large number of high quality submissions and could only accept a certain portion for the full paper track.

Please note that the submission deadline for the abstract has not yet passed (12 April 2019 17:00 UTC). We encourage you to revise your article based on reviewers’ comments, and consider submitting a shorter version of it to the abstract tract. Details about the abstract track can be found here: http://2019.midl.io/call-for-papers/

Thank you once again for your interest in MIDL 2019. We hope that despite the outcome, you consider joining us in London for the conference.

Sincerely,
Program Chairs for MIDL 2019.'''


message['LP Accept / Borderline']= '''Dear Author,

{0}

Unfortunately, given the concerns raised by the reviewers and our target acceptance rate, the PC decided not to accept your submission for the full paper track. However, there is clear consensus that your submission has merit for presentation at MIDL, and is likely to result in valuable discussion. Given the quality of your submission, we would be delighted to have your submission presented in the abstract track and like to offer you an early acceptance if you decide to summarise and resubmit the article as an extended abstract.

If you accept our offer, we ask you to submit a faithful summary of your initial full submission as a 3 page extended abstract, excluding references and acknowledgements. Further details for the abstract submissions can be found here: http://2019.midl.io/call-for-papers/. We also would like to remind you our dual submission policy, if you are also considering submitting your work to elsewhere. Details for the dual submission policy can be found here: https://2019.midl.io/submissions/.

Additionally, please let us know if you would like us to remove your full paper from the OpenReview environment since the full paper is not accepted.

Thank you for your interest in MIDL 2019. We hope you accept our offer and decide to join us in the conference. We are looking forward to seeing you in London.

Sincerely,
Program Chairs for MIDL 2019.'''

message['Accept'] = '''Dear Author,

We are happy to inform you that your submission {0} to MIDL has been accepted for presentation in the conference as a full submission. We will inform you about the type of presentation (Oral / Poster) in the next two weeks. In the meanwhile, there are two important points we would like to draw your attention to:

For the camera-ready version, we encourage you to take into account the reviewers’ concerns and apply appropriate changes to your submission to improve its quality. To this end, if you need to go over the suggested page limit, you may do so while still aiming for conciseness. The quality of the published article in the PMLR proceedings is the most important concern. We acknowledge that these changes might also take time. To provide you enough time, we have set the deadline for submitting the camera-ready version to 15 April 2019. Please inform us as soon as possible, if you think you will not be able to prepare the camera ready article until then. Further information on the process for submitting the camera-ready manuscript will be provided in due course.


Importantly, in order to ensure publication of your paper, please be aware that each conference paper must have at least one author registering to the conference no later than 25th of March.
Details about registration can be found here: https://2019.midl.io/registration/

Congratulations once again. We are looking forward to seeing you in London in July.

Sincerely,
Program Chairs for MIDL 2019
'''
def create_decision_invite():
    ## Decision

    for key in submissions.keys():
        paperinv = conference.get_id() + '/-/Paper' + str(key) + '/Decision'

        decision_reply = {
            'forum': submissions[key].id,
            'replyto': submissions[key].id,
            'writers': {'values': [conference.get_id()]},
            'signatures': {'values': [conference.get_program_chairs_id()]},
            'readers': {
                'values': ['everyone'],
                'description': 'The users who will be allowed to read the above content.'
            },
            'content': {
                'title': {
                    'order': 1,
                    'value': 'Acceptance Decision'
                },
                'decision': {
                    'order': 2,
                    'value-radio': [
                        'Accept',
                        'Reject'
                    ],
                    'required': True
                },
                'presentation': {
                    'order': 3,
                    'value-radio': [
                        'Oral',
                        'Poster',
                    ],
                    'required': False
                }
            }
        }

        decision_parameters = {
            'readers': ['everyone'],
            'writers': [conference.get_id()],
            'signatures': [conference.get_id()],
            'duedate': tools.timestamp_GMT(2019, month=2, day= 22, hour=23, minute=59),
            'invitees': [conference.get_program_chairs_id()],
            'reply': decision_reply
        }

        invite = openreview.Invitation(paperinv, **decision_parameters)
        client.post_invitation(invite)

def remove_if_rejected(paper_num, decision, add_text):
    if int(paper_num) not in submissions.keys():
        # already removed
        print("already removed "+paper_num)
        return True
    else:
        paper = submissions[int(paper_num)]
        if (decision == "Reject" or decision == "LP Accept / Borderline")\
                and paper.content.get('remove if rejected', False):
            # this is actually the time now here as though it were GMT so it's off by 5 hours.
            paper.ddate = tools.datetime_millis(datetime.datetime.now())
            client.post_note(paper)
            print("Remove note: " + paper_num)
            client.send_mail(subject_line, paper.content['authorids'], message[decision].format(add_text))
            return True
    return False

def post_decision(paper_num, decision, add_text):
    if (decision == "Reject") or (decision == "Accept") or (decision == "LP Accept / Borderline"):
        paper = submissions[int(paper_num)]
        if decision == "LP Accept / Borderline":
            # if borderline, use additional text in email
            # but treat as if rejected
            client.send_mail(subject_line, paper.content['authorids'],
                             message[decision].format(add_text))
            decision = "Reject"
        else:
            client.send_mail(subject_line, paper.content['authorids'],
                             message[decision].format(paper.content['title']))

        # post decision note as Accept or Reject
        paperinv = conference.get_id() + '/-/Paper' + paper_num + '/Decision'
        decision_note= openreview.Note(
            invitation= paperinv,
            forum= submissions[int(paper_num)].id,
            signatures= [conference.get_program_chairs_id()],
            writers= [conference.get_id()],
            readers= ['everyone'],
            content= {'title':'Acceptance Decision',
                      'decision':decision}
        )
        client.post_note(decision_note)
        print("Post note: "+paper_num+decision)
    elif decision:
        print("Decision invalid: <"+decision+">")

##################################################################

create_decision_invite()
if args.assignments.endswith('.csv'):
    with open(args.assignments, 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        # skip header row
        next(reader,None)
        for row in reader:
            paper_number = row[1]
            if len(row) >= 13:
                decision = row[12]
            if len(row) >= 14:
                add_text = row[13]
            else:
                add_text = ""
            if not remove_if_rejected(paper_number, decision, add_text):
                post_decision(paper_number, decision, add_text)
else:
    paper_number = args.assignments.split(',')[1]
    decision = args.assignments.split(',')[0]
    if not remove_if_rejected(paper_number, decision, ""):
        post_decision(paper_number, decision, "")
