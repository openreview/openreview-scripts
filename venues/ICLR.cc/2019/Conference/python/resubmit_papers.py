'''
A throwaway script for testing ICLR 19 workflow.

Gets ICLR 2018 papers and posts them as ICLR 2019 submissions.
'''

import openreview
import argparse
import iclr19

def resubmit_papers(client, old_papers_inv, new_papers_inv):
    for paper in openreview.tools.iterget_notes(client, invitation=old_papers_inv):
        new_content = paper.content
        new_paper = openreview.Note(**{
            'invitation': new_papers_inv,
            'writers': paper.signatures,
            'readers': [iclr19.CONFERENCE_ID],
            'signatures': paper.signatures,
            'content': new_content
        })

        try:
            p = client.post_note(new_paper)
            print("{} -> {}".format(paper.id, p.id))
        except openreview.OpenReviewException as e:
            pass

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--baseurl', help="openreview base URL")
    parser.add_argument('--username')
    parser.add_argument('--password')

    args = parser.parse_args()

    ## Initialize the client library with username and password
    client = openreview.Client(baseurl=args.baseurl, username=args.username, password=args.password)
    print("connecting to", client.baseurl)

    print('posting ICLR 18 submissions to ICLR 19')
    resubmit_papers(client, 'ICLR.cc/2018/Conference/-/Submission', iclr19.SUBMISSION_ID)
