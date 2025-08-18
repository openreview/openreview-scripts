import pandas as pd
import os
import openreview

main_dir = os.getenv('HOME')+'/github/openreview-scripts/venues/auai.org/UAI/2018/python/'
baseurl = 'https://openreview.net'

# Populate these variables before running
csv_file = main_dir + '.csv'
username = ''
pw = ''

subject = 'UAI 2018: Invitation to serve on the Program Committee'

message = '''Dear {0},

As program co-chairs of UAI 2018, it is our pleasure to invite you to serve as a member of the Program Committee (PC) for the 2018 Uncertainty in AI Conference (UAI). The conference will be held in the bay area, CA, USA, during the first two weeks of August (exact date and location to be finalized soon). 

UAI is the premier international conference on research related to representation, inference, learning and decision making in the presence of uncertainty as they relate to the field of artificial intelligence. The Program Committee has a major responsibility in the selecting a high quality program for the conference: we count on your help and your expertise. The success of the conference depends a great deal on having experts such as you providing constructive reviews for submitted papers. 

We expect you will have about 5 papers to review, which hopefully is not too heavy a load (see a detailed timeline below). We would be delighted if you can accept this invitation, and help us turning UAI 2018 into a great event. 

Please let us know by December 20th whether you will be able to join the program committee.

To ACCEPT the invitation, please click on the following link:

{1}

To DECLINE the invitation, please click on the following link:

{2}

The timeline of PC actions is the following:
1. By December 20th, 2018: Please respond by clicking above indicating whether you accept the PC invitation or not. 
2. March 4-9, 2018: Enter bids for submitted papers.
3. March 19th to April 19th: Review period. 
4. April 21st to May 3rd: Discussion period, and editing the reviews accordingly.
7. May 13th:  Final decisions sent to authors.

We really hope you will be able to accept our invitation and help us select a high quality program for UAI 2018!

Thanks in advance for your help. If you have any questions please contact us at uai2018chairs@gmail.com.

Best regards, 

Ricardo Silva and Amir Globerson
UAI 2018 Program Chairs
uai2018chairs@gmail.com


'''

client = openreview.Client(baseurl=baseurl, username=username, password=pw)
print 'connecting to {0}'.format(client.baseurl)

invitees_df = pd.read_csv(csv_file)

# MODIFIED_BY_YCN: in url, 'SPC_Invitation' -> 'PC_Invitation'
def send_mail(email, first):
    # the hashkey is important for uniquely identifying the user,
    # without requiring them to already have an openreview account.
    # The second argument to the client.get_hash() function
    # is just a big random number that the invitation's "process function" also knows about.
    hashkey = client.get_hash(email.encode('utf-8'), "2810398440804348173")

    # build the URL to send in the message
    url = client.baseurl+"/invitation?id=auai.org/UAI/2018/-/PC_Invitation&email=" + email + "&key=" + hashkey + "&response="

    # format the message defined above
    personalized_message = message.format(first, url + "Yes", url + "No")

    # send the email through openreview
    response = client.send_mail(subject, [email], personalized_message)

    print "Mail response: ", response

pc_invited = client.get_group('auai.org/UAI/2018/Program_Committee/Invited')

for idx, entry in invitees_df.iterrows():
    email_add = entry.Email
    first_name = entry.FirstName
    # check to make sure that the user hasn't already been invited
    send_mail_valid = True
    if email_add in pc_invited.members:
        user_input = raw_input("{0} has already been invited. Would you like to send the message anyway? y/[n]: ".format(email_add))
        if user_input.lower() != 'y':
            send_mail_valid = False
    else:
        print 'Add {0} to invited list.'.format(email_add)
        pc_invited = client.add_members_to_group(pc_invited, email_add)

    # if everything checks out, send the message
    if send_mail_valid:
        print "[{2}/{3}] sending message to {0} at {1}".format(first_name, email_add, idx+1, len(invitees_df))
        send_mail(email_add, first_name)
    else:
        print "no message was sent."
