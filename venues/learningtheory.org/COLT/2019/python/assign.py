import openreview
import config
import argparse

def getPCmembersByForum(blind_note):
    reg = 'learningtheory.org/COLT/2019/Conference/Paper' + str(blind_note.number) + '/Program_Committee_Member.*'
    anonreviewers = client.get_groups(regex=reg)
    anonreviewer_ids = [anon.id for anon in anonreviewers]
    return anonreviewer_ids

def get_assignments(submissions):
    assignments = []

    paper_by_forum = {n.forum: n for n in submissions}

    config_notes = client.get_notes(invitation='learningtheory.org/COLT/2019/Conference/-/Assignment_Configuration', content = { 'label': args.label})
    config_note = config_notes[0]
    added_constraints = config_note.content['constraints']

    for assignment in openreview.tools.iterget_notes(client, invitation='learningtheory.org/COLT/2019/Conference/-/Paper_Assignment', content = { 'label': args.label}):
        assigned_groups = assignment.content['assignedGroups']
        paper_constraints = added_constraints.get(assignment.forum, {})
        paper_assigned = []
        for assignment_entry in assigned_groups:
            score = assignment_entry['scores'].get('bid', 0)
            pc_member = assignment_entry['userId']
            paper_assigned.append(pc_member)

            paper = paper_by_forum.get(assignment.forum)

            if paper and paper_constraints.get(pc_member) != '-inf':
                current_row = [paper.number, paper.forum, pc_member, score]
                assignments.append(current_row)

        for user, constraint in paper_constraints.items():
            print('user, constraint', user, constraint)
            if user not in paper_assigned and constraint == '+inf':
                current_row = [paper.number, paper.forum, user, '99']
                assignments.append(current_row)


    return sorted(assignments, key=lambda x: x[0])

if __name__ == '__main__':
    ## Argument handling
    parser = argparse.ArgumentParser()
    parser.add_argument('label')
    parser.add_argument('--baseurl', help="base url")
    parser.add_argument('--username')
    parser.add_argument('--password')
    args = parser.parse_args()

    client = openreview.Client(baseurl=args.baseurl, username=args.username, password=args.password)

    conference = config.get_conference(client)
    submissions = client.get_notes(invitation='learningtheory.org/COLT/2019/Conference/-/Blind_Submission')


    assignments = get_assignments(submissions)

    for a in assignments:
        paper_number = a[0]
        user = a[2]
        parent_label = 'Program_Committee'
        individual_label = 'Program_Committee_Member'
        individual_group_params = {
            'readers': [
                conference.get_id(),
                conference.get_program_chairs_id()
            ]
        }
        parent_group_params = {
            'readers': [
                conference.get_id(),
                conference.get_program_chairs_id(),
                'learningtheory.org/COLT/2019/Conference/Paper{0}/Program_Committee'.format(paper_number)
            ],
            'signatories': ['learningtheory.org/COLT/2019/Conference/Paper{0}/Program_Committee'.format(paper_number)]
        }

        new_assigned_group = openreview.tools.add_assignment(
            client, paper_number, conference.get_id(), user,
            parent_label = parent_label,
            individual_label = individual_label,
            individual_group_params = individual_group_params,
            parent_group_params = parent_group_params)


    # Templates for unsubmitted and submitted groups of Program Committee
    pcs_unsubmitted_template = {
        'id': conference.get_id() + '/Paper<number>/Program_Committee/Unsubmitted',
        'readers':[
            conference.get_id(),
            conference.get_program_chairs_id()
        ],
        'writers': [conference.get_id()],
        'signatures': [conference.get_id()],
        'signatories': [conference.get_id()],
        'members': []
    }

    pcs_submitted_template = {
        'id': conference.get_id() + '/Paper<number>/Program_Committee/Submitted',
        'readers':[
            conference.get_id(),
            conference.get_program_chairs_id()
        ],
        'writers': [conference.get_id()],
        'signatures': [conference.get_id()],
        'signatories': [conference.get_id()],
        'members': []
    }

    # Post unsubmitted and submitted program committee groups for each blind note
    for paper in submissions:
        group_to_post = openreview.Group.from_json(
        openreview.tools.fill_template(
            pcs_unsubmitted_template, paper))

        members = getPCmembersByForum(paper)
        group_to_post.members = members
        print ("Group posted :", client.post_group(group_to_post).id)

        group_to_post = openreview.Group.from_json(
        openreview.tools.fill_template(
            pcs_submitted_template, paper))
        print ("Group posted :", client.post_group(group_to_post).id)

