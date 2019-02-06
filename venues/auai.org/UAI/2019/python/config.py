#!/usr/bin/python

import openreview

def get_conference(client):

    builder = openreview.conference.ConferenceBuilder(client)
    builder.set_conference_id('auai.org/UAI/2019/Conference')
    builder.set_conference_name('Conference on Uncertainty in Artificial Intelligence')
    builder.set_conference_short_name('UAI 2019')
    builder.set_homepage_header({
    'title': 'UAI 2019',
    'subtitle': 'Conference on Uncertainty in Artificial Intelligence',
    'deadline': 'Submission Deadline: 11:59 pm Samoa Standard Time, March 4, 2019',
    'date': 'June 22 - June 26, 2019',
    'website': 'http://auai.org/uai2019/',
    'location': 'Tel Aviv, Israel'
    })
    print ('Homepage header set')
    builder.set_conference_area_chairs_name('Senior_Program_Committee')
    builder.set_conference_reviewers_name('Program_Committee')
    return builder.get_result()
