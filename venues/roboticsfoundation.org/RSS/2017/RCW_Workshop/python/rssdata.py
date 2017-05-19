import datetime
import time
"""
RSS Conference constants
"""

ADMIN = "rss2017admin"
CONFERENCE = "roboticsfoundation.org/RSS/2017/RCW_Workshop"
COCHAIRS = CONFERENCE+"/Program_Co-Chairs"
# the two tracks within the conference
POSTER = CONFERENCE+"/-_Poster"
PROCEEDINGS = CONFERENCE+"/-_Proceedings"
POSTER_REVIEWERS = POSTER+"/Reviewers"
PROCEEDINGS_REVIEWERS = PROCEEDINGS+"/Reviewers"
# Due date May 21, 2017 at 5:00pm (here)
DATE_DUE = datetime.datetime(2017, 5, 22, 7, 59)
TIMESTAMP_DUE = int(time.mktime(DATE_DUE.timetuple()))*1000
