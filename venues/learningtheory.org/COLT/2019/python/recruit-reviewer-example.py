import config
import argparse
import openreview
import datetime
from Crypto.Hash import HMAC, SHA256
hash_seed = "1234"

if __name__ == '__main__':
    ## Argument handling
    parser = argparse.ArgumentParser()
    parser.add_argument('--baseurl', help="base url")
    parser.add_argument('--username')
    parser.add_argument('--password')
    args = parser.parse_args()

    client = openreview.Client(baseurl=args.baseurl, username=args.username, password=args.password)
    conference = config.get_conference(client)

    program_committee = 'spector@cs.umass.edu'

    # Create paper groups and assign them to a program committee
    for n in openreview.tools.iterget_notes(client, invitation = conference.get_submission_id()):
        pc_group_id = "{conference_id}/Paper{number}/Program_Committee".format(conference_id = conference.get_id(), number = n.number)
        group_id = "{conference_id}/Paper{number}/Reviewers".format(conference_id = conference.get_id(), number = n.number)
        group_invited_id = "{conference_id}/Paper{number}/Reviewers/Invited".format(conference_id = conference.get_id(), number = n.number)
        group_declined_id = "{conference_id}/Paper{number}/Reviewers/Declined".format(conference_id = conference.get_id(), number = n.number)
        client.post_group(openreview.Group(id = group_id,
                                        readers = [group_id, conference.get_id(), pc_group_id],
                                        writers = [conference.get_id(), pc_group_id],
                                        signatures = [conference.get_id()],
                                        signatories = [group_id]))
        client.post_group(openreview.Group(id = group_invited_id,
                                        readers = [conference.get_id(), pc_group_id],
                                        writers = [conference.get_id(), pc_group_id],
                                        signatures = [conference.get_id()],
                                        signatories = [conference.get_id()]))
        client.post_group(openreview.Group(id = group_declined_id,
                                        readers = [conference.get_id(), pc_group_id],
                                        writers = [conference.get_id(), pc_group_id],
                                        signatures = [conference.get_id()],
                                        signatories = [conference.get_id()]))

        openreview.tools.assign(client=client,
                                conference=conference.get_id(),
                                paper_number=n.number,
                                reviewer_to_add=program_committee,
                                parent_label = 'Program_Committees',
                                individual_label = 'Program_Committee',
                                individual_group_params = {
                                    'readers': [
                                        conference.get_id(),
                                        conference.get_program_chairs_id(),
                                        'learningtheory.org/COLT/2019/Conference/Paper{0}/Program_Committee'.format(n.number)
                                    ],
                                    'signatories': ['learningtheory.org/COLT/2019/Conference/Paper{0}/Program_Committee'.format(n.number)]
                                    },
                            parent_group_params = {
                                    'readers': [
                                        conference.get_id(),
                                        conference.get_program_chairs_id(),
                                        'learningtheory.org/COLT/2019/Conference/Paper{0}/Program_Committees'.format(n.number)
                                    ],
                                    'signatories': ['learningtheory.org/COLT/2019/Conference/Paper{0}/Program_Committees'.format(n.number)]
                                    })
    print('DONE.')
