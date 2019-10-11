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
Use the --reviewer (-r) flag to specify a username or email address to get assignments.

python get-reviewers.py --paper 123

python get-reviewers.py --reviewer ~Oriol_Vinyals1

'''

if __name__ == "__main__":
    ## Argument handling
    parser = argparse.ArgumentParser()
    parser.add_argument('-p','--paper')
    parser.add_argument('-r','--reviewer')
    parser.add_argument('--baseurl', help="base url")
    parser.add_argument('--username')
    parser.add_argument('--password')

    args = parser.parse_args()

    client = openreview.Client(baseurl=args.baseurl, username=args.username, password=args.password)

    paper_number = args.paper
    reviewer_name = args.reviewer

    conference = 'ICLR.cc/2020/Conference'

    if paper_number:
        paper_url = 'ICLR.cc/2020/Conference/Paper{}'.format(paper_number)
        reviewer_group = client.get_group(id=paper_url + '/Reviewers')
        anon_reviewers_groups = client.get_groups(regex=paper_url+'/AnonReviewer.*')
        print('Reviewers for paper {paper_number}:'.format(paper_number=paper_number))
        for reviewer in reviewer_group.members:
            anon_reviewers = [g for g in anon_reviewers_groups if reviewer in g.members]
            if anon_reviewers:
                anon_reviewer = anon_reviewers[0]
                print('{reviewer} - (AnonReviewer{number})'.format(reviewer=reviewer, number=anon_reviewer.id[-1]))
            else:
                print('AnonReviewer not found for {reviewer}, something wrong is here'.format(reviewer=reviewer))

    if reviewer_name:
        reviewer_groups = client.get_groups(member=reviewer_name, regex='ICLR.cc/2020/Conference/Paper.*/Reviewers$')
        anon_reviewers_groups = client.get_groups(member=reviewer_name, regex='ICLR.cc/2020/Conference/Paper.*/AnonReviewer.*$')
        print('Papers assigned to reviewer {reviewer}:'.format(reviewer=reviewer_name))
        for group in reviewer_groups:
            number = [token for token in group.id.split('/') if token.startswith('Paper')][0].replace('Paper', '')
            anon_reviewers = [g for g in anon_reviewers_groups if g.id.startswith('ICLR.cc/2020/Conference/Paper{number}'.format(number=number))]
            if anon_reviewers:
                anon_reviewer = anon_reviewers[0]
                print('Paper {paper_number} - (AnonReviewer{number})'.format(paper_number=number, number=anon_reviewer.id[-1]))
            else:
                print('AnonReviewer not found for {number}, something wrong is here'.format(number=number))

