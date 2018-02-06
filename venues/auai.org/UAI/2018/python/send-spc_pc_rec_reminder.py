import pandas as pd
import os
import openreview

main_dir = os.getenv('HOME')+'/github/openreview-scripts/venues/auai.org/UAI/2018/python/'
baseurl = 'https://openreview.net'

# Populate these variables before running.
username = ''
pw = ''
gdoc_link = ''
subject = '[UAI 2018 - SPC] Reminder: Request for Recommended Reviewers'

message = '''
Dear Senior Program Chair,

This is a friendly reminder to provide us with the names of reviewers that you would like to work with for UAI 2018. We thank those who have already provided us with the names.

In order to ensure the quality of the review process we would like to ask you to suggest names of reviewers that you have high confidence in, and would like to see as reviewers for papers in your pool. Ideally, a reviewer should be an advanced graduate student, with at least two publications in a key ML venue.

We have already constructed an initial list in the following Google spreadsheet. Please add your recommendations as new rows therein. We would like each SPC member to provide at least five recommendations if possible.
Link to the editable reviewer list: {0}

If you have any question, please send us an e-mail at uai2018chairs@gmail.com.

Best,
Ricardo and Amir
UAI 2018 Program Chairs
uai2018chairs@gmail.com

'''

client = openreview.Client(baseurl=baseurl, username=username, password=pw)
print 'connecting to {0}'.format(client.baseurl)
spc_d = set(client.get_group('auai.org/UAI/2018/Senior_Program_Committee/Declined').members)
spc_i = set(client.get_group('auai.org/UAI/2018/Senior_Program_Committee/Invited').members)
spc_a = set(client.get_group('auai.org/UAI/2018/Senior_Program_Committee').members)
target_emails = spc_a
for idx, email_add in enumerate(target_emails):
    # check to make sure that the user hasn't already been invited
    print "[{1}/{2}] Sending reminder message to {0}".format(email_add, idx+1, len(target_emails))
    response = client.send_mail(subject, [email_add], message.format(gdoc_link))
    print " - Mail response: ", response
