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

    # update_homepage(conference)

    conference_id = conference.get_id()
    ac_group = client.get_group(conference.get_area_chairs_id())

    buddy_ac_group = client.post_group(
        openreview.Group(
            id = conference_id + '/' + buddy_ac_parent_group_name,
            readers = [
                conference_id,
                conference.get_program_chairs_id(),
                conference.get_area_chairs_id()],
            signatories = [conference_id + '/' + buddy_ac_parent_group_name],
            signatures = [conference.get_id()],
            writers = [conference.get_id()],
            web = 'buddyAreachairWebfield.js',
            members = ac_group.members
        )
    )

    submissions = conference.get_submissions()
    for paper in submissions:
        paper_number = str(paper.number)
        individual_group_id = conference_id + '/Paper' + paper_number + '/' + buddy_ac_individual_group_name
        print (individual_group_id)
        individual_buddy_group = client.post_group(
            openreview.Group(
                id = individual_group_id,
                readers = [
                    conference_id,
                    conference.get_program_chairs_id(),
                    individual_group_id],
                nonreaders = [conference_id + '/Paper' + paper_number + '/Authors'],
                signatories = [individual_group_id],
                signatures = [conference.get_id()],
                writers = [conference.get_id()],
                members = ['~Mohit_Uniyal1']
            )
        )

        ac_conversation_invitation = openreview.Invitation(
            id = conference_id + '/Paper' + paper_number + '/-/Area_Chair_Only_Comment',
            # super = 'ICLR.cc/2020/Conference/-/Area_Chair_Internal_Comment',
            readers = ['everyone'],
            writers = [conference_id],
            signatures = [conference_id],
            invitees = [
                conference.get_area_chairs_id(number = paper_number), individual_group_id
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
        individual_group_id = conference_id + '/Paper' + paper_number + '/' + buddy_ac_individual_group_name
        if individual_group_id not in anon_rev.readers:
            anon_rev.readers.append(individual_group_id)

        upd_anon = client.post_group(anon_rev)