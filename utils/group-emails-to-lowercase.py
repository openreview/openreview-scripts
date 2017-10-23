#!/usr/bin/python

###############################################################################
# ex. python group-emails-to-lowercase.py -group MyConf.org/2017/Reviewers --baseurl http://localhost:3000
#       --username admin --password admin_pw
#
# Sets all members that are emails to lowercase.  Notifies user if there are profiles or groups using the
# uppercase letters in the
###############################################################################

## Import statements
import argparse
import sys
from openreview import *

## Argument handling
parser = argparse.ArgumentParser()
parser.add_argument('-g','--group', required=True, help = "the full path of the group ex. MyConf.org/2017")
parser.add_argument('--baseurl', help="base url")
parser.add_argument('--username')
parser.add_argument('--password')

args = parser.parse_args()

## Initialize the client library with username and password
client = Client(baseurl=args.baseurl, username=args.username, password=args.password)

def get_profile(value):
    profile = None
    try:
        profile = client.get_profile(value)
    except openreview.OpenReviewException as e:
        # throw an error if it is something other than "not found"
        if e[0][0] != 'Profile not found':
            print "OpenReviewException: {0}".format(e)
            raise e
    return profile

def get_group(value):
    group = None
    try:
        group = client.get_group(value)
    except openreview.OpenReviewException as e:
        # throw an error if it is something other than "not found"
        if e[0][0]['type'] != 'Not Found':
            print "OpenReviewException: {0}".format(e)
            raise e
    return group

# return True if it finds an uppercase letter
def has_uppercase(value):
    has_upper = False
    for character in value:
        if character.isupper():
            has_upper = True
    return has_upper

# locate emails w/ uppercase letters
#   replace with lowercase email
def upper_to_lower(group_name):
    target_group = get_group(group_name)
    upper_emails = []
    lower_emails = []
    if target_group == None:
        print "ERROR: invalid group id {0}".format(group_name)
    else:
        for email in target_group.members:
            if '@' in email and has_uppercase(email):
                # find emails with uppercase
                # has uppercase chars, convert to lowercase
                print email
                lower = email.lower()
                upper_emails.append(email)
                lower_emails.append(lower)
        ### replace uppercase w/ lowercase emails
        print "Replace emails with lowercase: {0}".format(upper_emails)
        client.remove_members_from_group(target_group,upper_emails)
        client.add_members_to_group(target_group, lower_emails)
    return upper_emails

# print uppercase profiles and groups found
def find_upper_email_references(upper_emails):
    ## try to get profile via email
    ## if get one, check that lower exists and set to that group instead
    for email in upper_emails:
        profile = get_profile(email)
        if profile != None:
            print "ERROR: Uppercase profile for {0} with id {1}".format(email, profile.id)
        group = get_group(email)
        if group != None:
            if len(group.members) > 0:
                print "ERROR: Uppercase group {0} has edges. Members:{1}".format(email, group.members)
            else:
                print "ERROR: Uppercase group {0} exists with no members.".format(email)


emails = upper_to_lower(args.group)
find_upper_email_references(emails)