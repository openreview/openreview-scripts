#!/usr/bin/python

import openreview


def get_conference(client):

    builder = openreview.conference.ConferenceBuilder(client)

    builder.set_conference_id('Demo/2019/Workshop/DoubleBlind')
    builder.set_conference_name('Double Blind Workshop')
    builder.set_conference_short_name('DoubleBlind 2019')
    builder.set_homepage_header({
    'title': 'Double Blind Workshop',
    'subtitle': 'Demo 2019',
    'deadline': 'Submission Deadline: July 1, 2019 11:59pm EST',
    'date': 'Aug 2-4 2019',
    'website': 'https://openreview.net/about',
    'location': 'Some Place, Some Country',
    'instructions': 'Please see the venue website for more information. (This can be replaced with text specific to the workshop.)'
    })
    builder.set_authorpage_header({'schedule':
      '''<em>This text can be changed to suit your needs.</em> <br>
      <h4>Submission Period</h4>
        <p><ul>
          <li><strong>Submission deadline: July 1, 11:59pm EST</strong></li>
          <li>Authors can revise their paper as many times as needed up to the paper submission deadline.</li>
          <li>Please ensure that the email addresses of the corresponding author are up-to-date in his or her profile.</li>
          <li>Update your profile to include your most up-to-date information, including work history and relations, to ensure proper conflict-of-interest detection during the paper matching process.</li>
        </ul></p>'''})
    builder.set_double_blind(True)
    builder.set_override_homepage(True)
    return builder.get_result()
