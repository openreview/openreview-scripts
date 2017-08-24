#!/usr/bin/python

###############################################################################
''' Assigns reviewers to papers - run in same directory as config.py
 ex. python assign-reviewers.py --baseurl http://localhost:3000
       --username admin --password admin_pw 'reviewer@gmail.com,3'

 Checks paper number valid.
 Check reviewer email address or domain is not on the conflicts list.
 Check reviewer is in the system.
 If reviewer is not in conference reviewers group (config.CONF/Reviewers), add it.
 If reviewer not already assigned to this paper:
	Determine AnonReviewer number
	Create Paper#/AnonReviewer#  group with this reviewer as a member
    Assign Paper#/AnonReviewer# to the Paper#/Reviewers group and
                                Paper#/Reviewers/NonReaders group for this paper'''
###############################################################################

## Import statements
import argparse
import csv
import sys
from openreview import *

## Argument handling
parser = argparse.ArgumentParser()
parser.add_argument('assignments', help="either (1) a csv file containing reviewer assignments or (2) a string of the format '<email_address>,<paper#>' e.g. 'reviewer@cs.umass.edu,23'")
parser.add_argument('--baseurl', help="base url")
parser.add_argument('--username')
parser.add_argument('--password')
args = parser.parse_args()

## Initialize the client library with username and password
client = Client(baseurl=args.baseurl, username=args.username, password=args.password)

submissions = client.get_notes(invitation=config.SUBMISSION)

## parses command line assignments - looks for pairs of emails and paper numbers
## full checks for valid paper numbers and email addresses done in assign reviewer
def parse_single_assigment(s):
    try:    
        email_addr = s.split(',')[0]
        paper_number = s.split(',')[1]

        try: 
            int(paper_number)
        except ValueError:
            return False

        if not '@' in email_addr:
            return False

        return True
    except IndexError:
        return False

# check if reviewer_email or reviewer's domains are on conflict list
def reviewer_conflicts(reviewer_email, paper_number, conflict_list):
    # check reviewer email as a whole is on the conflicts list
    if reviewer_email in conflict_list:
        print "Error: Reviewer \"" + reviewer_email + "\" is an author for Paper" + paper_number
        return True

    # if the reviewer email ends w/ .edu check it is on conflicts list
    name, domain = reviewer_email.split('@')
    if domain.endswith('.edu') and domain in conflict_list:
        print "Error: Reviewer \"" + reviewer_email + "\" email has conflicts for Paper" + paper_number
        return True

    return False

# Check email is in a valid format, then get user profile.
# Return None if fail to get profile.
def get_reviewer_profile(reviewer_email):
    valid_email = re.compile('^[^@\s,]+@[^@\s,]+\.[^@\s,]+$')
    if not valid_email.match(reviewer_email):
        print "Error: Reviewer \""+reviewer_email+"\" invalid. Please check for typos and whitespace."
        return None
    else:
        try:
            profile = client.get_profile(reviewer_email)
        except openreview.OpenReviewException as e:
            # generally user not found
            print("Error: Reviewer (%s): %s" % (reviewer_email, e))
            return None

        reviewer_tilde = profile.id
        if '~' not in reviewer_tilde:
            print "Something went wrong with reviewer at ", reviewer
            print "reviewer_tilde = ", reviewer_tilde
            return None
    return profile

def create_reviewer_group(new_reviewer_id, reviewer_email, conflict_list):
    print 'Creating reviewer: ', new_reviewer_id
    new_reviewer = Group(
        new_reviewer_id,
        signatures=[config.CONF],
        writers=[config.CONF],
        members=[reviewer_email],
        readers=[config.CONF,config.PROGRAM_CHAIRS,new_reviewer_id],
        nonreaders=conflict_list,
        signatories=[new_reviewer_id])
    client.post_group(new_reviewer)
    print "assigned user %s to group %s" % (reviewer_email, new_reviewer_id)
    return new_reviewer

# does some parameter checking, checks for conflicts
# check if reviewer already assigned to paper
# if not then create Anonymous group for the reviewer and add to reviewer group
def assign_reviewer(reviewer_email, paper_num):
    paper_number = str(paper_num)
    paper_group = config.CONF + '/Paper' + paper_number
    # check paper_number and reviewer email are valid
    notes = [note for note in submissions if str(note.number) == paper_number]
    if not notes:
        print "Error: Paper number " + paper_number + " does not exist"
        return
    note = notes[0]
    profile = get_reviewer_profile(reviewer_email)
    if profile is None:
        return

    print(note.content['title'])
    # create list of conflicts emails and add paper author to it
    # conflict_list is a copy (not a reference) to the submission conflicts
    conflict_list = []
    # If conflicts are a part of a submission, add them here
    if 'conflicts' in note.content:
        conflict_list.extend(note.content['conflicts'][:])
    # authors for this paper are not allowed to be in the reviewers groups
    if 'authorids' in note.content:
        conflict_list += note.content['authorids']

    if reviewer_conflicts(reviewer_email, paper_number, conflict_list):
        return

    # gets reviewers for given paper
    reviewers = client.get_group(paper_group + '/Reviewers')
    existing_reviewers = reviewers.members
    # adds the given reviewer to the conference reviewers if not already there
    conference_reviewers = client.get_group(config.CONF + '/Reviewers')
    if not (reviewer_email in conference_reviewers.members):
        client.add_members_to_group(conference_reviewers, reviewer_email)

    # Each reviewer gets it's own AnonReviewer Group.
    # The Anon group gets added to Paper#/Reviewers.
    # To determine if
    # determine what number AnonReviewer this new reviewer should be
    # by searching for largest AnonReviewer so far
    N = 0;
    for anon_name in existing_reviewers:
        existing_reviewer = client.get_group(anon_name)

        # check if reviewer is already in the group by looking for given reviewer email, or associated ~name
        if hasattr(existing_reviewer, 'members'):
            if reviewer_email in existing_reviewer.members:
                print "Reviewer " + reviewer_email + " found in " + existing_reviewer.id
                return existing_reviewer
            reviewer_tilde = profile.id
            if reviewer_tilde in existing_reviewer.members:
                print "Reviewer " + reviewer_tilde + " found in " + existing_reviewer.id
                return existing_reviewer

        # anon_name isn't the given reviewer - check for the Anon number
        reviewer_number = int(anon_name.split('AnonReviewer')[1])
        if reviewer_number > N:
            N = reviewer_number

    # reviewer not in current group
    # create new group for this new reviewer with Anon name
    anon_reviewer_id = paper_group + '/AnonReviewer' + str(N + 1)

    # add that to the existing reviewers group and the NonReaders group
    new_reviewer = create_reviewer_group(anon_reviewer_id, reviewer_email, conflict_list)
    client.add_members_to_group(reviewers, anon_reviewer_id)
    ## reviewers are blocked from other reviews until complete
    client.add_members_to_group(client.get_group(paper_group + '/Reviewers/NonReaders'), new_reviewer_id)


##################################################################


if args.assignments.endswith('.csv'):   
    with open(args.assignments, 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in reader:
            reviewer_email = row[0]
            paper_number = row[1]
            assign_reviewer(reviewer_email,paper_number)
elif parse_single_assigment(args.assignments):
    reviewer_email = args.assignments.split(',')[0]
    paper_number = args.assignments.split(',')[1]
    assign_reviewer(reviewer_email,paper_number)
else:
    print "Invalid input. Need csv file or '<email_address>,<paper#>'"
    sys.exit()
