import os
import argparse
import json, csv
from collections import defaultdict, Counter
import xml.etree.cElementTree as ET

def get_rows(assignment_by_paperid, bids_by_user):
    csv_rows = []

    counts_by_ac = defaultdict(Counter)

    bid_counts_by_user = {}

    # loop over bids_by_user to find the number of bids of each type that each user submitted.
    for user, paper_bids in bids_by_user.items():
        eager_count = len([bid for pid, bid in paper_bids.items() if bid == '5 - Eager'])
        willing_count = len([bid for pid, bid in paper_bids.items() if bid == '4 - Willing'])
        inapinch_count = len([bid for pid, bid in paper_bids.items() if bid == '3 - In A Pinch'])
        neutral_count = len([bid for pid, bid in paper_bids.items() if bid == '1 - Neutral'])

        bid_counts_by_user[user] = [
            eager_count,
            willing_count,
            inapinch_count,
            neutral_count
        ]

    # iterate over the assignments and count the number of papers assigned for each bid type.
    for paperid, assignment_list in assignment_by_paperid.items():
        for user in assignment_list:
            if user in bids_by_user:
                bid = bids_by_user[user].get(paperid, '1 - Neutral')
                counts_by_ac[user][bid] += 1

    # populate the rows to be written to the csv file.
    for ac, counts in counts_by_ac.items():
        bid_counts = bid_counts_by_user.get(ac, [0,0,0,0])

        if bid_counts == [0,0,0,0]:
            print('this user has not submitted any bids: {}'.format(ac))

        # these rows can be formatted differently if desired.
        csv_rows.append([
            ac,
            '{}/{}'.format(counts['5 - Eager'], bid_counts[0]),
            '{}/{}'.format(counts['4 - Willing'], bid_counts[1]),
            '{}/{}'.format(counts['3 - In A Pinch'], bid_counts[2]),
            '{}/{}'.format(counts['1 - Neutral'], bid_counts[3])
        ])

    sorted_rows = sorted(csv_rows, key=lambda x: x[0])
    sorted_rows.insert(0, ['email', 'eager', 'willing', 'in a pinch', 'neutral'])

    return sorted_rows


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--infile', help='the .xml assignments file to be loaded to CMT.', required=True)
    parser.add_argument('-o', '--outfile', help='the .csv file where the stats should be written.', required=True)
    parser.add_argument('-b', '--bidfile', help='the post-processed .json file containing the bids per user.', required=True)
    args = parser.parse_args()

    with open(args.bidfile) as f:
        bids_by_user = json.load(f)

    tree = ET.parse(args.infile)
    root = tree.getroot()
    assignment_list = [{paper.attrib['submissionId']: [user.attrib['email'] for user in paper]} for paper in root]
    assignment_by_paperid = {}
    for a in assignment_list:
        assignment_by_paperid.update(a)

    rows = get_rows(assignment_by_paperid, bids_by_user)

    with open(args.outfile, 'w') as f:
        writer = csv.writer(f)
        for row in rows:
            writer.writerow(row)

