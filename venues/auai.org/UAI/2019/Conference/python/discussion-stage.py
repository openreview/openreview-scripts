import argparse
import openreview
from openreview import invitations
import datetime
import os
import config

if __name__ == '__main__':
    ## Argument handling
    parser = argparse.ArgumentParser()
    parser.add_argument('--baseurl', help="base url")
    parser.add_argument('--username')
    parser.add_argument('--password')
    args = parser.parse_args()

    client = openreview.Client(baseurl=args.baseurl, username=args.username, password=args.password)
    conference = config.get_conference(client)

    number_to_note = {int(note.number): note for note in openreview.tools.iterget_notes(
        client,
        invitation = 'auai.org/UAI/2019/Conference/-/Blind_Submission'
    )}
    all_review_invitations = [inv for inv in openreview.tools.iterget_invitations(
        client,
        regex = 'auai.org/UAI/2019/Conference/-/Paper[0-9]+/Official_Review$',
        details = 'repliedNotes'
    ) if int(inv.id.split('Paper')[1].split('/')[0]) in number_to_note]

    all_comment_invitations = [inv for inv in openreview.tools.iterget_invitations(
        client,
        regex = 'auai.org/UAI/2019/Conference/-/Paper[0-9]+/Comment$'
    ) if int(inv.id.split('Paper')[1].split('/')[0]) in number_to_note]

    # Update review invitations and review notes to remove authors as readers
    for review_invi in all_review_invitations:
        paper_number = review_invi.id.split('Paper')[1].split('/')[0]
        author_grp = 'auai.org/UAI/2019/Conference/Paper{0}/Authors'.format(paper_number)
        if author_grp in review_invi.reply['readers']['values']:
            review_invi.reply['readers']['values'].remove(author_grp)
            client.post_invitation(review_invi)
        for review_json in review_invi.details['repliedNotes']:
            review = openreview.Note.from_json(review_json)
            if author_grp in review.readers:
                review.readers.remove(author_grp)
                client.post_note(review)

    # Update comment invitation to disallow authors from readers of further comments
    for comment_invi in all_comment_invitations:
        paper_number = comment_invi.id.split('Paper')[1].split('/')[0]
        author_grp = 'auai.org/UAI/2019/Conference/Paper{0}/Authors'.format(paper_number)
        updated = False
        if author_grp in comment_invi.reply['readers']['values-dropdown']:
            comment_invi.reply['readers']['values-dropdown'].remove(author_grp)
            updated = True
        if author_grp in comment_invi.invitees:
            comment_invi.invitees.remove(author_grp)
            updated = True
        if updated:
            client.post_invitation(comment_invi)


    #Post meta-review invitations:
    conference.open_meta_reviews(due_date=datetime.datetime(2019, 5, 7, 23, 59))

    all_metareview_invitations = list(openreview.tools.iterget_invitations(
        client,
        regex = 'auai.org/UAI/2019/Conference/-/Paper[0-9]+/Meta_Review$'
    ))

    # Customize meta-review invitations
    for meta in all_metareview_invitations:
        meta.reply['content']['recommendation']['value-dropdown'] = ['Accept (Oral)', 'Accept (Poster)', 'Weak Reject', 'Reject']
        meta.reply['content'].pop('confidence')
        meta.reply['content']['best paper'] = {
            'order': 4,
            'description': 'Nominate as best paper',
            'value-radio': ['Yes', 'No'],
            'required': False
        }
        client.post_invitation(meta)

