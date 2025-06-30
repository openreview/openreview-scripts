#!/usr/bin/python

###############################################################################
# ex. python replace-emails-with-tilde.py --conf MyConf.org/2017 --baseurl http://localhost:3000
#       --username admin --password admin_pw
#
# To be run to refresh author groups in case of revisions and/or withdrawals
# Expects config to define BLIND_SUBMISSION, SUBMISSION and AUTHORS as well
# as an Authors group for each SUBMISSION paper
###############################################################################

## Import statements
import argparse
import sys
import config
from openreview import *

## Argument handling
parser = argparse.ArgumentParser()
parser.add_argument('group',  help = "the group to replace")
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
    target_group = client.get_group(group_name)
    upper_emails = []
    lower_emails = []
    for email in target_group.members:
        if '@' in email:
            ### find emails with uppercase
            if has_uppercase(email):
                ## has uppercase chars, convert to lowercase
                print email
                lower = email.lower()
                upper_emails.append(email)
                lower_emails.append(lower)
    ### replace uppercase w/ lowercase emails
    client.remove_members_from_group(target_group,upper_emails)
    client.add_members_to_group(target_group, lower_emails)
    return upper_emails


def find_upper_email_references(upper_emails, verbose=False):
    ## try to get profile via email
    ## if get one, check that lower exists and set to that group instead
    for email in upper_emails:
        profile = get_profile(email)
        if profile != None:
            print "ERROR: Uppercase profile for {0} with id {1}".format(email, profile.id)
        group = get_group(email)
        if group != None:
            lower = email.lower()
            lower_group = get_group(lower)
            if lower_group != None:
                if verbose:
                    print "Upper and lowercase group {0} exists. Members:{1}".format(lower, group.members)
            else:
                print "ERROR: Uppercase with no lowercase group {0} exists. Members:{1}".format(email, group.members)

### convert emails to profiles when available
def emails_to_profiles(group_name):
    add_names = []
    remove_emails = []
    target_group = client.get_group(group_name)
    for email in target_group.members:
        try:
            profile = client.get_profile(email)
            add_names.append(profile.id)
            remove_emails.append(email)
            print "found profile "+email
        except openreview.OpenReviewException as e:
            # ~id doesn't exist, so no change needed
            print "NO profile "+email
            pass

    ### replace emails w/ profile names
    client.remove_members_from_group(target_group, remove_emails)
    client.add_members_to_group(target_group, add_names)


#### MAIN #####

emails = upper_to_lower(args.group)
find_upper_email_references(emails)
emails_to_profiles(args.group)