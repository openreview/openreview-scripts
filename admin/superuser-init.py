#!/usr/bin/python
import sys, os, shutil
import json
import re
import argparse
import getpass
import openreview
import datetime

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

def parse_json(file):
    json_string = open(os.path.join(os.path.dirname(__file__), file), 'r').read()
    json_parsed = re.sub('\/\*[^*]+\*\/|\s|\n', '', json_string)
    return json.loads(json_parsed)

def build_directory(directory_path):

    # create the subdirectories if they don't exist
    for subpath in ['','/python','/webfield','/process','/data']:
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
parser.add_argument('-c', '--conf', required=True, help = "the full path of the conference group to create.")
parser.add_argument('-d', '--data', required=True, help = "a .data file containing parameters.")
parser.add_argument('--overwrite', action='store_true', help="if true, overwrites the conference directory.")
parser.add_argument('--baseurl')
parser.add_argument('--username')
parser.add_argument('--password')
args = parser.parse_args()

client = openreview.Client(baseurl=args.baseurl, username=args.username, password=args.password)
directory_path = os.path.join(os.path.dirname(__file__), '../venues/{0}'.format(args.conf))
conference_group_id = args.conf

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

groups = build_groups(conference_group_id)

print "created the following groups:"
for g in groups: print g

post_groups = raw_input("Post groups? (y/[n]): ").lower()

if post_groups == 'y' or 'yes':
    for g in groups:
        client.post_group(groups[g])
        print groups[g]
    # add admin group to the conference members
    client.add_members_to_group(groups[conference_group_id], conference_group_id + '/Admin')



