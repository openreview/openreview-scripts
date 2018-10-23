'''
Reviewing Stage (~Oct. 8 - ~Oct. 29)

- Review assignments are deployed.
- Authors, reviewers, areachairs, and members of the public may continue to post comments under the same permissions as above.
- Reviewers and areachairs may no longer bid on papers.
- Review and meta-review tasks deployed.
- Reviews are visible to to paper area chairs and program chairs immediately upon creation.
- Reviews are hidden from reviewers until they post their own review.
- Reviews will be made available to the public during the rebuttal period
- Reviewer identity is revealed only to the paper’s area chair and to the program chairs, *not* to the other reviewers. This is important so that reviews can be rated honestly later.
- - Important: reviewers *should not* reveal their identities in any part of the discussion.
- Reviewer and areachair assignments consoles are enabled.
- Area chairs can send messages and reminders to reviewers through the AC console.


'''

import openreview
import akbc19
import notes
import groups
import invitations
import argparse
from collections import defaultdict

def getAnonReviewersByForum(blind_note):
    anonreviewer_ids = []
    reg = 'AKBC.ws/2019/Conference/Paper' + str(blind_note.number) + '/AnonReviewer.*'
    anonreviewers = client.get_groups(regex=reg)
    anonreviewer_ids = [an.id for an in anonreviewers]
    return anonreviewer_ids

if __name__ == '__main__':
    ## Argument handling
    parser = argparse.ArgumentParser()
    parser.add_argument('--baseurl', help="base url")
    parser.add_argument('--username')
    parser.add_argument('--password')
    args = parser.parse_args()

    client = openreview.Client(baseurl=args.baseurl, username=args.username, password=args.password)

    blind_submissions = openreview.tools.iterget_notes(client, invitation=akbc19.BLIND_SUBMISSION_ID)

    for blind_note in blind_submissions:
        groups.create_and_post(
            client, blind_note, 'Paper/Reviewers/Submitted')

        groups.create_and_post(
            client, blind_note, 'Paper/Reviewers/Unsubmitted',
            members=getAnonReviewersByForum(blind_note))
        
        client.post_invitation(invitations.enable_invitation('Official_Review', blind_note))
        client.post_invitation(invitations.enable_invitation('Meta_Review', blind_note))

        

