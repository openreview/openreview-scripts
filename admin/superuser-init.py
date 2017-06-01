#!/usr/bin/python
import sys, os
import argparse
import getpass
import openreview
import utils

"""
REQUIRED ARGUMENTS

	conf - the full path of the conference group you would like to create.
		e.g. auai.org/UAI/2017

OPTIONAL ARGUMENTS

	baseurl -  the URL of the OpenReview server to connect to (live site:
		https://openreview.net)
 	username - the email address of the logging in user
	password - the user's password

"""

parser = argparse.ArgumentParser()
parser.add_argument('-c','--conf', help = "the full path of the conference group to create", required=True)
parser.add_argument('--baseurl', help="base URL")
parser.add_argument('--username')
parser.add_argument('--password')

args = parser.parse_args()

client = openreview.Client(baseurl=args.baseurl, username=args.username, password=args.password)

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
	username = raw_input("Please provide administrator login (must be lowercase. if not a valid email address, you must activate the account manually): ")
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
	print "Added %s to %s: " % (username, args.conf)


