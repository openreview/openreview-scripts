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
# Due date June 18, 2017 at 7:59am here
DATE_DUE = datetime.datetime(2017, 6, 18, 7, 59)
TIMESTAMP_DUE = int(time.mktime(DATE_DUE.timetuple()))*1000
# June 27, 2017, 11:59:59pm Anywhere on Earth time (UTC -12).
#  == June 28, 2017, 7:59am EST
REVIEW_DUE = datetime.datetime(2017, 6, 28, 7, 59)
REVIEW_DUE = int(time.mktime(REVIEW_DUE.timetuple()))*1000

