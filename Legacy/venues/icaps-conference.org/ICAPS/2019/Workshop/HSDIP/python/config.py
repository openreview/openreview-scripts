#!/usr/bin/python

import openreview


def get_conference(client):

    builder = openreview.conference.ConferenceBuilder(client)

    builder.set_conference_id('icaps-conference.org/ICAPS/2019/Workshop/HSDIP')
    builder.set_conference_name('Heuristics and Search for Domain-independent Planning')
    builder.set_conference_short_name('ICAPS HSDIP 2019')
    builder.set_homepage_header({
    'title': 'Heuristics and Search for Domain-independent Planning',
    'subtitle': 'ICAPS 2019 Workshop',
    'deadline': 'Submission Deadline: March 17, 2019 midnight AoE',
    'date': 'July 11-15, 2019',
    'website': 'https://icaps19.icaps-conference.org/workshops/HSDIP/index.html',
    'location': 'Berkeley, CA, USA'
    })
    builder.set_double_blind(True)
    builder.set_submission_public(True)
    return builder.get_result()

