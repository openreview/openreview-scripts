import argparse
import openreview
import config

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

def get_bibtex(note, forum, decision_note=None, anonymous=True):
    first_word = note.content['title'].split(' ')[0].lower()

    if anonymous:
        first_author_last_name = 'anonymous'
        authors = 'Anonymous'
    else:
        first_author_last_name = note.content['authors'][0].split(' ')[1].lower()
        authors = ', '.join(note.content['authors'])

    bibtex = [
        '@article{',
        first_author_last_name + '2018' + first_word + ',',
        'title={' + note.content['title'] + '},',
        'author={' + authors + '},',
        'journal={International Conference on Learning Representations},',
        'year={2018},',
        'url={https://openreview.net/forum?id=' + forum + '},',
        '}'
    ]

    if decision_note:
        decision = decision_note.content['decision']
        if 'Reject' in decision:
            bibtext.insert(-1, 'note={rejected}')

        if 'Accept (Oral)' in decision:
            bibtex.insert(-1, 'note={accepted as oral presentation},')

        if 'Accept (Poster)' in decision:
            bibtex.insert(-1, 'note={accepted as poster},')

        if 'Invite to Workshop Track' in decision:
            bibtex.insert(-1, 'note={rejected: invited to workshop track},')

    return '\n'.join(bibtex)

if args.type == 'submissions':
    blind_submissions = client.get_notes(invitation=config.BLIND_SUBMISSION)

    decisions_by_forum = {n.forum: n for n in client.get_notes(
            invitation='ICLR.cc/2018/Conference/-/Acceptance_Decision')}

    for b in blind_submissions:
        original_note = client.get_note(b.original)

        decision_note = decisions_by_forum.get(b.forum, None)

        overwriting_note = openreview.Note(**{
            'id': b.id,
            'original': b.original,
            'invitation': config.BLIND_SUBMISSION,
            'forum': b.forum,
            'signatures': [config.CONF],
            'writers': [config.CONF],
            'readers': ['everyone'],
            'content': {'_bibtex': get_bibtex(original_note, b.forum, decision_note=decision_note, anonymous=(args.hide and not args.show))}
        })

        print "{0} note {1}".format('Revealing' if args.show and not args.hide else 'Hiding', overwriting_note.id)
        client.post_note(overwriting_note)

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
