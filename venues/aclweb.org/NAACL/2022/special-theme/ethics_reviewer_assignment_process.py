def process_update(client, edge, invitation, existing_edge):

    SHORT_PHRASE = 'NAACL 2022 Conference'
    GROUP_ID = 'aclweb.org/NAACL/2022/Conference/Special_Theme_Ethics_Reviewers'
    PAPER_GROUP_ID = 'aclweb.org/NAACL/2022/Conference/Paper{number}/Special_Theme_Ethics_Reviewers'
    print(edge.id)
    print(invitation.id)
    print(existing_edge)

    note=client.get_note(edge.head)
    group=client.get_group(PAPER_GROUP_ID.format(number=note.number))
    if edge.ddate and edge.tail in group.members:
        print(f'Remove member {edge.tail} from {group.id}')
        client.remove_members_from_group(group.id, edge.tail)

    if not edge.ddate and edge.tail not in group.members:
        print(f'Add member {edge.tail} to {group.id}')
        client.add_members_to_group(group.id, edge.tail)
        client.add_members_to_group(GROUP_ID, edge.tail)

        recipients=[edge.tail]
        subject=f'[{SHORT_PHRASE}] You have been assigned as an Ethic Reviewer for paper number {note.number}'
        message=f'''This is to inform you that you have been assigned as an Ethic Reviewer for paper number {note.number} for {SHORT_PHRASE}.

To review this new assignment, please login to OpenReview and go to https://openreview.net/forum?id={note.forum}.

To check all of your assigned papers, go to https://openreview.net/group?id={GROUP_ID}.

Thank you,

NAACL 2022 Conference Ethics Chairs'''

        client.post_message(subject, recipients, message, parentGroup=group.id)
