import openreview
import argparse
import datetime

if __name__ == '__main__':
    ## Argument handling
    parser = argparse.ArgumentParser()
    parser.add_argument('--baseurl', help="base url")
    parser.add_argument('--username')
    parser.add_argument('--password')
    args = parser.parse_args()

    client = openreview.Client(baseurl=args.baseurl, username=args.username, password=args.password)

    conference = openreview.helpers.get_conference(client, 'SkxpQPWdA4')

    pc_group = client.get_group(conference.get_program_chairs_id())
    updated_pc_group = openreview.tools.replace_members_with_ids(client, pc_group)
    pc_names_list = []
    for pc_id in updated_pc_group.members:
        if '@' in pc_id:
            pc_names_list.append(pc_id)
        elif pc_id.startswith('~'):
            pc_names_list.append(pc_id[1:-1].strip('.').replace('_', ' '))


    tag_invitation_id = conference.get_id() + '/-/Assigned_to_PC'
    tag_invitation = client.get_invitations(regex = tag_invitation_id, tags = True)
    map_forum_tag = {}
    if len(tag_invitation):
        existing_tags = openreview.tools.iterget_tags(
            client,
            invitation = tag_invitation_id
        )
        map_forum_tag = {tag.forum: tag for tag in existing_tags}
    else:
        posted_invitation = client.post_invitation(
            openreview.Invitation(
                readers = [conference.get_program_chairs_id()],
                invitees = ['OpenReview.net/Support'],
                id = tag_invitation_id,
                signatures = ['OpenReview.net/Support'],
                writers = ['OpenReview.net/Support'],
                duedate = 1577750340000,
                expdate = 1577750340000,
                multiReply = False,
                reply = {
                    'invitation' : conference.get_submission_id(),
                    'readers' : {
                        'description': 'The users who will be allowed to read the above content.',
                        'values-regex': [conference.get_program_chairs_id()]
                    },
                    'signatures' : {
                        'description': 'How your identity will be displayed with the above content.',
                        'values-regex': [conference.get_program_chairs_id()]
                    },
                    'writers': {
                        'values': [conference.get_program_chairs_id()]
                    },
                    'content': {
                        'tag': {
                            'description': 'Assign Program Chair',
                            'order': 1,
                            'value-dropdown': pc_names_list,
                            'required': True
                        }
                    }
                }
            )
        )

    notes = list(conference.get_submissions())
    paper_count = len(notes)

    for index, paper in enumerate(notes):
        pc_selected = pc_names_list[index % len(pc_names_list)]
        if paper.forum not in map_forum_tag:
            tag = client.post_tag(
                openreview.Tag(
                    invitation = tag_invitation_id,
                    readers = [conference.get_program_chairs_id()],
                    signatures = [conference.get_program_chairs_id()],
                    forum = paper.forum,
                    tag = pc_selected
                )
            )
            print (paper.forum, ' assigned to PC ', pc_selected)
        else:
            print (paper.forum, ' was already assigned to PC ', map_forum_tag[paper.forum].tag)

