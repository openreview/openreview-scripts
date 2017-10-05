#!/usr/bin/python
import sys, os, shutil
import json
import re
import argparse
import getpass
import openreview
import datetime

"""
REQUIRED ARGUMENTS
    conf - the full path of the conference group you would like to create.
        e.g. auai.org/UAI/2017
        A directory with path exactly equal to the conference group ID
        should already exist before running this script.

    data - a file containing parameters of the conference.
        See openreview-scripts/admin/conference-template/params.data

OPTIONAL ARGUMENTS
    overwrite - if present, overwrites the conference directory.
    baseurl -  the URL of the OpenReview server to connect to (live site:
        https://openreview.net)
    username - the email address of the logging in user
    password - the user's password


"""

def build_directory(directory_path):

    # create the subdirectories if they don't exist
    for subpath in ['/python','/webfield','/process','/data']:
        path = '{0}/{1}'.format(directory_path, subpath)
        if not os.path.exists(path):
            print "Creating directory {0}".format(path)
            os.makedirs(path)


def generate_file(template_path, directory_path, data, overwrite = False):

    # generate new files from templates
    ext = '.py' if 'python' in template_path else '.js'
    newfile_path = directory_path + '/' + template_path.replace('.template', ext)

    with open(os.path.join(os.path.dirname(__file__), './conference-template/{0}'.format(template_path))) as template:
        template_string = template.read()

    for replacement in data:
        template_string = template_string.replace(replacement, data[replacement])

    if not os.path.exists(newfile_path) or overwrite:
        with open(newfile_path, 'w') as newfile:
            print "writing {0}".format(newfile_path)
            newfile.write(template_string)


def build_groups(conference_group_id):
    # create list of subpaths (e.g. Test.com, Test.com/TestConference, Test.com/TestConference/2018)
    path_components = conference_group_id.split('/')
    paths = ['/'.join(path_components[0:index+1]) for index, path in enumerate(path_components)]

    # We need to check if ancestor groups of the conference exist.
    # If they don't, they must be created before continuing.
    for p in paths:
        if not client.exists(p) and p != conference_group_id:
            group = client.post_group(openreview.Group(
                p,
                readers = ['everyone'],
                writers = [],
                signatures = [],
                signatories = [],
                members = []
            ))
            print "Posting group: ", p

    # create conference group
    if not client.exists(conference_group_id):
        print "Posting group: ", conference_group_id
        conf_group = client.post_group(openreview.Group(
            conference_group_id,
            readers = ['everyone'],
            writers = [conference_group_id],
            signatories = [conference_group_id]
        ))
    else:
        print "Group %s already exists" % conference_group_id
        conf_group = client.get_group(conference_group_id)

    # create admin group
    admin = conference_group_id + '/Admin'
    if not client.exists(admin):
        admin_group = client.post_group(openreview.Group(
            admin,
            readers = [admin],
            signatories = [admin]
        ))
        print "Posting group: ", admin
    else:
        print "Group %s already exists" % admin
        admin_group = client.get_group(admin)


    # add admin group to the conference members
    client.add_members_to_group(conf_group, [admin])

    # create admin user
    create_admin = raw_input("Create administrator login? (y/[n]): ").lower()
    if create_admin == 'y' or create_admin == 'yes':
        default_username = conference_group_id.split('/')[-1].lower()+'_admin'
        username = raw_input("Please provide administrator login, in lowercase, with no spaces (default: {0}): ".format(default_username))
        if not username.strip(): username = default_username
        firstname = raw_input("Please provide administrator first name: ")
        lastname = raw_input("Please provide administrator last name: ")

        passwords_match = False
        while not passwords_match:
            password = getpass.getpass("Please provide a new administrator password: ")
            passwordconfirm = getpass.getpass("Please confirm the new password: ")

            passwords_match = password == passwordconfirm
            if not passwords_match:
                print "Passwords do not match."

        client.register_user(email = username, password=password,first=firstname,last=lastname)

        manual_activation = raw_input("Would you like to enter the activation token now? (y/[n]): ")
        manual_activation = manual_activation.lower() == 'y'

        if manual_activation:
            valid_token = False
            while not valid_token:
                try:
                    token = raw_input("Please provide the confirmation token: ")
                    activation = client.activate_user(token = token)
                    print "Admin account activated."
                    print "UserID: ", activation['user']['profile']['id']
                    print "Login: ", username
                    valid_token = True
                except:
                    print "Invalid token."
        else:
            print "Admin account not activated. Please respond to the email confirmation sent to %s" % username
        client.add_members_to_group(admin_group, [username])
        print "Added %s to %s" % (username, args.conf)


parser = argparse.ArgumentParser()
parser.add_argument('-c', '--conf', required=True, help = "the full path of the conference group to create")
parser.add_argument('-d', '--data', required=True, help = "a .json file containing parameters. For each parameter present, the corresponding user prompt will be skipped and replaced with that value.")
parser.add_argument('--overwrite', action='store_true', help="if true, overwrites the conference directory")
parser.add_argument('--baseurl')
parser.add_argument('--username')
parser.add_argument('--password')
args = parser.parse_args()

client = openreview.Client(baseurl=args.baseurl, username=args.username, password=args.password)
directory_path = os.path.join(os.path.dirname(__file__), '../venues/{0}'.format(args.conf))
conference_group_id = args.conf

def parse_json(file):
    json_string = open(os.path.join(os.path.dirname(__file__), file), 'r').read()

    json_stripped = re.sub('\/\*[^*]+\*\/|\s', '', json_string.replace('\n',''))
    return json.loads(json_stripped)

# load data
data = parse_json(args.data)

# build the directory structure
build_directory(directory_path)

templates = [
    'python/config.template',
    'python/admin-init.template',
    'webfield/conferenceWebfield.template',
    'webfield/programchairWebfield.template',
    'process/submissionProcess.template',
    'process/commentProcess.template',
    'process/officialReviewProcess.template',
]

# generate new files from templates
for file in templates:
    generate_file(file, directory_path, data, overwrite = args.overwrite)

build_groups(conference_group_id)





