#!/usr/bin/python

import openreview


def get_conference(client):

    builder = openreview.conference.ConferenceBuilder(client)

    builder.set_conference_id('ICLR.cc/2019/Workshop/RML')
    builder.set_conference_name('Reproducibility in Machine Learning')
    builder.set_conference_short_name('RML 2019')
    builder.set_homepage_header({
    'title': 'Reproducibility in Machine Learning',
    'subtitle': 'ICLR 2019 Workshop',
    'deadline': 'Submission Deadline: 5 March 2019 11:59pm EST',
    'date': '6 May 2019',
    'website': 'https://iclr.cc/Conferences/2019/Schedule?showEvent=635',
    'location': 'New Orleans, Louisiana, United States'
    })
    builder.set_authorpage_header({'schedule':
      '''<h4>Submission Period</h4>
        <p><ul>
          <li><strong>Submission deadline: 5 March 11:59pm EST</strong></li>
          <li>Authors can revise their paper as many times as needed up to the paper submission deadline.</li>
          <li>Please ensure that the email addresses of the corresponding author are up-to-date in his or her profile.</li>
          <li>Update your profile to include your most up-to-date information, including work history and relations, to ensure proper conflict-of-interest detection during the paper matching process.</li>
        </ul></p>
      <br>
      <h4>Reviewing Period</h4>
        <p><ul>
          <li><strong>Reviews can be expected on March 28, 2019 </strong></li>
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
