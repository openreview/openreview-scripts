#!/usr/bin/python

import openreview


def get_conference(client):

    builder = openreview.conference.ConferenceBuilder(client)

    builder.set_conference_id('icaps-conference.org/ICAPS/2019/Workshop/SPARK')
    builder.set_conference_name('Scheduling and Planning Applications Workshop')
    builder.set_conference_short_name('SPARK 2019')
    builder.set_homepage_header({
    'title': 'Scheduling and Planning Applications Workshop',
    'subtitle': 'ICAPS 2019 Workshop',
    'deadline': 'Submission Deadline: April 5, 2019 23:59 GMT',
    'date': 'July 11-15, 2019',
    'website': 'https://icaps19.icaps-conference.org/workshops/SPARK/index.html',
    'location': 'Berkeley, CA, USA'
    })
    builder.set_double_blind(True)
    builder.set_submission_public(True)
    builder.set_override_homepage(True)
    return builder.get_result()

