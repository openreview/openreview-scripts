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


