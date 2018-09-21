'''
Rebuttal and Discussion Stage (~Oct. 29 - TBD)
- All reviews are made visible to the public, and authors have the opportunity to respond to them (and other comments made during the review period).
- Author permission to revise and withdraw submissions (with revision history) is enabled.
- - IMPORTANT: Withdrawn papers should transfer their comments.
- Authors, reviewers, areachairs, and members of the public may continue to post comments under the same permissions as above.
- Reviewers can revise their reviews, with revision history.
- Area chairs can continue to message/remind reviewers through the console for various reasons (e.g. to ask a reviewer to respond to an author rebuttal)


'''

import argparse
import openreview
import iclr19
import invitations
import notes

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--baseurl', help="base url")
    parser.add_argument('--username')
    parser.add_argument('--password')
    args = parser.parse_args()

    client = openreview.Client(baseurl=args.baseurl, username=args.username, password=args.password)

    official_review_invs = openreview.tools.iterget(
        client.get_invitations, regex='ICLR.cc/2019/Conference/-/Paper.*/Official_Review')

    for review_inv in official_review_invs:
        review_inv.reply['readers']['values'] = ['everyone']
        client.post_invitation(review_inv)

    official_reviews = openreview.tools.iterget_notes(
        client, invitation='ICLR.cc/2019/Conference/-/Paper.*/Official_Review')
    for review in official_reviews:
        review = notes.reveal_note(review)
        review = notes.freeze_note(review)
        review = client.post_note(review)

        client.post_invitation(
            invitations.enable_invitation('Revise_Review', target_paper=review))

    original_notes = openreview.tools.iterget_notes(client, invitation=iclr19.SUBMISSION_ID)
    for original in original_notes:
        client.post_invitation(
            invitations.enable_invitation('Add_Revision', target_paper=original))

