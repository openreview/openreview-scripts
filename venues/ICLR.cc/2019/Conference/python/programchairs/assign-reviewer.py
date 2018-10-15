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

    conference = 'ICLR.cc/2019/Conference'
    paperUrl = "ICLR.cc/2019/Conference/Paper{}".format(paper_number)
    unsubmittedGroupId = paperUrl + "/Reviewers/Unsubmitted"
    anonReviewerRegex = re.compile(paperUrl+"/AnonReviewer.*")

    if reviewer_to_remove :
        if '@' in reviewer_to_remove:
            reviewer_to_remove = reviewer_to_remove.lower()
        
        (user,changed_groups_rem) = openreview.tools.remove_assignment(client, paper_number, conference, reviewer_to_remove,
                                            parent_group_params = {},
                                            parent_label = 'Reviewers',
                                            individual_label = 'AnonReviewer')
        reviewer_to_remove = user
        anonReviewerGroup = ""
        
        try:
            anonReviewerGroup = [grp for grp in changed_groups_rem if anonReviewerRegex.match(str(grp))][0]
        except IndexError as e:
            pass
        
        client.remove_members_from_group(client.get_group(unsubmittedGroupId),anonReviewerGroup)
        changed_groups_rem.append(unsubmittedGroupId)
        
        for grp in changed_groups_rem:
            print("{:40s} removed from --> {}".format(reviewer_to_remove, grp))

    if reviewer_to_add :
        if '@' in reviewer_to_add:
            reviewer_to_add = reviewer_to_add.lower()
        
        (user,changed_groups_add) = openreview.tools.add_assignment(client, paper_number, conference, reviewer_to_add,
                            parent_group_params = {}, individual_group_params = {'readers': [
                            'ICLR.cc/2019/Conference',
                            'ICLR.cc/2019/Conference/Program_Chairs',
                            'ICLR.cc/2019/Conference/Paper{}/Area_Chairs'.format(paper_number)
                            ]}, 
                            parent_label = 'Reviewers', 
                            individual_label = 'AnonReviewer')
        reviewer_to_add = user
        anonReviewerGroup = ""
        
        try:
            anonReviewerGroup = [grp for grp in changed_groups_add if anonReviewerRegex.match(str(grp))][0]
        except IndexError as e:
            pass
        
        client.add_members_to_group(client.get_group(unsubmittedGroupId),anonReviewerGroup)
        changed_groups_add.append(unsubmittedGroupId)
        
        for grp in changed_groups_add:
            print("{:40s} added to --> {}".format(reviewer_to_add, grp))
