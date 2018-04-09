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

    openreview.tools.assign(client, paper_number, 'auai.org/UAI/2018',
        individual_group_params = {'readers': [
            'auai.org/UAI/2018',
            'auai.org/UAI/2018/Program_Chairs',
            'auai.org/UAI/2018/Paper{}/Area_Chairs'.format(paper_number)
            ]},
        reviewer_to_add = reviewer_to_add,
        reviewer_to_remove = reviewer_to_remove,
        check_conflicts_invitation = None,
        parent_label = 'Reviewers',
        individual_label = 'AnonReviewer')
