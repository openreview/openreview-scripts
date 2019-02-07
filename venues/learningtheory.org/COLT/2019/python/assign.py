import openreview
import config
import argparse


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

    # find paper_number by forum because Paper_Assignments include forum info,
    # but add_assignment() needs paper_number
    notes = openreview.tools.iterget_notes(client, invitation=conference.get_id() + '/-/Blind_Submission')
    number_by_forum = {}
    for note in notes:
        number_by_forum[note.forum] = note.number

    assignment_notes = openreview.tools.iterget_notes(client,
                                                      invitation='/'.join([conference.get_id(), '-', 'Paper_Assignment']),
                                                      content = {'label' : args.label})
    
    unprocessed_assignments = {}
    for assignment_note in assignment_notes:
        paper_number = number_by_forum.get(assignment_note.forum)
        if paper_number:
            assignment_entries = assignment_note.content['assignedGroups']

            parent_label = 'Program_Committee'
            individual_label = 'Program_Committee_Member'
            individual_group_params = {
                'readers': [
                    conference.get_id(),
                    conference.get_program_chairs_id(),
                    'learningtheory.org/COLT/2019/Conference/Paper{0}/Program_Committee'.format(paper_number)
                ],
                'signatories': ['learningtheory.org/COLT/2019/Conference/Paper{0}/Program_Committee'.format(paper_number)]
            }
            parent_group_params = {
                'readers': [
                    conference.get_id(),
                    conference.get_program_chairs_id(),
                        'learningtheory.org/COLT/2019/Conference/Paper{0}/Program_Committee'.format(paper_number)
                ],
                'signatories': ['learningtheory.org/COLT/2019/Conference/Paper{0}/Program_Committee'.format(paper_number)]
            }

            for entry in assignment_entries:
                new_assigned_group = openreview.tools.add_assignment(
                    client, paper_number, conference.get_id(), entry['userId'],
                    parent_label = parent_label,
                    individual_label = individual_label,
                    individual_group_params = individual_group_params,
                    parent_group_params = parent_group_params)
                print('new_assigned_group', new_assigned_group)
                
        else:
            unprocessed_assignments[assignment_note.forum] = assignment_note.id
    print ('Count of unprocesses assignment notes : ', len(unprocessed_assignments.keys()))
    print ('Forums of unprocessed assignment notes : ', unprocessed_assignments.keys())
