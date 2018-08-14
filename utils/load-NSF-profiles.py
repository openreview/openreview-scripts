#!/usr/bin/python

###############################################################################
# Load NSF xml files into profiles including name, email and often institution
# NSF data comes from https://www.nsf.gov/awardsearch/download.jsp
#  -d "/Users/mandler/projects/openreview-scripts/data/2017/"
###############################################################################

## Import statements
import argparse
import xml.etree.ElementTree as ET
from openreview import *

## Argument handling
parser = argparse.ArgumentParser()
parser.add_argument('directory', help = "the full path to the XML files")
parser.add_argument('--baseurl', help="base url")
parser.add_argument('--username')
parser.add_argument('--password')

source_entity = 'NSF.gov'
source_id = source_entity+'/Upload'

def  get_all_profiles(client):
    # Pull all of the profile info in at once to # of calls by getting them one at a time
    # To determine ids for all profiles, get all groups w/ tilde_id names as an id.
    profile_groups = list(tools.iterget(client.get_groups, id='~.*'))
    tilde_ids = []
    for group in profile_groups:
        tilde_ids.append(group.id)

    # get all profiles associated with the tilde_ids
    all_profiles = []
    for i in range(0, len(tilde_ids), 100):
        all_profiles.extend(client.get_profiles(tilde_ids[i:i + 100]))

    # store the profiles in easy to access dictionaries
    # stored by id and by email
    profiles_by_id = {}
    profiles_by_email = {}
    for profile in all_profiles:
        profiles_by_id[profile.id] = profile
        for email in profile.content['emails']:
            profiles_by_email[email]= profile

    return profiles_by_id, profiles_by_email


def get_institute(person, root):
    ''' Get the name of the institute if the person is the Principal Investigator'''
    institute = ''
    if person.find('RoleCode').text == 'Principal Investigator':
        institute_fields = root.iter('Institution')
        for institute_field in institute_fields:
            institute = institute_field.find('Name').text
    return institute

def get_expertise(root):
    # get expertise strings from the ProgramElement and ProgramReference fields
    expertise = []

    def find_expertise(field):
        fields = root.iter(field)
        for field in fields:
            expert = field.find('Text').text
            # when it is in all caps it refers to programs, not keywords
            if expert and not expert.isupper():
                expertise.append(expert)

    find_expertise('ProgramElement')
    find_expertise('ProgramReference')

    return expertise

def new_referent(client, id, invitation, content):
    # creates new profile with only the necessary info
    if content:
        profile = openreview.Profile(referent=id,
                             invitation=invitation,
                             signatures=[source_id],
                             writers=[source_id],
                             content=content)
        profile = client.update_profile(profile)
        # test if fails to get original
        db_profile = client.get_profile(id)
        super_group = client.get_group('OpenReview.net')
        if len(super_group.members) > 1:
            print super_group.members
            raise openreview.OpenReviewException
        return profile

    else:
        return None

# creates profile then adds information from NSF
def create_nsf_profile(client, email, first_name, last_name, institute, expertise):
    # create new profile
    profile= tools.create_profile(client, email, first_name, last_name)

    # create referent
    content = {}
    content['emails'] = [email]
    #content['names'] = [{'first': first_name, 'last': last_name}]
    content = update_expertise_and_institute(content, expertise, institute)
    nsf_profile = new_referent(client, profile.id, profile.invitation, content)

    return nsf_profile

def update_expertise_and_institute(profile_content, expertise, institute):
    # add new information if it exists
    if institute:
        profile_content['history'] = [{'institution': {'name': institute}}]
    if expertise:
        profile_content['expertise'] = [{'keywords': expertise}]

    return profile_content

def update_coauthors(content, author_ids, email):
    # Take a list of authors and add all that aren't the current author
    # to the coauthor relations
    if len(author_ids) > 1:
        content['relations'] = []
        for id in author_ids:
            if id[1] != email:
                content['relations'].append({'name':id[0], 'email':id[1],
                                                        'relation':'Coauthor'})
    return content

# load information for one or more investigators from each xml file
def load_xml_investigators(client, dirpath):
    super_group = client.get_group('OpenReview.net')
    print len(super_group.members)
    # create the NSF group (or overwrite it if it exists)
    source_group = openreview.Group(id=source_entity, signatures=['OpenReview.net'],
                                   signatories=[source_entity], readers=[source_entity],
                                   writers=['OpenReview.net'], members=[])
    client.post_group(source_group)
    source_id_group = openreview.Group(id=source_id, signatures=['OpenReview.net'],
                                   signatories=[source_id], readers=[source_id],
                                   writers=['OpenReview.net'], members=[])
    client.post_group(source_id_group)

   # get list of files in directory or list is just one file
    if os.path.isdir(dirpath):
        file_names = os.listdir(dirpath)
    else:
        file_names = [dirpath.split('/')[-1]]
        dirpath = dirpath[:-len(file_names[0])]

    num_new = 0
    num_updates = 0
    total_files = len(file_names)
    file_count = 0
    one_percent = total_files//100.0
    if one_percent < 1:
        one_percent = 1

    # get all profiles
    print "Loading profiles..."
    profiles_by_id, profiles_by_email = get_all_profiles(client)
    print "Retrieved profiles"

    for filename in file_names:
        # print progress
        file_count += 1
        if file_count/one_percent == file_count//one_percent:
            print "{0}% complete".format(file_count*100/total_files)
        # only handle xml files
        if filename.endswith('.xml'):
            f = open(dirpath+'/'+filename, 'r')
            contents = ET.parse(f)
            root = contents.getroot()
            expertise = get_expertise(root)

            # Add all authors and associated emails to the coauthors list
            # this is needed to fill in the coauthor relations later
            coauthor_ids = []
            for person in root.iter('Investigator'):
                email_field = person.find('EmailAddress')
                if email_field is not None:
                    email = email_field.text
                    if email is not None:
                        email = email.strip().lower()
                    first_name = person.find('FirstName').text
                    last_name = person.find('LastName').text
                    coauthor_ids.append((first_name+' '+last_name,email))

            # for each <Investigator>
            for person in root.iter('Investigator'):
                email = None
                email_field = person.find('EmailAddress')
                if email_field is not None:
                    email = email_field.text
                if email is not None:
                    # pull data out of file for this investigator
                    email = email.strip().lower()
                    institute = get_institute(person, root)
                    first_name = person.find('FirstName').text
                    last_name = person.find('LastName').text
                    content = update_expertise_and_institute({}, expertise, institute)
                    content = update_coauthors(content, coauthor_ids, email)
                    # check if profile for this email already exists
                    if email in profiles_by_email.keys():
                        profile = profiles_by_email[email]
                        # if email profile exists, but name is different, create new name
                        found = False
                        # check if name already exists
                        for name in profile.content['names']:
                                if first_name == name['first'] and last_name == name['last']:
                                    found = True
                        if not found:
                            content['names']= [{'first':first_name, 'last':last_name}]

                        # create new profile and set content to only the new changes
                        try:
                            nsf_profile =new_referent(client, profile.id, profile.invitation, content)
                            if nsf_profile:
                                num_updates += 1
                        except openreview.OpenReviewException as e:
                            # can be unhappy if name includes parenthesis etc
                            print "Exception updating profile {}".format(e)
                            continue
                    else:
                        # profile for this email doesn't exist,
                        # add email if name and institute match existing profile
                        try:
                            response = client.get_tildeusername(first_name, last_name)
                        except openreview.OpenReviewException as e:
                            # can be unhappy if name includes parenthesis etc
                            # in this case it is OK to skip it
                            continue
                        tilde_id = response['username'].encode('utf-8')
                        # if tilde_name doesn't end with '1' then it already exists
                        if not tilde_id.endswith(last_name + '1'):
                            tilde_id = tilde_id[:-1] + '1'
                            # use the existing tilde_id to get the profile
                            if tilde_id in profiles_by_id.keys():
                                profile = profiles_by_id[tilde_id]
                                # compare institution domain matches email domain
                                # or the name matches the given name, then add this email to existing profile
                                if 'history' in profile.content.keys():
                                    for hist in profile.content['history']:
                                        if hist['institution']:
                                            email_domain = email.split('@')[1]
                                            if ('domain' in hist['institution'].keys() and email_domain== hist['institution']['domain']) or \
                                                    ('name' in hist['institution'].keys() and institute==hist['institution']['name']):
                                                ## create new empty content so just sending new data
                                                content = {}
                                                content['emails'] = [email]
                                                nsf_profile = new_referent(client, profile.id, profile.invitation, content)
                                                if nsf_profile:
                                                    num_updates += 1
                                                break
                                # if name matches but institution info doesn't,
                                # ignore it because we don't know if it's new or not
                        else:
                            # neither email nor name/institution don't match
                            profile = create_nsf_profile(client, email, first_name, last_name, institute, expertise)
                            profiles_by_id[tilde_id]=profile
                            profiles_by_email[email]=profile
                            num_new += 1


            f.closed

    print "Added {0} profiles.".format(num_new)
    print "Updated {0} profiles.".format(num_updates)

def main():
    args = parser.parse_args()

    ## Initialize the client library with username and password.
    client = Client(baseurl=args.baseurl, username=args.username, password=args.password)

    load_xml_investigators(client, args.directory)





if __name__ == "__main__":
    main()
