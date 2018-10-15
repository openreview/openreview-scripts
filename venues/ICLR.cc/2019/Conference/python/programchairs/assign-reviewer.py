## Import statements
import argparse
import sys
import csv
import openreview
import re

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
    
    (user,changed_groups) = openreview.tools.assign(client, paper_number, 'ICLR.cc/2019/Conference',
        individual_group_params = {'readers': [
            'ICLR.cc/2019/Conference',
            'ICLR.cc/2019/Conference/Program_Chairs',
            'ICLR.cc/2019/Conference/Paper{}/Area_Chairs'.format(paper_number)
            ]},
        reviewer_to_add = reviewer_to_add,
        reviewer_to_remove = reviewer_to_remove,
        parent_label = 'Reviewers',
        individual_label = 'AnonReviewer')

    userInUnsubmitted = 0
    paperUrl = "ICLR.cc/2019/Conference/Paper{}".format(paper_number)
    unsubmittedGroupId = paperUrl + "/Reviewers/Unsubmitted"
    anonReviewerRegex = re.compile(paperUrl+"/AnonReviewer.*")
    anonReviewerGroup = ""

    try:
        anonReviewerGroup = [grp for grp in changed_groups if anonReviewerRegex.match(str(grp))][0]
    except Exception as e:
        pass

    if anonReviewerGroup and (anonReviewerGroup in client.get_group(id=unsubmittedGroupId).members):
        userInUnsubmitted = 1
    
    if reviewer_to_remove:
        if userInUnsubmitted and anonReviewerGroup:
            client.remove_members_from_group(client.get_group(unsubmittedGroupId),anonReviewerGroup)
            changed_groups.append(unsubmittedGroupId)
        if not changed_groups:
            print("{:40s} is already not a part of any groups for Paper --> {}".format(user, paper_number))
        for grp in changed_groups:
            print("{:40s} removed from --> {}".format(user, grp))
    elif reviewer_to_add:
        if not userInUnsubmitted and anonReviewerGroup:
            client.add_members_to_group(client.get_group(unsubmittedGroupId),anonReviewerGroup)
            changed_groups.append(unsubmittedGroupId)
        for grp in changed_groups:
            print("{:40s} added to --> {}".format(user, grp))
