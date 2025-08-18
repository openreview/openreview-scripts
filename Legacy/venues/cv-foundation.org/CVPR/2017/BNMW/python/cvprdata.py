"""
CVPR 2017 BNMW Conference constants
"""
import datetime
import time

ADMIN = "cvpr2017admin"
CONFERENCE = 'cv-foundation.org/CVPR/2017/BNMW'
COCHAIRS = CONFERENCE+"/Program_Co-Chairs"
REVIEWERS = CONFERENCE+"/Reviewers"
# Due date April 7, 2017 at 5:15pm (here)
EIGHT_PG_DATE_DUE = datetime.datetime(2017, 4, 7, 17, 15)
EIGHT_PG_TIMESTAMP_DUE = int(time.mktime(EIGHT_PG_DATE_DUE.timetuple()))*1000
# Due date May 15, 2017 at 5:15pm (here)
FOUR_PG_DATE_DUE = datetime.datetime(2017, 5, 15, 17, 15)
FOUR_TIMESTAMP_DUE = int(time.mktime(FOUR_PG_DATE_DUE.timetuple()))*1000
