#!/usr/bin/python

###############################################################################
# Load NSF xml files into profiles including name, email and often institution
# NSF data comes from https://www.nsf.gov/awardsearch/download.jsp
#  -d "/Users/mandler/projects/openreview-scripts/data/2017/"
###############################################################################

## Import statements
import argparse
import os
import xml.etree.ElementTree as ET
from openreview import *

## Argument handling
parser = argparse.ArgumentParser()
parser.add_argument('-d','--directory', required=True, help = "the full path to the XML files")
parser.add_argument('--baseurl', help="base url")
parser.add_argument('--username')
parser.add_argument('--password')

# catch "not found" errors
def get_profile(client, value):
    profile = None
    try:
        profile = client.get_profile(value)
    except openreview.OpenReviewException as e:
        # throw an error if it is something other than "not found"
        if e[0][0] != 'Profile not found':
            print "OpenReviewException: {0}".format(e)
            raise e
    return profile


def create_profile(client, email, first, last, tilde_id, verbose=False):
    tilde_group = openreview.Group(tilde_id,
                                   signatures=["OpenReview.net"],
                                   signatories=[tilde_id],
                                   readers=[tilde_id],
                                   writers=[tilde_id],
                                   nonreaders=[],
                                   members=[email])
    if verbose: print "Generating new tilde group %s" % tilde_id

    try:
        client.post_group(tilde_group)
    except openreview.OpenReviewException as e:
        print "Failed to post {0} group: {1}".format(tilde_id, e)
        return

    email_group = openreview.Group(email,
                                   signatures=["OpenReview.net"],
                                   signatories=[email],
                                   readers=[email],
                                   writers=[email],
                                   nonreaders=[],
                                   members=[tilde_id])
    client.post_group(email_group)

    profile = openreview.Note.from_json({
        'id': tilde_id,
        'content': {
            'emails': [email],
            'preferred_email': email,
            'names': [{
                'first': first,
                'middle': '',
                'last': last,
                'username': tilde_id
            }]
        }
    })

    response = requests.put(client.baseurl + "/user/profile", json=profile.to_json(), headers=client.headers)

# load information for one or more investigators from each xml file
def load_xml_investigators(dirpath):
    # get list of files in directory
    file_names = os.listdir(dirpath)
    investigators = {}
    for filename in file_names:
        if filename.endswith('.xml'):
            f = open(dirpath+filename, 'r')
            contents = ET.parse(f)
            root = contents.getroot()
            # for each <Investigator>
            for person in root.iter('Investigator'):
                email = person.find('EmailAddress').text
                if email != None:
                    email = email.strip()
                    email = email.lower()
                    if email not in investigators:
                        # new investigator includes first, last name
                        investigators[email]={}
                        investigators[email]['first'] = person.find('FirstName').text
                        investigators[email]['last'] = person.find('LastName').text
                        investigators[email]['institute'] = ''
                    if person.find('RoleCode').text == 'Principal Investigator':
                        # we can only be sure the Institution is correct for PIs
                        for institute in root.iter('Institution'):
                            investigators[email]['institute'] = institute.find('Name').text
            f.closed
    return investigators

# for each new name/email, create a new profile
def upload_profiles(client, investigators):
    for email in investigators:
        # try to find profile w/ email
        profile = get_profile(client, email)
        # if this email already has a profile, no need to do anything
        # if not, if find profile w/~name
        if profile == None:
            tilde_id = "~{0}_{1}1".format(investigators[email]['first'], investigators[email]['last'])
            tilde_id = tilde_id.replace(' ', '_')
            profile = get_profile(client, tilde_id)
            if profile == None:
                # create new profile
                x = 1
                #create_profile(client, email, investigators[email]['first'], investigators[email]['last'], tilde_id)
            elif investigators[email]['institute'] != '':
                for line in profile.content['history']:
                    if 'institution' in line:
                        place = line['institution']
                        if 'name' in place:
                            if place['name'] == investigators[email]['institute']:
                                # add email to profile
                                profile.content['emails'].append(email)
                                print profile.content['emails']
                                print email
                                # PAM - remove elif down, or figure out how to update actual profile.
                                client.post_note(profile)




def main():
    args = parser.parse_args()

    ## Initialize the client library with username and password.
    client = Client(baseurl=args.baseurl, username=args.username, password=args.password)

    investigators = load_xml_investigators(args.directory)
    upload_profiles(client, investigators)



if __name__ == "__main__":
    main()
