#!/usr/bin/python
import sys, os, shutil
import json
import argparse
import getpass
import openreview
import utils
import datetime

"""
REQUIRED ARGUMENTS

    conf - the full path of the conference group you would like to create.
        e.g. auai.org/UAI/2017

OPTIONAL ARGUMENTS

    overwrite - if present, overwrites the conference directory.
    baseurl -  the URL of the OpenReview server to connect to (live site:
        https://openreview.net)
    username - the email address of the logging in user
    password - the user's password

"""

parser = argparse.ArgumentParser()
parser.add_argument('-c','--conf', help = "the full path of the conference group to create", required=True)
parser.add_argument('--overwrite', action='store_true', help="if true, overwrites the conference directory")
parser.add_argument('--data', help = "a .json file containing parameters. For each parameter present, the corresponding user prompt will be skipped and replaced with that value.")
parser.add_argument('--baseurl', help="base URL")
parser.add_argument('--username')
parser.add_argument('--password')

args = parser.parse_args()

client = openreview.Client(baseurl=args.baseurl, username=args.username, password=args.password)

data = {'conference': args.conf}
if args.data:
    datafile = open(os.path.join(os.path.dirname(__file__), args.data), 'r')
    data.update(json.loads(datafile.read()))

prompts = {
    'conference': "Enter the full path of the conference group you would like to create (e.g. my-conference.org/MYCONF/2017): ",
    'conference_title': "Enter the title of this conference (this will appear at the top of the homepage): ",
    'conference_subtitle': "Enter the subtitle of this conference (this will appear just below the title): ",
    'conference_location': "Enter the location of the conference: ",
    'conference_date': "Enter date of the conference in human-readable form: ",
    'human_duedate': "Enter the human-readable due date string that will appear on the homepage (this will have no effect on the system due date): ",
    'conference_phrase': "When users submit a paper, they will receive an email. Fill in the blank: \"Your submission to ______ has been received.\" ",
    'submission_name': "Enter the name of the submission invitation: ",
    "duedate_input": "Enter the duedate (DD/MM/YYYY): ",
    "duetime_input": "Enter the time of day that the submission is due in 24-hour format (e.g. enter 23:59 for 11:59 pm): ",
    "url": "Enter the URL of the conference: "
}

def get_input_or_data(name):
    if name not in data.keys():
        data[name] = raw_input(prompts[name])

    return data[name]

conference = get_input_or_data("conference")
directory = utils.get_path('../venues/%s' % conference, __file__)

if args.overwrite or not os.path.exists(directory):
    conference_title = get_input_or_data("conference_title")
    conference_subtitle = get_input_or_data("conference_subtitle")
    conference_location = get_input_or_data("conference_location")
    conference_date = get_input_or_data("conference_date")
    url = get_input_or_data("url")
    conference_phrase = get_input_or_data("conference_phrase")
    submission_name = get_input_or_data("submission_name")

    if submission_name.strip() == '':
        submission_name = "Submission"
        data['submission_name'] = submission_name

    human_duedate = get_input_or_data("human_duedate")
    # check if due date/time is valid and after current time

    duedate_valid = False
    while not duedate_valid and "duedate_input" not in data.keys():
        duedate_input = raw_input(prompts["duedate_input"])
        try:
            day, month, year = duedate_input.split('/')
            day = int(day)
            month = int(month)
            year = int(year)
            # this will catch invalid values for date
            duedate = utils.get_duedate(year, month, day)
            now = datetime.datetime.now()
            assert duedate > now, "Cannot enter a date in the past"

            # get due time
            duetime_input = get_input_or_data("duetime_input")
            hour, minute = duetime_input.split(':')
            hour = int(hour)
            minute = int(minute)
            duedate = utils.get_duedate(year, month, day, hour, minute)
            assert duedate > now, "Cannot enter a time in the past"

            duedate_valid = True
            data["duedate_input"] = duedate_input
        except Exception, e:
            print "Duedate invalid: ", e

    duedate_milliseconds = utils.date_to_timestamp(duedate)


    print "Creating conference directory at %s" % directory

    makedir = lambda d: os.makedirs(d) if not os.path.exists(d) else None

    makedir(directory)
    makedir(directory + '/python')
    makedir(directory + '/webfield')
    makedir(directory + '/process')
    makedir(directory + '/data')

    print "writing %s/python/config.py" % directory
    with open(directory + '/python/config.py', 'w') as new_configfile, open(utils.get_path('./conference-template/python/config.template', __file__)) as template_configfile:
        templatestring = template_configfile.read().replace('<<CONF>>', "\"%s\"" % conference)
        templatestring = templatestring.replace('<<SUBMISSION_NAME>>',submission_name)
        templatestring = templatestring.replace('<<TIMESTAMP>>',str(duedate_milliseconds))
        new_configfile.write(templatestring)

    print "writing %s/webfield/conf.html" % directory
    with open(directory + '/webfield/conf.html', 'w') as new_webfile, open(utils.get_path('./conference-template/webfield/conf.template',__file__)) as template_webfile:
        templatestring = template_webfile.read().replace('<<TITLE>>',"\"%s\"" % conference_title)
        templatestring = templatestring.replace('<<CONF>>',"\"%s\"" % conference)
        templatestring = templatestring.replace('<<SUBMISSION_NAME>>', submission_name)
        templatestring = templatestring.replace('<<SUBTITLE>>',"\"%s\"" % conference_subtitle)
        templatestring = templatestring.replace('<<LOCATION>>',"\"%s\"" % conference_location)
        templatestring = templatestring.replace('<<CONF_DATE>>',"\"%s\"" % conference_date)
        templatestring = templatestring.replace('<<DATE>>',"%s" % human_duedate)
        templatestring = templatestring.replace('<<URL>>',"\"%s\"" % url)
        new_webfile.write(templatestring)

    print "writing %s/python/admin-init.py" % directory
    with open(directory + '/python/admin-init.py', 'w') as new_initfile, open(utils.get_path('./conference-template/python/admin-init.template', __file__)) as template_initfile:
        templatestring = template_initfile.read().replace('<<SUBMISSION_DUEDATE>>', "%s" % duedate_milliseconds)
        new_initfile.write(templatestring)

    print "writing %s/process/submissionProcess.template" % directory
    with open(directory + '/process/submissionProcess.template', 'w') as new_submissionprocess, open(utils.get_path('./conference-template/process/submissionProcess.template', __file__)) as template_submissionprocess:
        templatestring = template_submissionprocess.read().replace('<<CONF>>', "\"%s\"" % conference)
        templatestring = templatestring.replace('<<PHRASE>>', "\"%s\"" % conference_phrase)
        new_submissionprocess.write(templatestring)

    print "writing %s/process/commentProcess.js" % directory
    with open(directory + '/process/commentProcess.js', 'w') as new_commentprocess, open(utils.get_path('./conference-template/process/commentProcess.template', __file__)) as template_commentprocess:
        templatestring = template_commentprocess.read().replace('<<PHRASE>>', "\"%s\"" % conference_phrase)
        new_commentprocess.write(templatestring)

    print "writing %s/params.json" % directory
    with open(directory + '/params.json', 'w') as paramsfile:
        json.dump(data, paramsfile, indent=4)


admin = args.conf + '/Admin'

if client.username.lower() != "openreview.net": raise(Exception('This script may only be run by the superuser'))

path_components = args.conf.split('/')
paths = ['/'.join(path_components[0:index+1]) for index, path in enumerate(path_components)]

# We need to check if ancestors of the conference exist. If they don't, they
# must be created before continuing.
for p in paths:
    if not client.exists(p) and p != args.conf:
        client.post_group(openreview.Group(
            p,
            readers = ['everyone'],
            writers = [],
            signatures = [],
            signatories = [],
            members = []
        ))
        print "Posting group: ", p

if not client.exists(args.conf):
    print "Posting group: ", args.conf
    conf_group = client.post_group(openreview.Group(
        args.conf,
        readers = ['everyone'],
        writers = [args.conf],
        signatories = [args.conf]
    ))
else:
    print "Group %s already exists" % args.conf
    conf_group = client.get_group(args.conf)

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

client.add_members_to_group(conf_group, [admin])

utils.process_to_file(
    os.path.join(os.path.dirname(__file__), "../venues/%s/process/submissionProcess.template" % args.conf),
    os.path.join(os.path.dirname(__file__), "../venues/%s/process" % args.conf)
    )

create_admin = raw_input("Create administrator login? (y/[n]): ").lower()

if create_admin == 'y' or create_admin == 'yes':
    default_username = conference.split('/')[-1].lower()+'_admin'
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

    manual_activation = raw_input("Would you like to activate the user manually? (y/[n]): ")
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


