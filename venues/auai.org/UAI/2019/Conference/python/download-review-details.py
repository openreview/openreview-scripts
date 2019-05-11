import argparse
import openreview
import datetime
# import config
from collections import defaultdict
import csv
import re

def prettyId(name):
    result = ''
    if not name:
        return result
    if '@' in name:
        return name
    if name.startswith('~'):
        r=re.compile(r'\d')
        result = r.sub('', name)
        result = result.lstrip('~')
        result = result.replace('_', ' ')
    return result


if __name__ == '__main__':
    ## Argument handling
    parser = argparse.ArgumentParser()
    parser.add_argument('--baseurl', help="base url")
    parser.add_argument('--username')
    parser.add_argument('--password')
    args = parser.parse_args()

    client = openreview.Client(baseurl=args.baseurl, username=args.username, password=args.password)

    paper_number_to_blind_note = {int(paper.number): paper for paper in openreview.tools.iterget_notes(
        client,
        invitation = 'auai.org/UAI/2019/Conference/-/Blind_Submission'
    )}

    print (len(paper_number_to_blind_note))

    paper_number_to_meta_review = {int(meta_rev.invitation.split('Paper')[1].split('/')[0]): meta_rev for meta_rev in openreview.tools.iterget_notes(
        client,
        invitation = 'auai.org/UAI/2019/Conference/-/Paper.*/Meta_Review'
    ) if int(meta_rev.invitation.split('Paper')[1].split('/')[0]) in paper_number_to_blind_note}

    print (len(paper_number_to_meta_review))

    all_reviews = openreview.tools.iterget_notes(
        client,
        invitation = 'auai.org/UAI/2019/Conference/-/Paper.*/Official_Review'
    )
    paper_number_to_review = defaultdict(lambda : [])
    for review in all_reviews:
        paper_number = int(review.invitation.split('Paper')[1].split('/')[0])
        if paper_number in paper_number_to_blind_note:
            paper_number_to_review[paper_number].append(review)

    print (len(paper_number_to_review))

    ac_groups = openreview.tools.iterget_groups(
        client,
        regex = 'auai.org/UAI/2019/Conference/Paper[0-9]+/Area_Chairs$'
    )
    ac_to_paper_numbers = defaultdict(lambda : set())
    for ac in ac_groups:
        paper_number = int(ac.id.split('Paper')[1].split('/')[0])
        ac_id = ac.members[0]
        ac_to_paper_numbers[ac_id].add(paper_number)

    with open('UAI2019.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerow(["Area Chair", "Paper Number", "Paper Title", "Review Rating", "Review Confidence", "Meta-review", "Final Decision", "Decision Text"])
        # print (sorted(ac_to_paper_numbers.items(), key = lambda key:key))
        for index, ac_tuple in enumerate(sorted(ac_to_paper_numbers.items(), key = lambda key:key)):
            for paper in sorted(ac_tuple[1]):
                if paper in paper_number_to_blind_note:
                    review_stats = [(review.content['rating'], review.content['confidence']) for review in paper_number_to_review[paper]]
                    meta_review = paper_number_to_meta_review.get(paper, None)
                    if meta_review:
                        meta_review = meta_review.content['recommendation']
                    else:
                        meta_review = 'Meta-review not available'

                    writer.writerow([prettyId(ac_tuple[0]), str(paper), paper_number_to_blind_note[paper].content['title'], review_stats[0][0], review_stats[0][1], meta_review, None, None])

                    if len(review_stats) > 1:
                        for i in range(1, len(review_stats)):
                            writer.writerow([None, None, None, review_stats[i][0], review_stats[i][1], None, None, None])

