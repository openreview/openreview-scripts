import archive
import openreview
import argparse

def main(client):
    profile_by_signature = {}
    for claim in openreview.tools.iterget_tags(client, invitation=archive.confirmation_tag_invitation.id):
        if 'No' in claim.tag:
            claim_signature = claim.signatures[0]
            paper = client.get_note(claim.forum)

            if claim_signature not in profile_by_signature:
                profile_by_signature[claim_signature] = client.get_profile(claim_signature)

            profile = profile_by_signature[claim_signature]

            claim_emails = profile.content['emails']

            new_authorids = []
            for authorid in paper.content['authorids']:
                if authorid in claim_emails:
                    new_authorids.append('')
                else:
                    new_authorids.append(authorid)

            if new_authorids != paper.content['authorids']:
                paper.content['authorids'] = new_authorids
                posted_paper = client.post_note(paper)
                print(posted_paper.id)


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--baseurl', help="base URL")
    parser.add_argument('--username')
    parser.add_argument('--password')

    args = parser.parse_args()

    client = openreview.Client(baseurl=args.baseurl, username=args.username, password=args.password)
    print('connecting to {0}'.format(client.baseurl))

    main(client)
