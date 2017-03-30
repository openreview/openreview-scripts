import datetime
import time
"""
RSS Conference constants
"""

ADMIN = "rss2017admin"
CONFERENCE = "roboticsfoundation.org/RSS/2017/Workshop"
COCHAIRS = CONFERENCE+"/Program_Co-Chairs"
# the two tracks within the conference
POSTER = CONFERENCE+"/Poster"
PROCEEDINGS = CONFERENCE+"/Proceedings"
POSTER_REVIEWERS = POSTER+"/Reviewers"
PROCEEDINGS_REVIEWERS = PROCEEDINGS+"/Reviewers"
# Due date (guess) June 30, 2017 at 5:00pm (here)
DATE_DUE = datetime.datetime(2017, 6, 30, 17, 0)
TIMESTAMP_DUE = int(time.mktime(DATE_DUE.timetuple()))*1000
