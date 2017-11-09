## Import statements
import argparse
import sys
import csv
import openreview

'''
Usage:

python assign-reviewer.py --paper 1123 --add ~Michael_Spector1 --remove ~Melisa_Bok1
python assign-reviewer.py --paper 1123

'''

## Argument handling
parser = argparse.ArgumentParser()
parser.add_argument('-p','--paper', required=True)
parser.add_argument('-a','--add')
parser.add_argument('-r','--remove')
parser.add_argument('--baseurl', help="base url")
parser.add_argument('--username')
parser.add_argument('--password')

args = parser.parse_args()

client = openreview.Client(baseurl=args.baseurl, username=args.username, password=args.password)

paper_number = args.paper
reviewer_to_remove = args.remove
reviewer_to_add = args.add

reviewers_group = client.get_group('ICLR.cc/2018/Conference/Paper{0}/Reviewers'.format(paper_number))
anonreviewer_groups = client.get_groups(id = 'ICLR.cc/2018/Conference/Paper{0}/AnonReviewer.*'.format(paper_number))
empty_anonreviewer_groups = sorted([ a for a in anonreviewer_groups if a.members == [] ], key=lambda x: x.id)

def next_anonreviewer_id(empty_anonreviewer_groups):
    if len(empty_anonreviewer_groups) > 0:
        anonreviewer_group = empty_anonreviewer_groups[0]
        empty_anonreviewer_groups.remove(anonreviewer_group)
        return anonreviewer_group.id
    else:
        anonreviewer_group_ids = [g.id for g in anonreviewer_groups]

        # reverse=True lets us get the AnonReviewer group with the highest index
        highest_anonreviewer_id = sorted(anonreviewer_group_ids, reverse=True)[0]

        # find the number of the highest anonreviewer group
        highest_anonreviewer_index = highest_anonreviewer_id[-1]
        return 'ICLR.cc/2018/Conference/Paper{0}/AnonReviewer{1}'.format(paper_number, int(highest_anonreviewer_index)+1)


if reviewer_to_remove:
    assigned_anonreviewer_groups = [a for a in anonreviewer_groups if reviewer_to_remove in a.members]
    for anonreviewer_group in assigned_anonreviewer_groups:
        print "removing {0} from {1}".format(reviewer_to_remove, anonreviewer_group.id)
        client.remove_members_from_group(anonreviewer_group, reviewer_to_remove)
        empty_anonreviewer_groups.append(anonreviewer_group)
        empty_anonreviewer_groups = sorted(empty_anonreviewer_groups, key=lambda x: x.id)
    print "removing {0} from {1}".format(reviewer_to_remove, reviewers_group.id)
    client.remove_members_from_group(reviewers_group, reviewer_to_remove)

if reviewer_to_add:
    anonreviewer_id = next_anonreviewer_id(empty_anonreviewer_groups)
    paper_authors = 'ICLR.cc/2018/Conference/Paper{0}/Authors'.format(paper_number)

    anonymous_reviewer_group = openreview.Group(
        id = anonreviewer_id,
        readers = [
            'ICLR.cc/2018/Conference',
            'ICLR.cc/2018/Conference/Area_Chairs',
            'ICLR.cc/2018/Conference/Program_Chairs',
            anonreviewer_id
            ],
        nonreaders = [
            paper_authors
            ],
        writers = ['ICLR.cc/2018/Conference'],
        signatories = [anonreviewer_id],
        signatures = ['ICLR.cc/2018/Conference'],
        members = [reviewer_to_add])

    print "adding {0} to {1}".format(reviewer_to_add, anonymous_reviewer_group.id)
    client.post_group(anonymous_reviewer_group)
    print "adding {0} to {1}".format(reviewer_to_add, reviewers_group.id)
    client.add_members_to_group(reviewers_group, reviewer_to_add)
