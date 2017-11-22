import openreview
import argparse
import config

parser = argparse.ArgumentParser()
parser.add_argument('--username')
parser.add_argument('--password')
parser.add_argument('--baseurl', help = "base URL")
args = parser.parse_args()

client = openreview.Client(username=args.username, password=args.password, baseurl=args.baseurl)

def create_revision_invitation(forum, referent, signature):
    params = {
        'writers': [config.CONF],
        'signatures': [config.CONF],
        'readers': ['everyone'],
        'invitees': [signature],
        'reply': {
            'forum': forum,
            'referent': referent,
            'writers': {
                'values': [config.CONF]
            },
            'signatures': {
                'values-regex': signature + '|ICLR.cc/2018/Conference'
            },
            'readers': {
                'values':['everyone']
            },
            'content': config.official_review_params['reply']['content']
        }
    }

    signature_components = signature.split('/')
    paper_num = signature_components[3]
    anonreviewer = signature_components[4]

    revise_review = openreview.Invitation('ICLR.cc/2018/Conference/-/{0}/{1}/Revise_Review'.format(anonreviewer, paper_num), **params)
    return revise_review

review_invitations = client.get_invitations(regex = config.CONF + '/-/Paper.*/Official_Review')
reviews = client.get_notes(invitation = config.CONF + '/-/Paper.*/Official_Review')

for inv in review_invitations:
    forum_reviews = [r for r in reviews if r.forum == inv.reply['forum']]

    inv.reply['writers'] = {'values': []}
    with open('../process/officialReviewProcess_withRevision.js') as f:
        inv.process = f.read()
    inv = client.post_invitation(inv)

    for review in forum_reviews:
        print "updating review: ", review.id
        review.readers = ['everyone']
        review.writers = []
        client.post_note(review)
        review_revision_invitation = create_revision_invitation(review.forum, review.id, review.signatures[0])
        print "posting review revision invitation ", review_revision_invitation.id
        client.post_invitation(review_revision_invitation)
