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

# load information for one or more investigators from each xml file
def load_xml_investigators(client, dirpath):
    # get list of files in directory
    file_names = os.listdir(dirpath)
    num_profiles = 0
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
                    try:
                        create_profile(client, email, person.find('FirstName').text, person.find('LastName').text)
                        num_profiles += 1
                    except openreview.OpenReviewException as e:
                        # throw an error if it is something other than profile already exists
                        if not (type(e[0]) == str and e[0].startswith("There is already a profile")):
                            print "OpenReviewException: {0}".format(e)

            f.closed
    print "Added {0} profiles.".format(num_profiles)


def main():
    args = parser.parse_args()

    ## Initialize the client library with username and password.
    client = Client(baseurl=args.baseurl, username=args.username, password=args.password)

    load_xml_investigators(client, args.directory)





if __name__ == "__main__":
    main()
