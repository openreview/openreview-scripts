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

def get_institute(person, root):
    ''' Get the name of the institute if the person is the Principal Investigator'''
    institute = ''
    if person.find('RoleCode').text == 'Principal Investigator':
        institute_fields = root.iter('Institution')
        for institute_field in institute_fields:
            institute = institute_field.find('Name').text
    return institute

# get expertise strings from the ProgramElement and ProgramReference fields
def get_expertise(root):
    # get expertise keywords
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

# creates profile with a given tilde_id as the creator
def create_nsf_profile(client, tilde_id, email, first_name, last_name, institute, expertise):
    # create new profile with institution name and expertise keywords
    tilde_group = openreview.Group(id=tilde_id, signatories=[tilde_id],
                                   readers=[tilde_id], members=[email])
    email_group = openreview.Group(id=email, signatories=[email],
                                   readers=[email],  members=[tilde_id])
    profile_content = {
        'emails': [email],
        'preferredEmail': email,
        'names': [
            {
                'first': first_name,
                'middle': None,
                'last': last_name,
                'username': tilde_id
            }
        ]
    }
    profile = openreview.Profile(tilde_id, content=profile_content)
    client.post_group(tilde_group)
    client.post_group(email_group)
    profile = client.post_profile(profile)

    profile.content=update_expertise_and_institute(profile.content, expertise, institute)
    profile.signatures = [source_id]
    profile.writers = [source_id]
    client.update_profile(profile)
    return profile

def update_expertise_and_institute(profile_content, expertise, institute):
    # add new information if it exists and isn't already in profile
    if institute:
        profile_content['history'] = [{'institution': {'name': institute}}]
    if expertise:
        profile_content['expertise'] = [{'keywords': expertise}]

    return profile_content

def update_coauthors(content, coauthor_ids, email):
    if len(coauthor_ids) > 1:
        content['relations'] = []
        for id in coauthor_ids:
            if id[1] != email:
                content['relations'].append({'name':id[0], 'email':id[1],
                                                        'relation':'Coauthor'})
    return content

# load information for one or more investigators from each xml file
def load_xml_investigators(client, dirpath):
    source_group = openreview.Group(id=source_entity, signatures=['OpenReview.net'],
                                   signatories=[source_entity], readers=[source_entity],
                                   writers=['OpenReview.net'], members=[])
    client.post_group(source_group)
    source_id_group = openreview.Group(id=source_id, signatures=['OpenReview.net'],
                                   signatories=[source_id], readers=[source_id],
                                   writers=['OpenReview.net'], members=[])
    client.post_group(source_id_group)
    # get list of files in directory
    if os.path.isdir(dirpath):
        file_names = os.listdir(dirpath)
    else:
        file_names = [dirpath.split('/')[-1]]
        dirpath = dirpath[:-len(file_names[0])]
    num_new = 0
    num_updates = 0
    for filename in file_names:
        if filename.endswith('.xml'):
            f = open(dirpath+'/'+filename, 'r')
            contents = ET.parse(f)
            root = contents.getroot()
            expertise = get_expertise(root)
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
                    email_domain = email.split('@')[1]
                    institute = get_institute(person, root)
                    first_name = person.find('FirstName').text
                    last_name = person.find('LastName').text
                    content = update_expertise_and_institute({}, expertise, institute)
                    content = update_coauthors(content, coauthor_ids, email)
                    # print first_name+" "+last_name
                    # check if profile for this email already exists
                    profile = tools.get_profile(client, email)

                    if profile:
                        profile.signatures = [source_id]
                        profile.writers = [source_id]
                        # if email profile exists, but name is different, create new name
                        found = False
                        for name in profile.content['names']:
                            if first_name == name['first'] and last_name == name['last']:
                                found = True
                        if not found:
                            content['names']= [{'first':first_name, 'last':last_name}]


                        profile.content = content
                        client.update_profile(profile)
                        num_updates = num_updates+1
                    else:
                        # profile for this email doesn't exist,
                        # add email if name and institute match existing profile
                        try:
                            response = client.get_tildeusername(first_name, last_name)
                        except openreview.OpenReviewException as e:
                            continue
                        tilde_id = response['username'].encode('utf-8')
                        if not tilde_id.endswith(last_name + '1'):
                            tilde_id = tilde_id[:-1] + '1'
                            profile = tools.get_profile(client,tilde_id)
                            if profile and 'history' in profile.content.keys():
                                for hist in profile.content['history']:
                                    if hist['institution']:
                                        if ('domain' in hist['institution'].keys() and email_domain== hist['institution']['domain']) or \
                                                ('name' in hist['institution'].keys() and institute==hist['institution']['name']):
                                            ## create new empty content so just sending new data
                                            profile.content = content
                                            profile.content['emails']=[email]
                                            profile.signatures = [source_id]
                                            profile.writers = [source_id]
                                            client.update_profile(profile)
                                            num_updates += 1
                                            break
                        else:
                            # email and name/institution don't match
                            profile = create_nsf_profile(client, tilde_id, email, first_name, last_name, institute, expertise)
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
