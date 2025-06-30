#!/usr/bin/python

import openreview


def get_conference(client):

    builder = openreview.conference.ConferenceBuilder(client)

    builder.set_conference_id('ICML.cc/2019/Workshop/RL4RealLife')
    builder.set_conference_name('Reinforcement Learning for Real Life')
    builder.set_conference_short_name('RL4RealLife 2019')
    builder.set_homepage_header({
    'title': 'Reinforcement Learning for Real Life',
    'subtitle': 'An ICML Workshop',
    'deadline': 'Submission Deadline: May 1, midnight GMT',
    'date': 'June 14th, 2019',
    'website': 'https://sites.google.com/view/RL4RealLife',
    'location': 'Long Beach, CA, USA'
    })
    builder.set_double_blind(False)
    builder.set_submission_public(True)
    #builder.set_override_homepage(True)
    return builder.get_result()
