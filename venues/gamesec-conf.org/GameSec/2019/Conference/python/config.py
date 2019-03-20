#!/usr/bin/python

import openreview

def get_conference(client):

    builder = openreview.conference.ConferenceBuilder(client)

    builder.set_conference_id('gamesec-conf.org/GameSec/2019/Conference')
    builder.set_conference_name('Conference on Decision and Game Theory for Security')
    builder.set_conference_short_name('GameSec 2019')
    builder.set_homepage_header({
    'title': 'Conference on Decision and Game Theory for Security',
    'subtitle': '',
    'deadline': 'Submission Deadline: May 27, 2019, 2019 23:59 AoE',
    'date': ' October 30 - November 1, 2019',
    'website': 'http://www.gamesec-conf.org/',
    'location': 'Stockholm, Sweden',
    'instructions': ''
    })
    builder.set_double_blind(True)

    builder.set_authorpage_header({'schedule':
      '''<h4>Submission Period</h4>
        <p><ul>
          <li><strong>Submission deadline: May 27, 2019</strong></li>
          <li>Authors can revise their paper as many times as needed up to the paper submission deadline.</li>
          <li>Please ensure that the email addresses of the corresponding author are up-to-date in his or her profile.</li>
          <li>Update your profile to include your most up-to-date information, including work history and relations, to ensure proper conflict-of-interest detection during the paper matching process.</li>
        </ul></p>
      <br>
      <h4>Decisions</h4>
        <p><ul>
          <li><strong>TBD </strong></li>
        </ul></p>'''})

    builder.set_reviewerpage_header({'schedule':
      '''<h4>Submission Period</h4>
        <p><ul>
          <li><strong>Submission deadline: May 27, 2019</strong></li>
          <li>Update your profile to include your most up-to-date information, including work history and relations, to ensure proper conflict-of-interest detection during the paper matching process.</li>
        </ul></p>
      <br>
      <h4>Reviewing Period</h4>
        <p><ul>
          <li><strong>TBD</strong></li>
          <li>During the review period, authors will not be allowed to revise their paper. </li>
        </ul></p>'''})

    builder.set_submission_public(False)
    return builder.get_result()


