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
import iclr19
import notes
import groups
import invitations
import argparse

if __name__ == '__main__':
    ## Argument handling
    parser = argparse.ArgumentParser()
    parser.add_argument('--reviewer_label', required=True)
    parser.add_argument('--areachair_label', required=True)
    parser.add_argument('--baseurl', help="base url")
    parser.add_argument('--username')
    parser.add_argument('--password')
    args = parser.parse_args()

    client = openreview.Client(baseurl=args.baseurl, username=args.username, password=args.password)

    blind_submissions = openreview.tools.iterget_notes(client, invitation=iclr19.BLIND_SUBMISSION_ID)

    assignment_notes = openreview.tools.iterget_notes(client,
        invitation=iclr19.ASSIGNMENT_INV_ID,
        details='forumContent')

    def get_number_from_details(note_details):
        '''
        The forum content in the "details" field doesn't have the actual paper number,
        so we have to infer it from the group in authorids.
        '''

        authorids = note_details['forumContent']['authorids']
        assert len(authorids) == 1, 'something went wrong: no authorids in paper with title {}'.format(
            forum_content['title'])
        paper_authors_id = authorids[0]
        authorgroup_components = paper_authors_id.split('/')
        paper_num = authorgroup_components[3]
        num = int(paper_num.split('Paper')[1])
        return num

    for assignment_note in assignment_notes:
        paper_number = get_number_from_details(assignment_note.details)
        assignment_entries = assignment_note.content['assignedGroups']

        if args.reviewer_label == assignment_note.content['label']:
            parent_label = 'Reviewers'
            individual_label = 'AnonReviewer'
            individual_group_params = {'readers': [
                iclr19.AREA_CHAIRS_ID,
                iclr19.PROGRAM_CHAIRS_ID
            ]}
        if args.areachair_label == assignment_note.content['label']:
            parent_label = 'Area_Chairs'
            individual_label = 'Area_Chair'
            individual_group_params = {'readers': [
                iclr19.PROGRAM_CHAIRS_ID
            ]}

        for entry in assignment_entries:
            openreview.tools.assign(client, paper_number, iclr19.CONFERENCE_ID,
                reviewer_to_add = entry['userId'],
                parent_label = parent_label,
                individual_label = individual_label,
                individual_group_params = individual_group_params)

    for blind_submission in blind_submissions:
        client.post_invitation(invitations.enable_invitation('Official_Review', blind_submission))
        client.post_invitation(invitations.enable_invitation('Meta_Review', blind_submission))

