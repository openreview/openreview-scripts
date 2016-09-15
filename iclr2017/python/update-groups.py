#!/usr/bin/python

"""
Setup python script takes as input the CSV files above and adds them as
members to the groups ICLR.cc/2017/pc, areachairs, and reviewers-invited.

"""

## Import statements
import argparse
import csv
import sys
from openreview import *

## Handle the arguments
parser = argparse.ArgumentParser()
parser.add_argument('-p','--programchairs', help="csv file containing the email addresses of the program chair(s)")
parser.add_argument('-a','--areachairs', help="csv file containing the email addresses of the area chairs")
parser.add_argument('-r','--reviewers', help="csv file containing the email addresses of candidate reviewers. Will send invitation email to the addresses on this list.")
parser.add_argument('--baseurl', help="base URL")
parser.add_argument('--username')
parser.add_argument('--password')

args = parser.parse_args()

## Initialize the client library with username and password
if args.username!=None and args.password!=None:
    openreview = Client(baseurl=args.baseurl, username=args.username, password=args.password)
else:
    openreview = Client(baseurl=args.baseurl)

groups = [];

def SingleAssignmentValid(s):
    if not '@' in s:
        return False

    return True

def sendMail(reviewers_invited):
    ## For each candidate reviewer, send an email asking them to confirm or reject the request to review
    for count, reviewer in enumerate(reviewers_invited):
        print "Sending message to "+reviewer
        hashkey = openreview.get_hash(reviewer, "4813408173804203984")
        url = openreview.baseurl+"/invitation?id=ICLR.cc/2017/conference/-/reviewer_invitation&email=" + reviewer + "&key=" + hashkey + "&response="
        message = "You have been invited to serve as a reviewer for the International Conference on Learning Representations (ICLR) 2017 Conference.\n\n"
        message = message+ "To ACCEPT the invitation, please click on the following link: \n\n"
        message = message+ url + "Yes\n\n"
        message = message+ "To DECLINE the invitation, please click on the following link: \n\n"
        message = message+ url + "No\n\n" + "Thank you"

        openreview.send_mail("OpenReview invitation response", [reviewer], message)


def update_group_members(groupid,assignment):
    new_members = []
    group = openreview.get_group(groupid)
    

    if type(group)==Group:

        if assignment.endswith('.csv'):
            with open(assignment, 'rb') as assignment:
                reader = csv.reader(assignment, delimiter=',', quotechar='|')
                for row in reader:
                    for email in row:
                        new_members.append(email)
        elif SingleAssignmentValid(assignment):
            new_members.append(assignment)
        else:
            print "Invalid input: ",assignment
            sys.exit()

        print "updating group ",g
        group.members += new_members
    else:
        print "could not find group ",g
    
    # if groupid=='ICLR.cc/2017/conference/reviewers-invited':
    #     sendMail(new_members)

    return group


for g,c in [('ICLR.cc/2017/pcs',args.programchairs),('ICLR.cc/2017/areachairs',args.areachairs),('ICLR.cc/2017/conference/reviewers-invited',args.reviewers)]:
    if c!=None:
        group = update_group_members(g,c)
        if type(group)==Group:
            openreview.post_group(group)

    
