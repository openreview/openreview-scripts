#!/usr/bin/python

import sys, os
from openreview import tools
"""
GROUPS

Defines constants for CONFERENCE_ID (the name of the conference), and for the names of each group.
All other groups will be named by joining the name with CONFERENCE_ID: <CONFERENCE_ID>/<NAME>

Example:

    CONFERENCE_ID = 'my.conference/2017'
    PROGRAM_CHAIRS = 'Program_Chairs'

    --> my.conference/2017/Program_Chairs

"""

CONFERENCE_ID = 'MIDL.io/2019/Conference'
PROGRAM_CHAIRS = CONFERENCE_ID+'/Program_Chairs'

conference_params = {
    'id': CONFERENCE_ID,
    'readers': ['everyone'],
    'writers': [CONFERENCE_ID],
    'signatures': [],
    'signatories': [CONFERENCE_ID],
    'members': []
}

program_chairs_params = {
    'id': PROGRAM_CHAIRS,
    'readers': [CONFERENCE_ID, PROGRAM_CHAIRS],
    'writers': [CONFERENCE_ID],
    'signatories': [CONFERENCE_ID, PROGRAM_CHAIRS],
    'signatures': [CONFERENCE_ID],
}



code_of_conduct_text = """As a professional scientific community, we are committed to providing an atmosphere that encourages the free expression and exchange of ideas. Consistent with this commitment, it is the policy of the MIDL conference series that all participants in all activities will enjoy a welcoming environment free from unlawful discrimination, harassment and retaliation. All participants in activities of the MIDL conference series also agree to comply with all rules and conditions of the activities, which are subject to change without notice. This policy applies to all participants — attendees, organizers, reviewers, speakers, sponsors, guests, staff, contractors, exhibitors, and volunteers at our conference sessions and conference-related social events — who are required to agree with this code of conduct both during the event and on official communication channels, including social media.

All individuals must behave responsibly in MIDL activities in which they participate, at the MIDL conference, related events and social activities at on-site and off-site locations, and in related online communities and social media. Threatening physical or verbal actions and disorderly or disruptive conduct will not be tolerated. Harassment, including verbal comments relating to gender, sexual orientation, disability, race, ethnicity, religion, age, national origin, gender identity or expression, veteran status or other protected status, or sexual images in public spaces, deliberate intimidation, stalking, unauthorized or inappropriate photography or recording, inappropriate physical contact, and unwelcome sexual attention, will not be tolerated. All individuals participating in activities of the MIDL conference series must comply with these standards of behavior.

Violations should be reported in a timely fashion to the MIDL ombudsperson via ombudsperson@midl.io. The ombudsperson may refuse to deal with a dispute. This decision is at the sole discretion of the ombudsperson.

Unacceptable behavior may cause removal or denial of access to meeting facilities or activities, and other penalties, without refund of any applicable registration fees or costs. In addition, violations may be reported to the individual’s employer. Offenders may be banned from future activities of the MIDL conference series."""


