#!/usr/bin/python

import openreview


def get_conference(client):

    builder = openreview.conference.ConferenceBuilder(client)

    builder.set_conference_id('icaps-conference.org/ICAPS/2019/Workshop/KEPS')
    builder.set_conference_name('Workshop on Knowledge Engineering for Planning and Scheduling')
    builder.set_conference_short_name('ICAPS KEPS 2019')
    builder.set_homepage_header({
    'title': 'Workshop on Knowledge Engineering for Planning and Scheduling',
    'subtitle': 'ICAPS 2019 Workshop',
    'deadline': 'Submission Deadline: March 15, 2019',
    'date': 'July 11-15, 2019',
    'website': 'https://icaps19.icaps-conference.org/workshops/KEPS/index.html',
    'location': 'Berkeley, CA, USA'
    })
    builder.set_double_blind(True)
    builder.set_submission_public(True)
    return builder.get_result()

