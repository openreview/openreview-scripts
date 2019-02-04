import argparse
import openreview
from openreview import invitations
import datetime
import os
import config

if __name__ == '__main__':
    ## Argument handling
    parser = argparse.ArgumentParser()
    parser.add_argument('--baseurl', help="base url")
    parser.add_argument('--username')
    parser.add_argument('--password')
    args = parser.parse_args()

    client = openreview.Client(baseurl=args.baseurl, username=args.username, password=args.password)
    conference = config.get_conference(client)

    program_chair_group = conference.set_program_chairs(emails=[])
    with open('../webfield/programChairWebfield.js') as f:
        program_chair_group.web = f.read()
        client.post_group(program_chair_group)

    # set_area_chairs_name
    conference.set_area_chairs_name('Senior_Program_Committee')
    area_chair_group = conference.set_area_chairs(emails=[])
    # with open('../webfield/programChairWebfield.js') as f:
    #     program_chair_group.web = f.read()
    #     client.post_group(program_chair_group)

    conference_group = client.get_group(conference.get_id())
    with open(os.path.abspath('../webfield/homepage.js')) as f:
        conference_group.web = f.read()
        client.post_group(conference_group)

    print('Conference creation complete.')

    print ('inviting SPC members now')

    spc_emails_to_invite = [
        'mohituniyal16apr@gmail.com',
        '~Mohit_Uniyal1',
        'mbok@cs.umass.edu']
    message = 'Please join the Justice league: Accept : {accept_url} \n\n Decline : {decline_url}'

    conference.recruit_reviewers(
        emails = spc_emails_to_invite,
        title = 'UAI 2019: Invitation to serve on the Program Committee',
        message = message,
        reviewers_name = 'Senior_Program_Committee'
    )

    print ('done')
