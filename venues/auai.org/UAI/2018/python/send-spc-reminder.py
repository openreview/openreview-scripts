import pandas as pd
import os
import openreview

main_dir = os.getenv('HOME')+'/github/openreview-scripts/venues/auai.org/UAI/2018/python/'
baseurl = 'https://openreview.net'

# Populate these variables before running.
username = ''
pw = ''

subject = '[Reminder] UAI 2018: Invitation to serve on the Senior Program Committee'

message = '''
This is a reminder to respond to your UAI 2018 Senior Program Committee invitation by December 20, 2017. 

As program chairs of UAI 2018, it is our pleasure to invite you to serve as a member of the Senior Program Committee (SPC) for the 2018 Uncertainty in AI Conference (UAI). The conference will be held in the San Francisco area in early August 2018.

UAI is the premier international conference on research related to representation, inference, learning and decision making in the presence of uncertainty, as they relate to the fields of artificial intelligence and machine learning. As a Senior Program Committee Member for the UAI 2018 conference you will help us select a high quality program for the conference. We count on your help and your expertise.

Your main responsibilities will be to help to control the quality of the reviewing process and include:
a) Help us form the Program Committee (PC) by suggesting 5 to 10 potential members.
b) Help us with reviewer assignment by suggesting 3 to 5 reviewers (from the PC) for each paper assigned to you, if you happen to know some good candidates. We expect that you will be assigned around 10 papers.
c) Read the reviews for the papers assigned to you and, if necessary, ask the reviewers to improve their quality.
d) Proactively lead the discussions among reviewers.
e) Write an informative meta-review for each paper assigned to you, and make an accept/reject recommendation.


To ACCEPT the invitation, please click on the following link:

{1}

To DECLINE the invitation, please click on the following link:

{2}

The timeline of SPC actions is the following:

1. By December 20, 2017: Please respond by clicking above indicating whether you accept the SPC invitation or not.
2. March 4-9, 2018: Enter bids for submitted papers.
3. March 12-18: Suggest 3 to 5 reviewers for each paper assigned to you.
4. March 19th to April 20th: Review period. If a reviewer drops out, we might need your help in finding additional reviewers for the paper.
5. April 13th to April 20th: Check reviews and chase reviewers for missing ones.
6. April 21st to May 3rd: Discussion period with reviewers, suggest further reviewers if necessary.
7. By May 6th, write a meta-review for each paper.
10. May 7th - May 13th: Your meta-reviews will be used for making the final decisions. If we need additional input on a particular paper we might contact you.

We really hope you will be able to accept our invitation and help us select a high quality program for UAI 2018.  Please reply to this invitation by following the link at the beginning of this message, no later than December 1st, 2017.

Thanks in advance for your help!

Amir Globerson and Ricardo Silva
UAI 2018 Program Chairs
uai2018chairs@gmail.com

'''

client = openreview.Client(baseurl=baseurl, username=username, password=pw)
print 'connecting to {0}'.format(client.baseurl)
spc_d = set(client.get_group('auai.org/UAI/2018/Senior_Program_Committee/Declined').members)
spc_i = set(client.get_group('auai.org/UAI/2018/Senior_Program_Committee/Invited').members)
spc_a = set(client.get_group('auai.org/UAI/2018/Senior_Program_Committee').members)
target_emails = spc_i - (spc_a | spc_d)

def send_mail(email, first):
    # the hashkey is important for uniquely identifying the user,
    # without requiring them to already have an openreview account.
    # The second argument to the client.get_hash() function
    # is just a big random number that the invitation's "process function" also knows about.
    hashkey = client.get_hash(email.encode('utf-8'), "2810398440804348173")

    # build the URL to send in the message
    url = client.baseurl+"/invitation?id=auai.org/UAI/2018/-/SPC_Invitation&email=" + email + "&key=" + hashkey + "&response="

    # format the message defined above
    personalized_message = message.format(first, url + "Yes", url + "No")

    # send the email through openreview
    response = client.send_mail(subject, [email], personalized_message)

    print "Mail response: ", response

for idx, email_add in enumerate(target_emails):
    # check to make sure that the user hasn't already been invited
    print "[{1}/{2}] Sending reminder message to {0}".format(email_add, idx+1, len(target_emails))
    send_mail(email_add, '')
