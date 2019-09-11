import openreview
import argparse
import datetime

buddy_ac_parent_group_name = 'Buddy_Area_Chairs'
buddy_ac_individual_group_name = 'Buddy_Area_Chair1'

# def update_homepage():

if __name__ == '__main__':
    ## Argument handling
    parser = argparse.ArgumentParser()
    parser.add_argument('--baseurl', help="base url")
    parser.add_argument('--username')
    parser.add_argument('--password')
    args = parser.parse_args()

    client = openreview.Client(baseurl=args.baseurl, username=args.username, password=args.password)
    conference = openreview.helpers.get_conference(client, 'SkxpQPWdA4')

    conference_id = conference.get_id()

    buddy_ac_parent_group = client.get_groups(regex = conference_id + '/' + buddy_ac_parent_group_name)

    if not buddy_ac_parent_group:
        ac_group = client.get_group(conference.get_area_chairs_id())

        buddy_ac_group = client.post_group(
            openreview.Group(
                id = conference_id + '/' + buddy_ac_parent_group_name,
                readers = [
                    conference_id,
                    conference.get_program_chairs_id(),
                    conference.get_area_chairs_id()
                ],
                signatories = [conference_id + '/' + buddy_ac_parent_group_name],
                signatures = [conference_id],
                writers = [conference_id],
                web = 'buddyAreachairWebfield.js',
                members = ac_group.members
            )
        )

    map_meta_review_invitations = {invitation.id.split('Paper')[1].split('/')[0]: invitation for invitation in openreview.tools.iterget_invitations(client, regex = conference_id + '/Paper[0-9]+/-/Meta_Review')}

    map_paper_ac_groups = {group.id.split('Paper')[1].split('/')[0]: group for group in openreview.tools.iterget_groups(client, regex = conference_id + '/Paper[0-9]+/Area_Chairs$')}

    submissions = conference.get_submissions()
    for paper in submissions:
        paper_number = str(paper.number)
        individual_buddy_group_id = conference_id + '/Paper' + paper_number + '/' + buddy_ac_individual_group_name

        ## Create buddy ac group for this paper
        individual_buddy_group = client.post_group(
            openreview.Group(
                id = individual_buddy_group_id,
                readers = [
                    conference_id,
                    conference.get_program_chairs_id(),
                    individual_buddy_group_id],
                nonreaders = [conference_id + '/Paper' + paper_number + '/Authors'],
                signatories = [individual_buddy_group_id],
                signatures = [conference.get_id()],
                writers = [conference.get_id()],
                members = []
            )
        )

        # Add paper's buddy AC as member to paper's AC group
        paper_ac_group = map_paper_ac_groups[paper_number]
        client.add_members_to_group(paper_ac_group, individual_buddy_group_id)

        # Add paper's buddy AC as non-invitee for paper's meta-review invitation
        paper_meta_rev_invitation = map_meta_review_invitations.get(paper_number, None)
        if (paper_meta_rev_invitation):
            paper_meta_rev_invitation.noninvitees = individual_buddy_group_id
            client.post_invitation(paper_meta_rev_invitation)

        ## Post AC & AC-Buddy only Comment invitation for this paper
        ac_conversation_invitation = openreview.Invitation(
            id = conference_id + '/Paper' + paper_number + '/-/Area_Chair_Only_Comment',
            readers = [
                conference.get_area_chairs_id(number = paper_number),
                individual_buddy_group_id,
                conference_id
            ],
            writers = [conference_id],
            signatures = [conference_id],
            invitees = [
                conference.get_area_chairs_id(number = paper_number), individual_buddy_group_id
            ],
            reply = {
                "forum" : paper.forum,
                "readers": {
                    "description": "Select all user groups that should be able to read this comment.",
                    "values": [
                        "ICLR.cc/2020/Conference/Paper" + paper_number + "/Area_Chairs",
                        "ICLR.cc/2020/Conference/Paper" + paper_number + "/Buddy_Area_Chair1",
                        conference.get_program_chairs_id()
                    ]
                    },
                "writers": {
                    "values-regex": "ICLR.cc/2020/Conference/Paper6/(Buddy_)*Area_Chair[0-9]+",
                    "description": "How your identity will be displayed."
                },
                "signatures": {
                    "values-regex": "ICLR.cc/2020/Conference/Paper6/(Buddy_)*Area_Chair[0-9]+",
                    "description": "How your identity will be displayed."
                },
                "content": {
                    "comment": {
                        "value-regex": "[\\S\\s]{1,5000}",
                        "required": True,
                        "order": 1,
                        "description": "Your comment or reply (max 5000 characters)."
                    },
                    "title": {
                        "value-regex": ".{1,500}",
                        "required": True,
                        "order": 0,
                        "description": "Brief summary of your comment."
                    }
                }
            },
            process = 'buddyAcCommentProcess.js'
        )
        client.post_invitation(ac_conversation_invitation)

    all_anon_revs = openreview.tools.iterget_groups(client, regex = 'ICLR.cc/2020/Conference/Paper[0-9]+/AnonReviewer[0-9]+')
    for anon_rev in all_anon_revs:
        paper_number = str(anon_rev.id.split('Paper')[1].split('/')[0])
        individual_buddy_group_id = conference_id + '/Paper' + paper_number + '/' + buddy_ac_individual_group_name
        if individual_buddy_group_id not in anon_rev.readers:
            anon_rev.readers.append(individual_buddy_group_id)
        upd_anon = client.post_group(anon_rev)
