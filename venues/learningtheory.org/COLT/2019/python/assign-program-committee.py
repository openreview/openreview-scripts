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
    member_to_remove = args.remove
    member_to_add = args.add

    conference_id = 'learningtheory.org/COLT/2019/Conference'

    result = openreview.tools.assign(
        client=client,
        conference='learningtheory.org/COLT/2019/Conference',
        paper_number=paper_number,
        reviewer_to_add=member_to_add,
        reviewer_to_remove=member_to_remove,
        parent_label = 'Program_Committee',
        individual_label = 'Program_Committee_Member',
        individual_group_params = {
            'readers': [
                'learningtheory.org/COLT/2019/Conference',
                'learningtheory.org/COLT/2019/Conference/Program_Chairs',
                'learningtheory.org/COLT/2019/Conference/Paper{0}/Program_Committee'.format(paper_number)
            ]},
        parent_group_params = {
            'readers': [
                'learningtheory.org/COLT/2019/Conference',
                'learningtheory.org/COLT/2019/Conference/Program_Chairs',
                'learningtheory.org/COLT/2019/Conference/Paper{0}/Program_Committee'.format(paper_number)
            ],
            'signatories': ['learningtheory.org/COLT/2019/Conference/Paper{0}/Program_Committee'.format(paper_number)]
        })

    print('result', result)
