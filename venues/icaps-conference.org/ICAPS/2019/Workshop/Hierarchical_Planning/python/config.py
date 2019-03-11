#!/usr/bin/python

import openreview


def get_conference(client):

    builder = openreview.conference.ConferenceBuilder(client)

    builder.set_conference_id('icaps-conference.org/ICAPS/2019/Workshop/Hierarchical_Planning')
    builder.set_conference_name('Second ICAPS Workshop on Hierarchical Planning')
    builder.set_conference_short_name('ICAPS 2019 Workshop Hierarchical Planning')
    builder.set_homepage_header({
    'title': 'Second Workshop on Hierarchical Planning',
    'subtitle': 'ICAPS 2019 Workshop',
    'deadline': 'Submission Deadline: March 24, 2019 midnight AoE',
    'date': 'July 11-15, 2019',
    'website': 'https://icaps19.icaps-conference.org/workshops/Hierarchical-Planning/index.html',
    'location': 'Berkeley, CA, USA'
    })
    builder.set_double_blind(True)
    
    return builder.get_result()

