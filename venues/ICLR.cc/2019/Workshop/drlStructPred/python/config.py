#!/usr/bin/python

import openreview


def get_conference(client):

    builder = openreview.conference.ConferenceBuilder(client)

    builder.set_conference_id('ICLR.cc/2019/Workshop/drlStructPred')
    builder.set_conference_name('Deep Reinforcement Learning Meets Structured Prediction')
    builder.set_conference_short_name('drlStructPred 2019')
    builder.set_homepage_header({
    'title': 'Deep Reinforcement Learning Meets Structured Prediction',
    'subtitle': 'ICLR 2019 Workshop',
    'deadline': 'Submission Deadline: 15 March 2019 11:59pm GMT',
    'date': '6 May 2019',
    'website': 'https://sites.google.com/view/iclr2019-drlstructpred',
    'location': 'New Orleans, Louisiana, United States'
    })
    builder.set_authorpage_header({'schedule':
      '''<h4>Submission Period</h4>
        <p><ul>
          <li><strong>Submission deadline: 15 March 11:59pm EST</strong></li>
          <li>Authors can revise their paper as many times as needed up to the paper submission deadline.</li>
          <li>Please ensure that the email addresses of the corresponding author are up-to-date in his or her profile.</li>
          <li>Update your profile to include your most up-to-date information, including work history and relations, to ensure proper conflict-of-interest detection during the paper matching process.</li>
        </ul></p>
      <br>
      <h4>Reviewing Period</h4>
        <p><ul>
          <li><strong>Reviews can be expected on TBD </strong></li>
          <li>During the review period, authors will not be allowed to revise their paper. </li>
        </ul></p>
      <br>
      <h4>Decisions</h4>
        <p><ul>
          <li><strong>TBD </strong></li>
        </ul></p>'''})
    builder.set_double_blind(True)
    builder.set_override_homepage(True)
    return builder.get_result()
