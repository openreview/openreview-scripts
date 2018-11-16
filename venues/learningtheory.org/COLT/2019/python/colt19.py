'''
COLT 2019 demo configuration
http://learningtheory.org/colt2019/
June 25 - 28

SUBMISSION DEADLINE Feb. 1, 11pm PST
AUTHOR FEEDBACK Mar. 22-27
AUTHORS NOTIFICATION Apr. 17

'''

import openreview
from openreview import invitations
import os

# group ids
CONFERENCE_ID = 'learningtheory.org/COLT/2019/Conference'
SHORT_PHRASE = 'COLT 2019'

PROGRAM_CHAIRS_ID = CONFERENCE_ID + '/Program_Chairs'

PROGRAM_COMMITTEE_ID = CONFERENCE_ID + '/Program_Committee'

# Deadlines
SUBMISSION_DEADLINE = openreview.tools.timestamp_GMT(year=2019, month=2, day=2, hour=6) # Feb 2, 6am GMT == Feb 1, 11pm PST

# Global group definitions

program_chairs = openreview.Group.from_json({
    'id': PROGRAM_CHAIRS_ID,
    'readers':[CONFERENCE_ID, PROGRAM_CHAIRS_ID],
    'writers': [],
    'signatures': [],
    'signatories': [CONFERENCE_ID, PROGRAM_CHAIRS_ID],
    'members': []
})

program_committee = openreview.Group.from_json({
    'id': PROGRAM_COMMITTEE_ID,
    'readers':['everyone'],
    'writers': [CONFERENCE_ID],
    'signatures': [CONFERENCE_ID],
    'signatories': [CONFERENCE_ID],
    'members': []
})
with open(os.path.abspath('../webfield/programCommitteeWebfield.js')) as f:
    program_committee.web = f.read()
