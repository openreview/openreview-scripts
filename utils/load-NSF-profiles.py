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

def get_expertise(root):
    # get expertise keywords
    expertise = []

    def find_expertise(field):
        fields = root.iter(field)
        for field in fields:
            expert = field.find('Text').text
            # when it is in all caps it refers to programs, not keywords
            if not expert.isupper():
                expertise.append(expert)

    find_expertise('ProgramElement')
    find_expertise('ProgramReference')
    return expertise

def create_nsf_profile(client, tilde_id, email, first_name, last_name, institute, expertise):
    # create new profile with institution name and expertise keywords
    tilde_group = openreview.Group(id=tilde_id, signatures=[source_id],
                                   signatories=[tilde_id], readers=[tilde_id],
                                   writers=[source_id], members=[email])
    email_group = openreview.Group(id=email, signatures=[source_id], signatories=[email],
                                   readers=[email], writers=[source_id], members=[tilde_id])
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
    profile_content=update_expertise_and_institute(profile_content, expertise, institute)
    profile = openreview.Profile(tilde_id, content = profile_content, signatures=[source_id], writers=[source_id])
    client.post_group(tilde_group)
    client.post_group(email_group)
    profile = client.post_profile(profile)
    return profile

def update_expertise_and_institute(profile_content, expertise, institute):
    # add new information if it exists and isn't already in profile
    if institute:
        profile_content['history'] = [{'institution': {'name': institute}}]
    if expertise:
        profile_content['expertise'] = [{'keywords': expertise}]

    return profile_content

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
    coauthor_ids = {}
    for filename in file_names:
        if filename.endswith('.xml'):
            f = open(dirpath+filename, 'r')
            contents = ET.parse(f)
            root = contents.getroot()
            expertise = get_expertise(root)
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
                    #print first_name+" "+last_name
                    # check if profile for this email already exists
                    profile = tools.get_profile(client, email)
                    content = {}
                    if profile:
                        # if email profile exists, but name is different, create new name
                        found = False
                        for name in profile.content['names']:
                            if first_name == name['first'] and last_name == name['last']:
                                found = True
                        if not found:
                            content['names']= [{'first':first_name, 'last':last_name}]

                        profile.content = update_expertise_and_institute(content, expertise, institute)
                        client.update_profile(profile)
                        num_updates = num_updates+1
                        coauthor_ids[profile.id] = (first_name+' '+last_name,email)
                    else:
                        # profile for this email doesn't exist,
                        # add email if name and institute match existing profile
                        response = client.get_tildeusername(first_name, last_name)
                        tilde_id = response['username'].encode('utf-8')
                        if not tilde_id.endswith(last_name + '1'):
                            tilde_id = tilde_id[:-1] + '1'
                            profile = tools.get_profile(client,tilde_id)
                            if profile and profile.content['history']:
                                for hist in profile.content['history']:
                                    if hist['institution'] is not None:
                                        if ('domain' in hist['institution'].keys() and email_domain== hist['institution']['domain']) or ('name' in hist['institution'].keys() and institute==hist['institution']['name']):
                                            ## create new empty content so just sending new data
                                            profile.content = {}
                                            profile.content['emails']=[email]
                                            profile.content = update_expertise_and_institute(profile.content, expertise, institute)
                                            profile.signatures = [source_id]
                                            profile.writers = [source_id]
                                            client.update_profile(profile)
                                            num_updates = num_updates+1
                                            coauthor_ids[profile.id] = (first_name + ' ' + last_name, email)
                                            break
                        else:
                            # email and name/institution don't match
                            profile = create_nsf_profile(client, tilde_id, email, first_name, last_name, institute, expertise)
                            num_new = num_new + 1
                            coauthor_ids[profile.id] = (first_name + ' ' + last_name, email)


            f.closed

    # if there are multiple authors, set coauthors field for each author
    if len(coauthor_ids) > 1:
        for author_id in coauthor_ids.keys():
            profile = tools.get_profile(client,author_id)
            profile.content = {}
            profile.content['relations'] =[]
            for id in coauthor_ids.keys():
                if id != author_id:
                    profile.content['relations'].append({'name':coauthor_ids[id][0], 'email':coauthor_ids[id][1],
                                            'relation':'Coauthor'})
            client.update_profile(profile)

    print "Added {0} profiles.".format(num_new)
    print "Updated {0} profiles.".format(num_updates)

def main():
    args = parser.parse_args()

    ## Initialize the client library with username and password.
    client = Client(baseurl=args.baseurl, username=args.username, password=args.password)

    load_xml_investigators(client, args.directory)





if __name__ == "__main__":
    main()
