## Import statements
import argparse
import sys
import csv
import openreview


'''

Requirements:

openreview-py

Usage:

Use the --paper (-p) flag to specify the paper number.
Use the --add (-a) flag to specify a username or email address to assign.
Use the --remove (-r) flag to specify a username or email address to remove.

The script processes removals before additions, and assigns the user to the
lowest AnonReviewer# group that is empty.

For example, after running the following:

python assign-reviewer.py --paper 123 --remove ~Oriol_Vinyals1 --add ~MarcAurelio_Ranzato1


Paper123/Reviewers = {
    AnonReviewer1: ~Tara_Sainath1
    AnonReviewer2: ~Oriol_Vinyals1
    AnonReviewer3: ~Iain_Murray1
}

becomes

Paper123/Reviewers = {
    AnonReviewer1: ~Tara_Sainath1
    AnonReviewer2: ~MarcAurelio_Ranzato1
    AnonReviewer3: ~Iain_Murray1
}


'''

def next_anonreviewer_id(empty_anonreviewer_groups, full_anonreviewer_groups, paper_number):
    if len(empty_anonreviewer_groups) > 0:
        anonreviewer_group = empty_anonreviewer_groups[0]
        empty_anonreviewer_groups.remove(anonreviewer_group)
        return anonreviewer_group.id
    elif len(full_anonreviewer_groups) > 0:
        anonreviewer_group_ids = [g.id for g in full_anonreviewer_groups]

        # reverse=True lets us get the AnonReviewer group with the highest index
        highest_anonreviewer_id = sorted(anonreviewer_group_ids, reverse=True)[0]

        # find the number of the highest anonreviewer group
        highest_anonreviewer_index = highest_anonreviewer_id[-1]
        return 'ICLR.cc/2018/Workshop/Paper{0}/AnonReviewer{1}'.format(paper_number, int(highest_anonreviewer_index)+1)
    else:
        return 'ICLR.cc/2018/Workshop/Paper{0}/AnonReviewer1'.format(paper_number)

def assign(client, paper_number, reviewer_to_add=None, reviewer_to_remove=None):
    try:
        reviewers_group = client.get_group('ICLR.cc/2018/Workshop/Paper{0}/Reviewers'.format(paper_number))
    except openreview.OpenReviewException as e:
        if e[0][0]['type'] == 'Not Found':
            reviewers_group = client.post_group(openreview.Group(**{
                'id': 'ICLR.cc/2018/Workshop/Paper{0}/Reviewers'.format(paper_number),
                'readers': ['ICLR.cc/2018/Workshop', 'ICLR.cc/2018/Workshop/Program_Chairs'],
                'nonreaders': ['ICLR.cc/2018/Workshop/Paper{0}/Authors'.format(paper_number)],
                'members': [],
                'writers': ['ICLR.cc/2018/Workshop', 'ICLR.cc/2018/Workshop/Program_Chairs'],
                'signatures': ['ICLR.cc/2018/Workshop'],
                'signatories': []
            }))
        else:
            raise e

    anonreviewer_groups = client.get_groups(id = 'ICLR.cc/2018/Workshop/Paper{0}/AnonReviewer.*'.format(paper_number))
    empty_anonreviewer_groups = sorted([ a for a in anonreviewer_groups if a.members == [] ], key=lambda x: x.id)

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
        paper = client.get_notes(invitation='ICLR.cc/2018/Workshop/-/Submission', number=paper_number)[0]

        user_domain_conflicts, user_relation_conflicts = openreview.tools.get_profile_conflicts(client, reviewer_to_add)
        paper_domain_conflicts, paper_relation_conflicts = openreview.tools.get_paper_conflicts(client, paper)

        domain_conflicts = paper_domain_conflicts.intersection(user_domain_conflicts)
        relation_conflicts = paper_relation_conflicts.intersection(user_relation_conflicts)

        if domain_conflicts:
            print "{:40s} XXX User has COI with the following domain: {}".format(reviewer_to_add, domain_conflicts)
        if relation_conflicts:
            print "{:40s} XXX User has COI with the following relation: {}".format(reviewer_to_add, relation_conflicts)

        if domain_conflicts or relation_conflicts:
            user_continue = raw_input('continue with assignment? y/[n]: ').lower() == 'y'
        else:
            user_continue = True

        if user_continue and reviewer_to_add not in reviewers_group.members:
            anonreviewer_id = next_anonreviewer_id(empty_anonreviewer_groups, anonreviewer_groups, paper_number)
            paper_authors = 'ICLR.cc/2018/Workshop/Paper{0}/Authors'.format(paper_number)
            anonymous_reviewer_group = openreview.Group(
                id = anonreviewer_id,
                readers = [
                    'ICLR.cc/2018/Workshop',
                    'ICLR.cc/2018/Workshop/Program_Chairs',
                    anonreviewer_id
                    ],
                nonreaders = [
                    paper_authors
                    ],
                writers = ['ICLR.cc/2018/Workshop'],
                signatories = [anonreviewer_id],
                signatures = ['ICLR.cc/2018/Workshop'],
                members = [reviewer_to_add])

            print "{:40s} --> {}".format(reviewer_to_add, anonymous_reviewer_group.id)
            client.post_group(anonymous_reviewer_group)
            client.add_members_to_group(reviewers_group, reviewer_to_add)
            return True
        elif reviewer_to_add in reviewers_group.members:
            print "{:40s} === {}".format(reviewer_to_add, reviewers_group.id)
            return True
        else:
            print "aborting assignment."
            return False

if __name__ == "__main__":
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

    if reviewer_to_remove and '@' in reviewer_to_remove:
        reviewer_to_remove = reviewer_to_remove.lower()

    if reviewer_to_add and '@' in reviewer_to_add:
        reviewer_to_add = reviewer_to_add.lower()

    assign(client, paper_number, reviewer_to_add=reviewer_to_add, reviewer_to_remove=reviewer_to_remove)
