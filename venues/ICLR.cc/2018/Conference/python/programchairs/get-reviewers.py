#!/usr/bin/python

###############################################################################
# get-reviewers.py
# -n print reviewers for specified paper
# -u print papers assigned to specified reviewer
# -a print all papers and reviewers to specified file (one paper/reviewer pair per line)
# -p print all papers and reviewers to specified file (one paper, all reviewers per line)
# -r print all reviewers and paper numbers to specified file (one review, all paper numbers per line)
# -i print all reviewers: email, firstname, lastname, middleinitial, institution
###############################################################################

## Import statements
import argparse
import csv
import re
from openreview import *

## Argument handling
parser = argparse.ArgumentParser()
parser.add_argument('-n', '--paper_number', help="the number of the paper to assign this reviewer to")
parser.add_argument('-u', '--user',help="the user whose reviewing assignments you would like to see")
parser.add_argument('-a', '--all',help="specify an output file to save all the reviewer assignments")
parser.add_argument('-p', '--papers',help="specify an output file to save all paper numbers and assigned reviewers for each")
parser.add_argument('-r', '--reviewers',help="specify an output file to save all reviewers and his/her paper assignments")
parser.add_argument('-i', '--info',help="specify a CSV output file to save all reviewers: email, firstname, lastname, middleinitial, institution")
parser.add_argument('--baseurl', help="base url")
parser.add_argument('--username')
parser.add_argument('--password')
args = parser.parse_args()

## Initialize the client library with username and password
openreview = Client(baseurl=args.baseurl, username=args.username, password=args.password)
baseurl = openreview.baseurl

# pull information out of profile and store it in profile_info
def load_profile_info(profile, profile_info):
    # if this id isn't in profile_info
    if not any(d['id'] == profile['id'] for d in profile_info):
        info = {}
        info['id']=profile['id']
        info['first'] = profile['content']['names'][0]['first']
        if len(profile['content']['names'][0]['middle']) > 0:
            info['mi'] = profile['content']['names'][0]['middle'][0]
        else:
            info['mi'] = " "
        info['last'] = profile['content']['names'][0]['last']

        # if preferred email isn't set, use email from form
        if profile['content']['preferred_email'] != "":
            info['email'] = profile['content']['preferred_email']
        else:
            info['email'] = profile['content']['emails'][0]

        # check for most recent entry in history
        end_date = 0
        info['institute'] = ""
        for entry in profile['content']['history']:
            if entry['end'] > end_date:
                end_date = entry['end']
                info['institute'] = entry['institution']['name']
        profile_info.append(info)
    return profile_info


if args.paper_number != None:

    paper_number = args.paper_number
    notes = openreview.get_notes(invitation = 'ICLR.cc/2018/Conference/-/Blind_Submission', number = paper_number)

    if len(notes) > 0:
        note = notes[0]
        reviewers = openreview.get_group('ICLR.cc/2018/Conference/Paper' + str(note.number) + '/Reviewers');
        area_chairs = openreview.get_groups('ICLR.cc/2018/Conference/Paper' + str(note.number) + '/Area_Chair')
        print "Area Chair: {0}".format(area_chairs[0].members[0])
        print "Reviewers: {0}".format(reviewers.members)

    else:
        print "Paper number not found", paper_number

if args.user != None:

    user = args.user
    try:
        reviewers = openreview.get_groups(member = user, regex = 'ICLR.cc/2018/Conference/Paper[0-9]+/Reviewers')

        if len(reviewers):
            for reviewer in reviewers:
                paperNumber = reviewer.id.split('Paper')[1].split('/Reviewers')[0]
                print paperNumber
        else:
            print "No paper assigned to reviewer", user
    except Exception as ex:
        print "Can not the groups for", user


if args.all != None:
    # print paper number and reviewer id on each line
    with open(args.all, 'wb') as outfile:

        csvwriter = csv.writer(outfile, delimiter=',')

        notes = openreview.get_notes(invitation = 'ICLR.cc/2018/Conference/-/Blind_Submission')
        assignments = openreview.get_groups(id = 'ICLR.cc/2018/Conference/Paper.*/Reviewers')

        assignments_by_paper = {}
        for a in assignments:
            paper_number = a.id.split('Paper')[1].split('/Reviewers')[0]
            assignments_by_paper[paper_number] = a.members

        for n in notes:
            key = str(n.number)
            if key in assignments_by_paper.keys():
                reviewers = assignments_by_paper[key]
                for reviewer in reviewers:
                    row = []
                    row.append(key)
                    row.append(reviewer.encode('utf-8'))
                    csvwriter.writerow(row)
            else:
                row = []
                row.append(n.number)
                row.append('None')
                csvwriter.writerow(row)

if args.papers:
    # print paper number, number of reviewers and lists reviewers
    with open(args.papers, 'wb') as outfile:

        csvwriter = csv.writer(outfile, delimiter=',')

        notes = openreview.get_notes(invitation='ICLR.cc/2018/Conference/-/Blind_Submission')
        assignments = openreview.get_groups(id='ICLR.cc/2018/Conference/Paper.*/Reviewers')
        area_chairs = openreview.get_groups(id='ICLR.cc/2018/Conference/Paper.*/Area_Chair')

        assignments_by_paper = {}
        for a in assignments:
            paper_number = a.id.split('Paper')[1].split('/Reviewers')[0]
            assignments_by_paper[paper_number] = {}
            assignments_by_paper[paper_number]['reviewers'] = a.members
            assignments_by_paper[paper_number]['AC'] = ""

        for ac in area_chairs:
            paper_number = ac.id.split('Paper')[1].split('/Area_Chair')[0]
            if paper_number in assignments_by_paper:
                if ac.members:
                    assignments_by_paper[paper_number]['AC'] = ac.members[0]
                else:
                    print "Empty members "+ac.id
            else:
                print "Papernum missing "+ str(paper_number)
                # print paper, number of reviewers, reviewer ids
        row = ['Paper #', 'Area Chair','Number of Reviewers','Reviewer1', 'Reviewer2', 'Reviewer3']
        csvwriter.writerow(row)
        for n in notes:
            key = str(n.number)
            row = []
            row.append(key)
            if key in assignments_by_paper.keys():
                reviewers = assignments_by_paper[key]['reviewers']
                row.append(assignments_by_paper[key]['AC'].encode('utf-8'))
                row.append(len(reviewers))
                for reviewer in reviewers:
                    row.append(reviewer.encode('utf-8'))

            else:
                row.append('0')

            csvwriter.writerow(row)

if args.reviewers:
    # print to file reviewer, number of papers assigned and list of paper numbers
    with open(args.reviewers, 'wb') as outfile:

        csvwriter = csv.writer(outfile, delimiter=',')

        notes = openreview.get_notes(invitation='ICLR.cc/2018/Conference/-/Blind_Submission')
        assignments = openreview.get_groups(id='ICLR.cc/2018/Conference/Paper.*/Reviewers')
        all_reviewers = openreview.get_group(id = 'ICLR.cc/2018/Conference/Reviewers')

        papers_by_reviewer = {}
        for reviewer in all_reviewers.members:
            if reviewer not in papers_by_reviewer:
                papers_by_reviewer[reviewer] = []

        for a in assignments:
            paper_number = a.id.split('Paper')[1].split('/Reviewers')[0]
            for reviewer in a.members:
                if reviewer not in papers_by_reviewer:
                    papers_by_reviewer[reviewer] = []
                papers_by_reviewer[reviewer].append(paper_number)

        # print reviewer, number of papers
        row = ['Reviewer','Number of Papers', 'Paper #']
        csvwriter.writerow(row)
        for key in papers_by_reviewer.keys():
            row = []
            row.append(key.encode('utf-8'))
            row.append(len(papers_by_reviewer[key]))
            row.extend(papers_by_reviewer[key])
            csvwriter.writerow(row)

if args.info:

    # get list of all reviewers
    reviewer_groups = openreview.get_groups(id='ICLR.cc/2018/Conference/-/Paper.*/Reviewers')
    reviewers = []
    for group in reviewer_groups:
        reviewers.extend(group.members)
    # remove duplicates
    reviewers = list(set(reviewers))

    # separate into emails and tilde_ids
    emails = []
    tilde_ids = []
    tildematch = re.compile('~.+')
    for reviewer in reviewers:
        if tildematch.match(reviewer):
            tilde_ids.append(reviewer)
        else:
            emails.append(reviewer)

    # get tilde_id profiles
    profile_info = []
    tilde_response = openreview.get_profiles(tilde_ids)
    for profile in tilde_response:
        profile_info = load_profile_info(profile, profile_info)

    # get email profiles
    email_response = openreview.get_profiles(emails)
    for profile in email_response:
        profile_info = load_profile_info(profile['profile'], profile_info)

    # sort on last name, first name
    profile_info = sorted(profile_info, key=lambda k:k['first'])
    profile_info = sorted(profile_info, key=lambda k:k['last'])

    with open(args.info, 'wb') as outfile:
        csvwriter = csv.writer(outfile, delimiter=',')

        # write the header
        header = ['Email', 'First Name','Last Name', 'Middle Initial','Institution']
        csvwriter.writerow(header)
        # print results
        for profile in profile_info:
            row = []
            row.append(profile['email'])
            row.append(profile['first'].encode('utf-8'))
            row.append(profile['last'].encode('utf-8'))
            row.append(profile['mi'].encode('utf-8'))
            row.append(profile['institute'].encode('utf-8'))
            csvwriter.writerow(row)

