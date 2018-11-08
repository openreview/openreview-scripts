## Import statements
import argparse
import sys
import csv
import openreview
import re

'''
Requirements:

1. openreview-py
2. User running this script should have read & write permissions over Reviewers, Reviewers/Unsubmitted 
& AnonReviewer[integer] groups

Usage:

Use the --paper (-p) flag to specify the paper number.
Use the --add (-a) flag to specify a username or email address to assign.
Use the --remove (-r) flag to specify a username or email address to remove.

The script processes removals before additions, and assigns the user to the
lowest AnonReviewer# group that is empty.

For example, after running the following:

python assign-reviewer.py --paper 123 --remove ~Oriol_Vinyals1 --add ~MarcAurelio_Ranzato1
or
python assign-reviewer.py --p 123 --r ~Oriol_Vinyals1 --a ~MarcAurelio_Ranzato1

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
conference = 'AKBC.ws/2019/Conference'

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

    
    paperUrl = conference + "/Paper{}".format(paper_number)
    unsubmittedGroupId = paperUrl + "/Reviewers/Unsubmitted"
    anonReviewerRegex = re.compile(paperUrl+"/AnonReviewer.*")

    if reviewer_to_remove :
        if '@' in reviewer_to_remove:
            reviewer_to_remove = reviewer_to_remove.lower()
        
        (user,changed_groups_rem) = openreview.tools.remove_assignment(client, paper_number, conference, reviewer_to_remove)
        reviewer_to_remove = user
        
        anonReviewerGroup = next(filter(anonReviewerRegex.match,changed_groups_rem), None)
        if anonReviewerGroup:
            client.remove_members_from_group(client.get_group(unsubmittedGroupId),anonReviewerGroup)
        changed_groups_rem.append(unsubmittedGroupId)
        
        for grp in changed_groups_rem:
            print("{:40s} removed from --> {}".format(reviewer_to_remove, grp))

    if reviewer_to_add :
        if '@' in reviewer_to_add:
            reviewer_to_add = reviewer_to_add.lower()
        
        (user,changed_groups_add) = openreview.tools.add_assignment(client, paper_number, conference, reviewer_to_add,
                            individual_group_params = {'readers': [
                            conference,
                            conference + '/Program_Chairs',
                            conference + '/Paper{}/Area_Chairs'.format(paper_number)
                            ]})
        reviewer_to_add = user
        
        anonReviewerGroup = next(filter(anonReviewerRegex.match,changed_groups_add), "")
        if anonReviewerGroup:
            client.add_members_to_group(client.get_group(unsubmittedGroupId),anonReviewerGroup)
        changed_groups_add.append(unsubmittedGroupId)
        
        for grp in changed_groups_add:
            print("{:40s} added to --> {}".format(reviewer_to_add, grp))
