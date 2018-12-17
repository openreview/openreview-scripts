'''
This script generates AC-related scores for AKBC '19 paper-reviewer matching.

There are two AC-related scores:
    - Subject Area Overlap, compute as the jaccard similarity between each paper and each reviewer's
    stated subject areas.
    - Recruited AC score, defined as 1 for paper-reviewer pairs in which the paper's AC also recruited that
    reviewer, and 0 otherwise.

'''

import openreview
import akbc19
import csv
import argparse
from collections import defaultdict
import os

def get_profiles_by_name(client, first, last):
    '''
    Returns a single profile by first and last name
    '''
    response = requests.get(client.profiles_url, params = {'first': first, 'last': last}, headers = client.headers)
    return [openreview.Profile.from_json(p) for p in response.json()['profiles']]

def jaccard_similarity(list1, list2):
    intersection = len(list(set(list1).intersection(list2)))
    union = (len(list1) + len(list2)) - intersection
    return float(intersection / union)

def parse_reviewer_roster(path):
    subject_areas_by_reviewer = defaultdict(list)
    recommenders_by_reviewer = defaultdict(list)
    with open(path) as f:
        reader = csv.reader(f)
        reader.__next__()
        for row in reader:
            first = row[0]
            middle = row[1]
            last = row[2]
            email = row[3]
            subject_areas = row[4]
            ac1_id = row[5]
            ac2_id = row[6]

            try:
                reviewer_profile = client.get_profile(email)
                reviewer_id = reviewer_profile.id
            except openreview.OpenReviewException as e:
                reviewer_id = email

            subject_areas_by_reviewer[reviewer_id].extend([s.strip() for s in subject_areas.split(',')])
            recommenders_by_reviewer[reviewer_id].append(ac1_id)

            if ac2_id:
                recommenders_by_reviewer[reviewer_profile.id].append(ac2_id)

    return subject_areas_by_reviewer, recommenders_by_reviewer

def write_scores(path, scores):
    with open(path, 'w') as f:
        writer = csv.writer(f)
        for coordinates, score in scores.items():
            writer.writerow([coordinates[0], coordinates[1], score])


if __name__ == '__main__':
    ## Argument handling
    parser = argparse.ArgumentParser()
    parser.add_argument('outdir', help='directory path where the output files should be written')
    parser.add_argument('--baseurl', help="base url")
    parser.add_argument('--username')
    parser.add_argument('--password')
    args = parser.parse_args()

    client = openreview.Client(baseurl=args.baseurl, username=args.username, password=args.password)

    blind_submissions = openreview.tools.iterget_notes(client, invitation=akbc19.BLIND_SUBMISSION_ID)

    roster_path = '../data/reviewer_roster_formatted.csv'
    subject_areas_by_reviewer, recommenders_by_reviewer = parse_reviewer_roster(roster_path)

    overlap_scores = defaultdict(float)
    ac_scores = defaultdict(int)

    reviewers = client.get_group('AKBC.ws/2019/Conference/Reviewers')
    blind_submissions = openreview.tools.iterget_notes(client, invitation=akbc19.BLIND_SUBMISSION_ID)

    for paper in blind_submissions:
        paper_subjects = paper.content['subject areas']
        acs_group = client.get_group('AKBC.ws/2019/Conference/Paper{}/Area_Chairs'.format(paper.number))

        for reviewer in reviewers.members:
            reviewer_subjects = subject_areas_by_reviewer[reviewer]
            overlap_score = jaccard_similarity(reviewer_subjects, paper_subjects)
            overlap_scores[(paper.forum, reviewer)] = overlap_score

            # print(overlap_score, reviewer_subjects, paper_subjects)

            ac_recommenders = recommenders_by_reviewer[reviewer]

            if any([ac in ac_recommenders for ac in acs_group.members]) :
                ac_scores[(paper.forum, reviewer)] = 1
            else:
                ac_scores[(paper.forum, reviewer)] = 0

    write_scores(os.path.join(args.outdir, 'ac_scores.csv'), ac_scores)
    write_scores(os.path.join(args.outdir, 'overlap_scores.csv'), overlap_scores)

