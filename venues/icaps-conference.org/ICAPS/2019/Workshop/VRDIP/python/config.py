#!/usr/bin/python

import openreview


def get_conference(client):

    builder = openreview.conference.ConferenceBuilder(client)

    builder.set_conference_id('icaps-conference.org/ICAPS/2019/Workshop/VRDIP')
    builder.set_conference_name('Planning the Future: Economics and Value-Rational')
    builder.set_conference_short_name('ICAPS Workshop 2019 VRDIP')
    builder.set_homepage_header({
    'title': 'Planning the Future: Economics and Value-Rational',
    'subtitle': 'ICAPS 2019 Workshop',
    'deadline': 'Submission Deadline: April 15, 2019',
    'date': 'July 11, 2019',
    'website': 'https://icaps19.icaps-conference.org/workshops/Planning-the-Future/index.html',
    'location': 'Berkeley, CA, USA'
    })
    builder.set_double_blind(True)
    builder.set_submission_public(True)
    return builder.get_result()

