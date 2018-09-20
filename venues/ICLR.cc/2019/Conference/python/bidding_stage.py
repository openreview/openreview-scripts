'''
Bidding Stage (Oct 2 - Oct 5)

- Bidding Task / interface enabled and added to the Reviewer Console
- Reviewers bid on papers.
- Area chairs bid on papers.

'''

import openreview
import iclr19
import notes
import groups
import invitations
import argparse

if __name__ == '__main__':
    ## Argument handling
    parser = argparse.ArgumentParser()
    parser.add_argument('--baseurl', help="base url")
    parser.add_argument('--username')
    parser.add_argument('--password')
    args = parser.parse_args()

    client = openreview.Client(baseurl=args.baseurl, username=args.username, password=args.password)

    with open('../webfield/reviewerWebfieldBiddingEnabled.js','r') as f:
        reviewers = client.get_group(iclr19.REVIEWERS_ID)
        reviewers.web = f.read()
        client.post_group(reviewers)

    with open('../webfield/areaChairWebfieldBiddingEnabled.js','r') as f:
        area_chairs = client.get_group(iclr19.AREA_CHAIRS_ID)
        area_chairs.web = f.read()
        client.post_group(area_chairs)

    iclr19.add_bid.invitees = [iclr19.REVIEWERS_ID, iclr19.AREA_CHAIRS_ID]
    client.post_invitation(iclr19.add_bid)

