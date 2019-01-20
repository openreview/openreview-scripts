'''
Script to create new revise-review invitations for reviews posted after rebuttal stage has started

This script finds the review comments that do not have corresponding revise invitations and creates the invitation.
'''

import argparse
import openreview
import akbc19 as conference_config
import invitations
import notes

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--baseurl', help="base url")
    parser.add_argument('--username')
    parser.add_argument('--password')
    args = parser.parse_args()

    client = openreview.Client(baseurl=args.baseurl, username=args.username, password=args.password)

    existing_review_revision_invis = [invi.id for invi in openreview.tools.iterget_invitations(
        client,
        regex = 'AKBC.ws/2019/Conference/-/Paper.*/Official_Review/AnonReview.*/Revision$'
    )]
    print ("len of existing",len(existing_review_revision_invis))

    official_review_invs = openreview.tools.iterget_invitations(
        client,
        regex='AKBC.ws/2019/Conference/-/Paper.*/Official_Review$',
        details='repliedNotes,replytoNote')

    counter_new_invis_created = 0

    for review_inv in official_review_invs:
        if review_inv.details and 'repliedNotes' in review_inv.details:
            official_reviews = [
                openreview.Note.from_json(r) \
                for r in review_inv.details['repliedNotes']]
            
            if (review_inv.details.get('replytoNote')):
                paper = openreview.Note.from_json(review_inv.details.get('replytoNote'))
                paper_number = paper.number
                for review in official_reviews:
                    reviewer_id = review.signatures[0].split('/')[4]

                    review_revision_inv = invitations.enable_invitation(
                        'Review_Revision', target_paper=review)
                    
                    review_revision_inv.id = review_revision_inv.id.replace('<paper_number>', "Paper" + str(paper_number))
                    review_revision_inv.id = review_revision_inv.id.replace('<reviewer_id>', reviewer_id)

                    if review_revision_inv.id not in existing_review_revision_invis:
                        review_revision_inv.reply['referent'] = review.id
                        review_revision_inv.reply['signatures'] = {
                            'description': 'How your identity will be displayed with the above content.',
                            'values-regex': conference_config.PAPER_ANONREVIEWERS_TEMPLATE_REGEX.replace('<number>',str(paper_number))
                        }
                        review_revision_inv.invitees = review.signatures

                        client.post_invitation(review_revision_inv)
                        print (review_revision_inv.id)
                        counter_new_invis_created += 1
                        if (counter_new_invis_created%10 == 0):
                            print ("Updated {} new invitations".format(counter_new_invis_created))
    
    print ("New revise review invitations created: {}".format(counter_new_invis_created))