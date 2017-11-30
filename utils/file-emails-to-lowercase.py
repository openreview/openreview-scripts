#!/usr/bin/python

###############################################################################
# ex. python file-emails-to-lowercase.py -file reviewers.csv --baseurl http://localhost:3000
#       --username admin --password admin_pw
#
# Finds groups or profiles that use upper case emails as listed in the file.
# The csv file is expected to list first name, last name, email.
###############################################################################

## Import statements
import argparse
import csv
from openreview import *

## Argument handling
parser = argparse.ArgumentParser()
parser.add_argument('-f','--file', required=True, help = "the full path of the file with the names and emails")
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

## Uses csv file with first name, last name, email
# flags all uppercase profiles
with open(args.file, 'rb') as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='|')
    # skip header row
    next(reader, None)
    for row in reader:
        email = row[2]
        twiddle_name = '~'+row[0]+'-'+row[1]+'1'
        ### find emails with uppercase
        if '@' in email and has_uppercase(email):
            upper_profile = get_profile(email)
            if upper_profile != None:
                ## profiles should only use lowercase email
                ## this profile shouldn't exist
                print "ERROR: Uppercase profile for {0} with id {1}".format(email, upper_profile.id)
            else:
                upper_group = get_group(email)
                if upper_group != None:
                    print "Delete group: {0} with members: {1}".format(upper_group.id, upper_group.members)

        # get all profiles
        # for all names, get profiles, check if refer to uppercase emails (they shouldn't at this point)
        # if they do, flag duplicates if lower profile exists
        name_profile = get_profile(twiddle_name)
        if name_profile != None:
            for name in members:
                ## for all uppercase member emails
                if '@' in name and has_upper(name):
                    print "ERROR: Uppercase profile with id {0}".format(profile.id)
                    lower_email = name.lower()
                    lower_profile = get_profile(lower_email)
                    if lower_profile != None and lower_profile.id != name_profile.id:
                        print "    Could be duplicate - upper: {0} lower: {1}".format(name_profile.id, lower_profile.id)