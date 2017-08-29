#!/usr/bin/python
# -*- coding: utf-8 -*-
"""

"""

## Import statements
import argparse
import csv
import sys
import re
import openreview
import config

## Handle the arguments
parser = argparse.ArgumentParser()
parser.add_argument('file', help="a csv file containing the email addresses of the area chairs")
parser.add_argument('--baseurl', help="base URL")
parser.add_argument('--username')
parser.add_argument('--password')

args = parser.parse_args()

## Initialize the client library with username and password
client = openreview.Client(baseurl=args.baseurl, username=args.username, password=args.password)


message = """

To ACCEPT the invitation, please click on the following link:

{0}

To DECLINE the invitation, please click on the following link:

{1}

"""

def sendMail(user):
    invitation = config.RECRUIT_AREA_CHAIRS

    ## For each candidate area chair, send an email asking them to confirm or reject the request to review
    hashkey = client.get_hash(user.encode('utf-8'), "2810398440804348173")
    url = client.baseurl + "/invitation?id=" + invitation + "&username=" + user + "&key=" + hashkey + "&response="
    response = client.send_mail("Area Chair Invitation for ICLR 2018", [user], message.format(url + "Yes", url + "No"))
    print "Mail response: ", response

if client.exists(config.AREA_CHAIRS_INVITED) and client.exists(config.AREA_CHAIRS_EMAILED):

    area_chairs_invited = client.get_group(config.AREA_CHAIRS_INVITED)
    area_chairs_emailed = client.get_group(config.AREA_CHAIRS_EMAILED)

    with open(args.file, 'rb') as csvfile:
        for row in csv.reader(csvfile):
            # This assumes a csv file with rows formatted as follows:
            # email_address,~tilde_name1
            area_chair = row[1]
            print 'area chair: ', area_chair
            client.add_members_to_group(area_chairs_invited, area_chair)

            if area_chair not in area_chairs_emailed.members:
                sendMail(area_chair)
                client.add_members_to_group(area_chairs_emailed, area_chair)

else:
    print "Error while retrieving area chairs; group may not exist"
    print client.exists(config.AREA_CHAIRS_INVITED)
    print client.exists(config.AREA_CHAIRS_EMAILED)


