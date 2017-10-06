#!/usr/bin/python
import sys, os, shutil
import json
import re
import argparse
import getpass
import openreview
import datetime
import ConfigParser

"""
This script should be used by OpenReview administrators to automatically build
the basic infrastructure for a new conference. It will create (or fill in as
needed) a directory under openreview-scripts/venues with the necessary
subdirectories, and will generate the scripts, webfields, and process functions
needed to run a simple conference.

REQUIRED KEYWORD ARGUMENTS
    conf - the full path of the conference group you would like to create.
        e.g. auai.org/UAI/2017
        A directory with path exactly equal to the conference group ID
        should already exist before running this script.

    data - a file containing parameters of the conference.
        See openreview-scripts/admin/conference-template/params.data

OPTIONAL KEYWORD ARGUMENTS
    overwrite - if present, overwrites the conference directory.
    baseurl -  the URL of the OpenReview server to connect to (live site:
        https://openreview.net)
    username - the email address of the logging in user
    password - the user's password


"""

def parse_properties(file):
    config = ConfigParser.RawConfigParser()
    config.read(file)
    return {key.upper(): value for key, value in config.items('config')}

def build_directories(paths, directory_path):

    # create main directory if it doesn't exist
    if not os.path.exists(directory_path):
        print "Creating directory {0}".format(directory_path)
        os.makedirs(directory_path)

    # create the subdirectories if they don't exist
    for subpath in paths:
        path = '{0}/{1}'.format(directory_path, subpath)
        if not os.path.exists(path):
            print "Creating directory {0}".format(path)
            os.makedirs(path)


def generate_file(template_path, directory_path, data, overwrite = False):

    # generate new files from templates
    ext = '.py' if 'python' in template_path else '.js'
    newfile_path = directory_path + '/' + template_path.replace('.template', ext)

    if not os.path.exists(newfile_path) or overwrite:
        with open(os.path.join(os.path.dirname(__file__), './conference-template/{0}'.format(template_path))) as template:
            template_string = template.read()

        for replacement in data:
            template_string = template_string.replace('<<{0}>>'.format(replacement), data[replacement])

        with open(newfile_path, 'w') as newfile:
            print "writing {0}".format(newfile_path)
            newfile.write(template_string)


def build_groups(conference_group_id):
    # create list of subpaths (e.g. Test.com, Test.com/TestConference, Test.com/TestConference/2018)
    path_components = conference_group_id.split('/')
    paths = ['/'.join(path_components[0:index+1]) for index, path in enumerate(path_components)]

    empty_params = {
        'readers': ['everyone'],
        'writers': [],
        'signatures': [],
        'signatories': [],
        'members': []
    }

    groups = {p: openreview.Group(p, **empty_params) for p in paths}
    groups[conference_group_id].writers = groups[conference_group_id].signatories = [conference_group_id]

    admin_id = conference_group_id + '/Admin'
    groups[admin_id] = openreview.Group(admin_id, readers=[admin_id], signatories=[admin_id])

    return groups


parser = argparse.ArgumentParser()
parser.add_argument('-v', '--venue', required=True, help = "the full path of the conference group to create.")
parser.add_argument('-d', '--data', help = "a .properties file containing parameters.")
parser.add_argument('--overwrite', action='store_true', help="if true, overwrites the conference directory.")
parser.add_argument('--baseurl')
parser.add_argument('--username')
parser.add_argument('--password')
args = parser.parse_args()

client = openreview.Client(baseurl=args.baseurl, username=args.username, password=args.password)
directory_path = os.path.join(os.path.dirname(__file__), '../venues/{0}'.format(args.venue))
conference_group_id = args.venue

# load data
data = parse_properties(args.data if args.data else directory_path + '/config.properties')


subdirectories = [
    '/python',
    '/webfield',
    '/process',
    '/data'
]

# build the directory structure
build_directories(subdirectories, directory_path)

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

groups = build_groups(conference_group_id)

for g in sorted([g for g in groups]):
    print "posting group {0}".format(g)
    client.post_group(groups[g])
# add admin group to the conference members
client.add_members_to_group(groups[conference_group_id], conference_group_id + '/Admin')



