import argparse
import openreview
import config
import re

# Argument handling
parser = argparse.ArgumentParser()
parser.add_argument('type', help = 'choose either "submissions" or "reviews"')
parser.add_argument('--hide', action = 'store_true')
parser.add_argument('--show', action = 'store_true')
parser.add_argument('--username')
parser.add_argument('--password')
parser.add_argument('--baseurl', help = "base URL")
args = parser.parse_args()

client = openreview.Client(username=args.username, password=args.password, baseurl=args.baseurl)

if args.type == 'submissions':
    blind_submissions = client.get_notes(invitation=config.BLIND_SUBMISSION)

    decisions_by_forum = {n.forum: n for n in client.get_notes(
            invitation='ICLR.cc/2018/Conference/-/Acceptance_Decision')}

    for b in blind_submissions:
        print "{0} note {1}".format('Revealing' if args.show and not args.hide else 'Hiding', b.id)

        original_note = client.get_note(b.original)

        decision_note = decisions_by_forum.get(b.forum, None)

        if 'Reject' in decision_note.content['decision']:
            accepted = False

        if 'Invite to Workshop Track' in decision_note.content['decision']:
            accepted = False

        if 'Accept' in decision_note.content['decision']:
            accepted = True

        overwriting_note = openreview.Note(**{
            'id': b.id,
            'original': b.original,
            'invitation': config.BLIND_SUBMISSION,
            'forum': b.forum,
            'signatures': [config.CONF],
            'writers': [config.CONF],
            'readers': ['everyone'],
            'content': {
                '_bibtex': openreview.tools.get_bibtex(
                    original_note,
                    'International Conference on Learning Representations',
                    '2018',
                    url_forum=b.forum,
                    accepted=accepted,
                    anonymous=(args.hide and not args.show))
                }
        })

        client.post_note(overwriting_note)

if args.type == 'decisions':
    decisions = client.get_notes(invitation='ICLR.cc/2018/Conference/-/Acceptance_Decision')

    for n in decisions:
        if args.show and not args.hide:
            n.readers = ['everyone']
        else:
            n.readers = ['ICLR.cc/2018/Conference']
        client.post_note(n)
        print "{0} note {1}".format('Revealing' if args.show and not args.hide else 'Hiding', n.id)

if args.type == 'reviews':
    review_invitations = client.get_invitations(regex = config.CONF + '/-/Paper.*/Official_Review')

    review_call_done = False
    reviews = []
    limit = 2000
    offset = 0
    while not review_call_done:
        review_batch = client.get_notes(invitation = config.CONF + '/-/Paper.*/Official_Review', offset=offset, limit=limit)
        offset += limit
        reviews += review_batch
        if len(review_batch) < limit:
            review_call_done = True

if args.type == 'metareviews':
    review_invitations = client.get_invitations(regex = config.CONF + '/-/Paper.*/Meta_Review')
    reviews = client.get_notes(invitation = config.CONF + '/-/Paper.*/Meta_Review')

if args.type == 'reviews' or args.type == 'metareviews':
    for inv in review_invitations:
        forum_reviews = [r for r in reviews if r.forum == inv.reply['forum']]

        if args.show and not args.hide:

            inv.reply['readers']['values'] = ['everyone']
            inv = client.post_invitation(inv)
            print "updating invitation ", inv.id

            for review in forum_reviews:
                print "updating review: ",review.id
                review.readers = ['everyone']
                review.writers = []
                review.nonreaders = []
                client.post_note(review)

        if args.hide and not args.show:
            inv.noninvitees = []
            for review in forum_reviews:
                print "updating review: ",review.id
                review.readers = [config.AREA_CHAIRS_PLUS]
                review.writers = review.signatures
                inv.noninvitees += review.signatures
                client.post_note(review)
            client.post_invitation(inv)
