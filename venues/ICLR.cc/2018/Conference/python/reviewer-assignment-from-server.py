'''
this is a one-time script to run the assignment directly from the server (because it's too slow to run it over the network)
'''

## Import statements
import argparse
import sys
import config
import csv
import openreview

## Argument handling
parser = argparse.ArgumentParser()
parser.add_argument('noteid')
parser.add_argument('tpms_file', help='should be iclr18_reviewer_assignments_1106(from_tpms).csv')
parser.add_argument('--baseurl', help="base url")
parser.add_argument('--username')
parser.add_argument('--password')

args = parser.parse_args()

client = openreview.Client(baseurl=args.baseurl, username=args.username, password=args.password)

submissions = client.get_notes(invitation=config.BLIND_SUBMISSION)
reviewergroup_by_number = {}
for paper in submissions:
    paper_num = str(paper.number)
    paperinv = config.CONF + '/-/Paper' + paper_num
    print("Adding groups for Paper"+ paper_num)
    paperGroup = config.CONF + '/Paper' + paper_num
    authorGroup = paperGroup + '/Authors'

    ## Reviewer group - people that can see the review invitation
    reviewerGroup = paperGroup + '/Reviewers'
    reviewerGroup_posted = client.post_group(openreview.Group(
        id=reviewerGroup,
        signatures=[config.CONF],
        writers=[config.CONF],
        members=[],
        readers=[config.CONF, config.PROGRAM_CHAIRS, config.AREA_CHAIRS],
        nonreaders=[authorGroup],
        signatories=[]))

    reviewergroup_by_number['Paper{0}'.format(paper_num)] = reviewerGroup_posted

    ## Area Chair group -
    areachairGroup = paperGroup + '/Area_Chair'
    client.post_group(openreview.Group(
        id=areachairGroup,
        signatures=[config.CONF],
        writers=[config.CONF],
        members=[],
        readers=[config.CONF, config.PROGRAM_CHAIRS, config.AREA_CHAIRS, areachairGroup],
        nonreaders=[authorGroup],
        signatories=[areachairGroup]))


# populate a configuration note with the TPMS assignments
configuration_note = client.get_note(args.noteid)

def tpms_assignment(configuration_note):
    configuration_note.content['assignments'] = { 'Paper{0}'.format(n.number): {'assigned':[], 'forum':n.forum, 'title':n.content['title']} for n in submissions}
    with open(args.tpms_file) as f:
        reader = csv.reader(f)
        headers = reader.next()
        print headers
        assignment_id_by_email = {}
        for paper_number, email, _ in reader:
            if email not in assignment_id_by_email:
                try:
                    profile = client.get_profile(email)
                    assignment_id_by_email[email] = profile.id
                except openreview.OpenReviewException as e:
                    assignment_id_by_email[email] = email

            paper_id = 'Paper{0}'.format(paper_number)
            if paper_id in configuration_note.content['assignments']:
                assignment_entry = configuration_note.content['assignments'][paper_id]
                assignment_entry['assigned'].append(assignment_id_by_email[email])

    return configuration_note

assignment_note = tpms_assignment(configuration_note)

# generate paper reviewer groups with reviewer-groups.py

# remember to enable official review invitations

for paper_number, assignment in assignment_note.content['assignments'].iteritems():
    print paper_number
    if assignment_note.content['configuration']['group'] == config.REVIEWERS:
        paper_reviewer_group = reviewergroup_by_number[paper_number]
        for reviewer_number, reviewer in enumerate(assignment['assigned']):
            anon_id = '{0}/{1}/AnonReviewer{2}'.format(config.CONF, paper_number, reviewer_number+1)
            paper_authors = '{0}/{1}/Authors'.format(config.CONF, paper_number)

            anonymous_reviewer_group = openreview.Group(
                id = anon_id,
                readers = [config.CONF, config.AREA_CHAIRS, config.PROGRAM_CHAIRS, anon_id],
                nonreaders = [paper_authors],
                writers = [config.CONF],
                signatories = [anon_id],
                signatures = [config.CONF],
                members = [reviewer])

            client.add_members_to_group(paper_reviewer_group, reviewer)
            client.post_group(anonymous_reviewer_group)
