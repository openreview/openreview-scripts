

import openreview
import akbc19 as conference_config
import notes
import groups
import invitations
import argparse
from collections import defaultdict

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

    assignment_notes = openreview.tools.iterget_notes(client,
        invitation=conference_config.ASSIGNMENT_INV_ID,
        details='forumContent')

    def get_number_from_details(note_details):
        '''
        The forum content in the "details" field doesn't have the actual paper number,
        so we have to infer it from the group in authorids.
        '''

        authorids = note_details['forumContent']['authorids']
        assert len(authorids) == 1, 'something went wrong: no authorids in paper with title {}'.format(
            note_details['forumContent']['title'])
        paper_authors_id = authorids[0]
        authorgroup_components = paper_authors_id.split('/')
        paper_num = authorgroup_components[3]
        num = int(paper_num.split('Paper')[1])
        return num

    for assignment_note in assignment_notes:
        if assignment_note.content['label'] == args.label:
            paper_number = get_number_from_details(assignment_note.details)
            assignment_entries = assignment_note.content['assignedGroups']
            paper_specific_area_chairs = conference_config.CONFERENCE_ID + '/Paper{}'.format(paper_number) + "/Area_Chairs"

            if args.type == 'reviewers':
                parent_label = 'Reviewers'
                individual_label = 'AnonReviewer'
                individual_group_params = {'readers': [
                    paper_specific_area_chairs,
                    conference_config.PROGRAM_CHAIRS_ID
                ]}

            elif args.type == 'areachairs':
                parent_label = 'Area_Chairs'
                individual_label = 'Area_Chair'
                individual_group_params = {'readers': [
                    conference_config.PROGRAM_CHAIRS_ID
                ]}

            for entry in assignment_entries:
                new_assigned_group = openreview.tools.add_assignment(
                    client, paper_number, conference_config.CONFERENCE_ID, entry['userId'],
                    parent_label = parent_label,
                    individual_label = individual_label,
                    individual_group_params = individual_group_params)
                print('new_assigned_group', new_assigned_group)
