#!/usr/bin/python

import openreview


def get_conference(client):

    builder = openreview.conference.ConferenceBuilder(client)

    builder.set_conference_id('ICLR.cc/2019/Workshop/DeepGenStruct')
    builder.set_conference_name('Deep Generative Models for Highly Structured Data')
    builder.set_conference_short_name('DeepGenStruct 2019')
    builder.set_homepage_header({
    'title': 'Deep Generative Models for Highly Structured Data ',
    'subtitle': 'ICLR 2019 Workshop',
    'deadline': 'Submission Deadline: March 15, 2019',
    'date': 'May 6 - May 9, 2019',
    'website': 'https://deep-gen-struct.github.io/index.html',
    'location': 'New Orleans, Louisiana, United States'
    })
    builder.set_authorpage_header({
        'title': 'Author Console',
        'instructions': 'This are the instructions',
        'schedule': 'To be Defined'
    })
    builder.set_double_blind(True)
    builder.set_override_homepage(True)
    return builder.get_result()
