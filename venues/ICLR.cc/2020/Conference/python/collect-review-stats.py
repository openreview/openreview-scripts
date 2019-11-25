import openreview
import argparse
import csv

from tqdm import tqdm

if __name__ == '__main__':
    ## Argument handling
    parser = argparse.ArgumentParser()
    parser.add_argument('--baseurl', help="base url")
    parser.add_argument('--username')
    parser.add_argument('--password')
    args = parser.parse_args()

    client = openreview.Client(baseurl=args.baseurl, username=args.username, password=args.password)

    conference_id = 'ICLR.cc/2020/Conference'

    map_number_to_blind_notes = {note.number: note for note in openreview.tools.iterget_notes(client, invitation=conference_id+'/-/Blind_Submission')}
    print ('{0} papers found'.format(len(map_number_to_blind_notes)))

    print('collecting review')
    all_reviews = list(openreview.tools.iterget_notes(client, invitation=conference_id+'/Paper[0-9]*/-/Official_Review$'))

    map_paper_to_reviews = {}
    for review in tqdm(all_reviews):
        paper_number = int(review.invitation.split('Paper')[1].split('/')[0])
        if paper_number in map_number_to_blind_notes:
            if paper_number not in map_paper_to_reviews:
                map_paper_to_reviews[paper_number] = []
            map_paper_to_reviews[paper_number].append(review)

    print('collecting reviewers')
    reviewer_iterator = list(openreview.tools.iterget_groups(client, regex='ICLR.cc/2020/Conference/Paper[0-9]*/AnonReviewer[0-9]*$'))

    map_signature_to_reviewer = {}
    for reviewer in tqdm(reviewer_iterator):
        if len(reviewer.members) < 1:
            continue
        map_signature_to_reviewer[reviewer.id] = reviewer.members[0]

    print('collecting reviewer ids and writing')
    with open('out.csv', 'w') as f:
        csv_f = csv.writer(f)
        csv_f.writerow(['Paper Number', 'Reviewer Id', 'Review Rating', 'Experience Assessment'])
        for paper_number in tqdm(sorted(map_paper_to_reviews)):
            for review in map_paper_to_reviews[paper_number]:
                if review.signatures[0] not in map_signature_to_reviewer:
                    continue
                reviewer = map_signature_to_reviewer[review.signatures[0]]
                csv_f.writerow([str(paper_number), reviewer, review.content['rating'], review.content['experience_assessment']])