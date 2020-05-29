import openreview
import csv
import time
from tqdm import tqdm
import argparse
from collections import defaultdict

if __name__ == '__main__':
    ## Argument handling
    parser = argparse.ArgumentParser()
    parser.add_argument('--baseurl', help='base url')
    parser.add_argument('--username')
    parser.add_argument('--password')
    args = parser.parse_args()

    client = openreview.Client(baseurl=args.baseurl, username=args.username, password=args.password)

    map_submissions = {note.number: note for note in openreview.tools.iterget_notes(client, invitation = 'thecvf.com/ECCV/2020/Conference/-/Blind_Submission')}
    
    # 1. Update all the review invitations
    paper_review_invis = list(openreview.tools.iterget_invitations(
        client, 
        regex='^thecvf.com/ECCV/2020/Conference/Paper[0-9]+/-/Official_Review$'))

    print('{} review invitations found'.format(len(paper_review_invis)))

    for invi in tqdm(paper_review_invis):
        paper_num = int(invi.id.split('Paper')[1].split('/')[0])
        if paper_num in map_submissions:
            invi.reply['readers']['values-copied'] = [
                'thecvf.com/ECCV/2020/Conference/Program_Chairs',
                'thecvf.com/ECCV/2020/Conference/Paper{}/Area_Chairs'.format(paper_num),
                'thecvf.com/ECCV/2020/Conference/Paper{}/Reviewers'.format(paper_num),
                'thecvf.com/ECCV/2020/Conference/Paper{}/Authors'.format(paper_num)
            ]
            updated_invi = client.post_invitation(invi)

    # 2. Update all the rebuttal invitations
    # May need to include "expired=True" in this call since the invitation possibly would have expired by then
    rebuttal_invis = list(openreview.tools.iterget_invitations(
        client, 
        regex='^thecvf.com/ECCV/2020/Conference/Paper[0-9]+/AnonReviewer[0-9]+/-/Rebuttal$'))

    print('{} rebuttal invitations found'.format(len(paper_review_invis)))

    for invi in tqdm(rebuttal_invis):
        paper_num = int(invi.id.split('Paper')[1].split('/')[0])
        if paper_num in map_submissions:
            invi.reply['readers']['values'] = [
                'thecvf.com/ECCV/2020/Conference/Program_Chairs',
                'thecvf.com/ECCV/2020/Conference/Paper{}/Area_Chairs'.format(paper_num),
                'thecvf.com/ECCV/2020/Conference/Paper{}/Reviewers'.format(paper_num),
                'thecvf.com/ECCV/2020/Conference/Paper{}/Authors'.format(paper_num)
            ]
            updated_invi = client.post_invitation(invi)
    
    # 3. Update all the official reviews
    
    official_reviews = list(openreview.tools.iterget_notes(
        client, 
        invitation='^thecvf.com/ECCV/2020/Conference/Paper[0-9]+/-/Official_Review$'))

    print('{} official review notes found'.format(len(official_reviews)))

    for review in tqdm(official_reviews):
        paper_num = int(review.invitation.split('Paper')[1].split('/')[0])
        if paper_num in map_submissions:
            review.readers = [
                'thecvf.com/ECCV/2020/Conference/Program_Chairs',
                'thecvf.com/ECCV/2020/Conference/Paper{}/Area_Chairs'.format(paper_num),
                'thecvf.com/ECCV/2020/Conference/Paper{}/Reviewers'.format(paper_num),
                'thecvf.com/ECCV/2020/Conference/Paper{}/Authors'.format(paper_num)]
            updated_note = client.post_note(review)

    # 4. Update all the rebuttals
    
    rebuttal_notes = list(openreview.tools.iterget_notes(
        client, 
        invitation='^thecvf.com/ECCV/2020/Conference/Paper[0-9]+/AnonReviewer[0-9]+/-/Rebuttal$'))

    print('{} rebuttal notes found'.format(len(rebuttal_notes)))

    for note in tqdm(rebuttal_notes):
        paper_num = int(note.invitation.split('Paper')[1].split('/')[0])
        if paper_num in map_submissions:
            note.readers = [
                'thecvf.com/ECCV/2020/Conference/Program_Chairs',
                'thecvf.com/ECCV/2020/Conference/Paper{}/Area_Chairs'.format(paper_num),
                'thecvf.com/ECCV/2020/Conference/Paper{}/Reviewers'.format(paper_num),
                'thecvf.com/ECCV/2020/Conference/Paper{}/Authors'.format(paper_num)]
            updated_note = client.post_note(note)

    # 5. Enable review revisions
    # 6. Disable confidential comments for Authors \
    # (remove Authors from both invitation.invitees and invitation.readers)
    # 7. Enable meta-reviews for ACs
    # 8. Enable review ratings for ACs