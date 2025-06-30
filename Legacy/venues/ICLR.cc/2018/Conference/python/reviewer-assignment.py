import argparse
import openreview
import config

# Argument handling
parser = argparse.ArgumentParser()
parser.add_argument('id', help = "the note ID of the assignment")
parser.add_argument('--username')
parser.add_argument('--password')
parser.add_argument('--baseurl', help = "base URL")
args = parser.parse_args()

client = openreview.Client(username=args.username, password=args.password, baseurl=args.baseurl)

assignment_note = client.get_note(args.id)


for paper_number, assignment in assignment_note.content['assignments'].iteritems():
    if assignment_note.content['configuration']['group'] == config.REVIEWERS:
        paper_reviewer_group = client.get_group('{0}/{1}/Reviewers'.format(config.CONF, paper_number))
        client.remove_members_from_group(paper_reviewer_group, paper_reviewer_group.members)
        for reviewer_number, reviewer in enumerate(assignment['assigned']):
            anonymous_reviewer_group = client.get_group('{0}/{1}/AnonReviewer{2}'.format(config.CONF, paper_number, reviewer_number+1))
            print "assigning reviewer {0} to {1}".format(reviewer, anonymous_reviewer_group.id)
            client.remove_members_from_group(anonymous_reviewer_group, anonymous_reviewer_group.members)
            client.add_members_to_group(anonymous_reviewer_group, reviewer)
            client.add_members_to_group(paper_reviewer_group, reviewer)

    if assignment_note.content['configuration']['group'] == config.AREA_CHAIRS:
        paper_areachair_group = client.get_group('{0}/{1}/Area_Chair'.format(config.CONF, paper_number))
        client.remove_members_from_group(paper_areachair_group, paper_areachair_group.members)
        client.add_members_to_group(paper_areachair_group, assignment['assigned'])
        print "assigning area chair {0} to {1}".format(assignment['assigned'][0], paper_areachair_group.id)
