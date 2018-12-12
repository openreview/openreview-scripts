'''
Create review rating invitations for all reviewers. This will be an invitation to rate reviews from other reviewers on the same paper
'''

import argparse
import openreview
import iclr19
import invitations

def get_all_reviews(client, paper_number):
    reply_notes = client.get_notes(invitation = iclr19.CONFERENCE_ID + "/-/Paper{}/Official_Review".format(paper_number))
    map_anon_reviewer_to_replynote = {}
    for note in reply_notes:
        anon_rev = note.signatures[0]
        map_anon_reviewer_to_replynote[anon_rev] = note.id
    return map_anon_reviewer_to_replynote

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--baseurl', help="base url")
    parser.add_argument('--username')
    parser.add_argument('--password')
    args = parser.parse_args()

    client = openreview.Client(baseurl=args.baseurl, username=args.username, password=args.password)

    all_papers = list(openreview.tools.iterget_notes(client, invitation = iclr19.BLIND_SUBMISSION_ID))

    counter = 0
    for paper in all_papers:

        map_paper_to_anonrev_reviews = get_all_reviews(client, paper.number)
        all_submitted_reviewers = client.get_group("ICLR.cc/2019/Conference/Paper{}/Reviewers/Submitted".format(paper.number)).members

        for anonrev, review_id in map_paper_to_anonrev_reviews.items():
            ## Create invitation for this paper-anonreview-review combination
            new_invitaton = invitations.enable_invitation("Review_Rating", paper)

            # Update the invi before posting it
            new_invitaton.reply['replyto'] = review_id
            new_invitaton.id = new_invitaton.id.replace("{AnonReviewerNumber}", anonrev.split("/")[-1])
            new_invitaton.invitees = [reviewer for reviewer in all_submitted_reviewers if reviewer != anonrev]
            new_invitaton.invitees.append('ICLR.cc/2019/Conference/Paper{}/Authors'.format(paper.number))
            new_invitaton.invitees.append('ICLR.cc/2019/Conference/Paper{}/Area_Chairs'.format(paper.number))
            # Post the invitation
            client.post_invitation(new_invitaton).id
            counter += 1
print ("Posted {} review rating invitations".format(counter))
