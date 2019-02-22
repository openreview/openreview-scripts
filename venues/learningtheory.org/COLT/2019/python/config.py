#!/usr/bin/python

import openreview

def get_conference(client):

    builder = openreview.conference.ConferenceBuilder(client)
    builder.set_conference_id('learningtheory.org/COLT/2019/Conference')
    builder.set_conference_name('Conference on Learning Theory')
    builder.set_conference_short_name('COLT 2019')
    builder.set_homepage_header({
    'title': 'COLT 2019',
    'subtitle': 'Conference on Learning Theory',
    'deadline': 'Submission Deadline: 11:00pm Eastern Standard Time, February 1, 2019',
    'date': 'June 25 - June 28, 2019',
    'website': 'http://learningtheory.org/colt2019/',
    'location': 'Phoenix, Arizona, United States'
    })
    builder.set_conference_area_chairs_name('Program_Committee')
    builder.enable_double_blind(read_area_chairs = True, read_program_chairs = True)
    return builder.get_result()
