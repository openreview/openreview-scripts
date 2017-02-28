import datetime
import time
"""
RSS Conference constants
"""

ADMIN = "rss2017admin"
CONFERENCE = "roboticsfoundation.org/RSS/2017"
COCHAIRS = CONFERENCE+"/Program_Co-Chairs"
REVIEWERS = CONFERENCE+"/Reviewers"
# Due date (guess) June 30, 2017 at 5:15pm
# PAM - how to account for GMT?
DATE_DUE = datetime.datetime(2017, 6, 30, 17, 15)
TIMESTAMP_DUE = int(time.mktime(DATE_DUE.timetuple()))*1000
