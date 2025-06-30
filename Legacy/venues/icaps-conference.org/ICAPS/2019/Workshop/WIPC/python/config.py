#!/usr/bin/python

import openreview


def get_conference(client):

    builder = openreview.conference.ConferenceBuilder(client)

    builder.set_conference_id('icaps-conference.org/ICAPS/2019/Workshop/WIPC')
    builder.set_conference_name('Workshop on the International Planning Competition')
    builder.set_conference_short_name('ICAPS WIPC 2019')
    builder.set_homepage_header({
    'title': 'Workshop on the International Planning Competition',
    'subtitle': 'ICAPS Workshop',
    'deadline': 'Submission Deadline: April 12th, midnight AoE',
    'date': 'July 11-12, 2019',
    'website': 'https://icaps19.icaps-conference.org/workshops/WIPC/index.html',
    'location': 'Berkeley, CA, USA'
    })
    builder.set_double_blind(True)
    builder.set_override_homepage(True)

    return builder.get_result()

