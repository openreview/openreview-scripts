

import openreview
import config
import argparse


if __name__ == '__main__':
    ## Argument handling
    parser = argparse.ArgumentParser()
    parser.add_argument('type', help='enter "areachairs" or "reviewers"')
    parser.add_argument('label')
    parser.add_argument('--baseurl', help="base url")
    parser.add_argument('--username')
    parser.add_argument('--password')
    args = parser.parse_args()

    assert args.type in ['areachairs','reviewers'], 'input "type" must be either "areachairs" or "reviewers"'

    client = openreview.Client(baseurl=args.baseurl, username=args.username, password=args.password)

    conference = config.get_conference(client)

    # find paper_number by forum because Paper_Assignments include forum info,
    # but add_assignment() needs paper_number
    notes = openreview.tools.iterget_notes(client, invitation=conference.get_submission_id())
    number_by_forum = {}
    for note in notes:
        number_by_forum[note.forum] = note.number

    assignment_notes = openreview.tools.iterget_notes(client,
                                                      invitation='/'.join([conference.get_id(), '-', 'Paper_Assignment']))
    for assignment_note in assignment_notes:
        if assignment_note.content['label'] == args.label:
            paper_number = number_by_forum[assignment_note.forum]
            assignment_entries = assignment_note.content['assignedGroups']

            if args.type == 'reviewers':
                parent_label = 'Reviewers'
                individual_label = 'AnonReviewer'
                individual_group_params = {'readers': [
                    conference.get_area_chairs_id(),
                    conference.get_program_chairs_id()
                ]}

            elif args.type == 'areachairs':
                parent_label = 'Area_Chairs'
                individual_label = 'Area_Chair'
                individual_group_params = {'readers': [
                    conference.get_program_chairs_id()
                ]}

            for entry in assignment_entries:
                new_assigned_group = openreview.tools.add_assignment(
                    client, paper_number, conference.get_id(), entry['userId'],
                    parent_label = parent_label,
                    individual_label = individual_label,
                    individual_group_params = individual_group_params)
                print('new_assigned_group', new_assigned_group)
