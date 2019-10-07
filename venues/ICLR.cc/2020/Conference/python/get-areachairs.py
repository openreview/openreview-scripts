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
Use the --areachair (-a) flag to specify a username or email address to get assignments.

python get-areachairs.py --paper 123

python get-areachairs.py --areachair ~Oriol_Vinyals1

'''

if __name__ == "__main__":
    ## Argument handling
    parser = argparse.ArgumentParser()
    parser.add_argument('-p','--paper')
    parser.add_argument('-a','--areachair')
    parser.add_argument('--baseurl', help="base url")
    parser.add_argument('--username')
    parser.add_argument('--password')

    args = parser.parse_args()

    client = openreview.Client(baseurl=args.baseurl, username=args.username, password=args.password)

    paper_number = args.paper
    areachair_name = args.areachair

    conference = 'ICLR.cc/2020/Conference'

    if paper_number:
        paper_url = 'ICLR.cc/2020/Conference/Paper{}'.format(paper_number)
        ac_group = client.get_group(id=paper_url + '/Area_Chairs')
        individual_ac_groups = client.get_groups(regex=paper_url+'/Area_Chair[0-9]+$')
        print('Area Chair for paper {paper_number}:'.format(paper_number=paper_number))
        for reviewer in ac_group.members:
            individual_ac = [g for g in individual_ac_groups if reviewer in g.members]
            if individual_ac:
                anon_reviewer = individual_ac[0]
                print('{reviewer} - (Area_Chair{number})'.format(reviewer=reviewer, number=anon_reviewer.id[-1]))
            else:
                print('Area Chair not found for {reviewer}, something wrong is here'.format(reviewer=reviewer))

    if areachair_name:
        ac_groups = client.get_groups(member=areachair_name, regex='ICLR.cc/2020/Conference/Paper.*/Area_Chairs$')
        individual_ac_groups = client.get_groups(member=areachair_name, regex='ICLR.cc/2020/Conference/Paper.*/Area_Chair[0-9]+$')
        print('Papers assigned to Area Chair {ac}:'.format(ac=areachair_name))
        for group in ac_groups:
            number = [token for token in group.id.split('/') if token.startswith('Paper')][0].replace('Paper', '')
            anon_reviewers = [g for g in individual_ac_groups if g.id.startswith('ICLR.cc/2020/Conference/Paper{number}'.format(number=number))]
            if anon_reviewers:
                anon_reviewer = anon_reviewers[0]
                print('Paper {paper_number} - (Area_Chair{number})'.format(paper_number=number, number=anon_reviewer.id[-1]))
            else:
                print('Area Chair not found for {number}, something wrong is here'.format(number=number))

