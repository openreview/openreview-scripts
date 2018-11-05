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
        client.get_invitations,
        regex='ICLR.cc/2019/Conference/-/Paper.*/Official_Review$',
        details='repliedNotes,replytoNote')

    for review_inv in official_review_invs:
        review_inv.reply['readers']['values'] = ['everyone']
        review_inv.reply['writers'] = {
            "description": "Users that may modify this record.",
            "values": [
                iclr19.CONFERENCE_ID
                ]
        }
        client.post_invitation(review_inv)
        if review_inv.details and 'repliedNotes' in review_inv.details:
            official_reviews = [
                openreview.Note.from_json(r) \
                for r in review_inv.details['repliedNotes']]

            if (review_inv.details.get('replytoNote')):
                paper = openreview.Note.from_json(review_inv.details.get('replytoNote'))
                paper_number = paper.number
                for review in official_reviews:
                    review.readers = ['everyone']
                    review.writers = [iclr19.CONFERENCE_ID]
                    review = client.post_note(review)

                    reviewer_id = review.signatures[0].split('/')[4]

                    review_revision_inv = invitations.enable_invitation(
                        'Review_Revision', target_paper=review)
                    
                    review_revision_inv.id = review_revision_inv.id.replace('<paper_number>', "Paper" + str(paper_number))
                    review_revision_inv.id = review_revision_inv.id.replace('<reviewer_id>', reviewer_id)

                    review_revision_inv.reply['referent'] = review.id
                    review_revision_inv.reply['signatures'] = {
                        'description': 'How your identity will be displayed with the above content.',
                        'values-regex': iclr19.PAPER_ANONREVIEWERS_TEMPLATE_REGEX.replace('<number>',str(paper_number))
                    }
                    review_revision_inv.invitees = review.signatures

                    client.post_invitation(review_revision_inv)
            
    blind_notes = openreview.tools.iterget_notes(client, invitation=iclr19.BLIND_SUBMISSION_ID)
    for note in blind_notes:
        client.post_invitation(
            invitations.enable_invitation('Paper_Revision', target_paper=note))

    # Create questionnaire response copies for only AC and PC's viewing
    client.post_invitation(iclr19.view_questionnaire_response_invi)
        
    ques_response_inv = client.get_invitations(
        regex='ICLR.cc/2019/Conference/-/Reviewer_Questionnaire_Response',
        details='repliedNotes,replytoNote')[0]
    print ("Available responses to reviewer questionnaire: {}".format (len(ques_response_inv.details['repliedNotes'])))
    
    # Map: Reviewer Signature -> Review response to questionnaire
    map_reviewer_response = {}
    if ques_response_inv.details and 'repliedNotes' in ques_response_inv.details:
        for response in ques_response_inv.details['repliedNotes']:
            map_reviewer_response[response['signatures'][0]] = response

    # Map: Paper-AnonReview -> Member's Signature
    map_paperanonreviewer_member = {}
    paper_anon_reviewers = openreview.tools.iterget_groups(client, regex = "ICLR.cc/2019/Conference/Paper.*/AnonReviewer.*")
    
    for reviewer in paper_anon_reviewers:
        map_paperanonreviewer_member[reviewer.id] = reviewer.members[0]
    
    # Map: Paper_Number -> Area Chair group
    map_paper_ac = {}
    paper_area_chairs = openreview.tools.iterget_groups(client, regex = "ICLR.cc/2019/Conference/Paper.*/Area_Chairs")
    for grp in paper_area_chairs:
        paper_number = grp.id.split('Paper')[1].split('/')[0]
        map_paper_ac[paper_number] = grp.id

    # Set: review note ids (avoid creating multiple copies of questionnaire responses)
    set_reviewid_copyid = set()

    questionnaire_response_copies = openreview.tools.iterget_notes(client, invitation = iclr19.view_questionnaire_response_invi.id)
    
    existing_copy_count = 0 
    for copy in questionnaire_response_copies:
        set_reviewid_copyid.add(copy.replyto)
        existing_copy_count += 1
    if existing_copy_count:
        print ("Existing copy count: {}".format(existing_copy_count))

    # Process each anonymous review
    processed_count = 0
    anon_reviews = openreview.tools.iterget_notes(client, invitation = iclr19.CONFERENCE_ID+'/-/Paper.*/Official_Review')
    for review in anon_reviews:
        paper_number = review.invitation.split('Paper')[1].split('/')[0]
        
        # check if this reviewer has posted a response to the questionnaire
        reviewer_sign = map_paperanonreviewer_member[ review.signatures[0] ]
        
        if (reviewer_sign in map_reviewer_response) and (review.id not in set_reviewid_copyid):
            # post a copy note of the questionnnaire response with invi = iclr19.view_questionnaire_response_invi.id
            copy_note = openreview.Note(
                original = map_reviewer_response[reviewer_sign]['id'],
                replyto = review.id,
                invitation = iclr19.view_questionnaire_response_invi.id,
                forum = review.forum,
                signatures = [iclr19.CONFERENCE_ID],
                writers = [iclr19.CONFERENCE_ID],
                readers = [iclr19.PROGRAM_CHAIRS_ID, map_paper_ac[paper_number]],
                content = {'title': 'Questionnaire Response for {}'.format(review.signatures[0].split('/')[-1])}
            )
            posted_note = client.post_note(copy_note)
            processed_count += 1
    print ("Questionnaire response copies created: {}".format(processed_count))
