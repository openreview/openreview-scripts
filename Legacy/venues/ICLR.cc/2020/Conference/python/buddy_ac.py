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

        print('Posted ', client.post_group(
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
        ).id)

    map_meta_review_invitations = {invitation.id.split('Paper')[1].split('/')[0]: invitation for invitation in openreview.tools.iterget_invitations(client, regex = conference_id + '/Paper[0-9]+/-/Meta_Review')}

    map_paper_ac_parent_groups = {group.id.split('Paper')[1].split('/')[0]: group for group in openreview.tools.iterget_groups(client, regex = conference_id + '/Paper[0-9]+/Area_Chairs$')}

    map_paper_ac_individual_groups = {group.id.split('Paper')[1].split('/')[0]: group for group in openreview.tools.iterget_groups(client, regex = conference_id + '/Paper[0-9]+/Area_Chair1$')}

    map_paper_buddy_ac_groups = {group.id.split('Paper')[1].split('/')[0]: group for group in openreview.tools.iterget_groups(client, regex = conference_id + '/Paper[0-9]+/' + buddy_ac_individual_group_name + '$')}

    map_paper_to_official_comment_invitations = {invitation.id.split('Paper')[1].split('/')[0]: invitation for invitation in openreview.tools.iterget_invitations(client, regex = conference_id + '/Paper[0-9]+/-/Official_Comment')}

    submissions = conference.get_submissions()
    for paper in submissions:
        paper_number = str(paper.number)
        individual_buddy_group_id = conference_id + '/Paper' + paper_number + '/' + buddy_ac_individual_group_name

        ## Create buddy ac group for this paper
        if paper_number not in map_paper_buddy_ac_groups:
            print('Posted ', client.post_group(
                openreview.Group(
                    id = individual_buddy_group_id,
                    readers = [
                        conference_id,
                        conference.get_program_chairs_id(),
                        conference.get_area_chairs_id(paper_number)],
                    nonreaders = [conference_id + '/Paper' + paper_number + '/Authors'],
                    signatories = [individual_buddy_group_id],
                    signatures = [conference.get_id()],
                    writers = [conference.get_id()],
                    members = []
                )
            ).id)

        paper_ac_individual_group = map_paper_ac_individual_groups.get(paper_number)
        if paper_ac_individual_group and (individual_buddy_group_id not in paper_ac_individual_group.readers):
            paper_ac_individual_group.readers.append(individual_buddy_group_id)
            client.post_group(paper_ac_individual_group)

        # Add paper's buddy AC as member to paper's AC parent group
        paper_ac_parent_group = map_paper_ac_parent_groups[paper_number]
        client.add_members_to_group(paper_ac_parent_group, individual_buddy_group_id)

        # Add paper's buddy AC as non-invitee for paper's meta-review invitation
        paper_meta_rev_invitation = map_meta_review_invitations.get(paper_number, None)
        if (paper_meta_rev_invitation):
            paper_meta_rev_invitation.noninvitees = [individual_buddy_group_id]
            client.post_invitation(paper_meta_rev_invitation)

        ## Update Official Comment invitation for this paper
        official_comment_invitation = map_paper_to_official_comment_invitations[paper_number]
        official_comment_invitation.reply['signatures']['values-regex'] += '|' + conference.get_id() + '/Paper' + paper_number + '/' + buddy_ac_individual_group_name
        client.post_invitation(official_comment_invitation)
