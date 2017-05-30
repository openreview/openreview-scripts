#!/usr/bin/python

import openreview
import sys, os
import config
import getpass
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "/Users/mandler/projects/openreview-scripts/utils"))
import utils
import templates


args, parser, overwrite = utils.parse_args()
client = openreview.Client(baseurl=args.baseurl, username=args.username, password=args.password)

"""

OPTIONAL SCRIPT ARGUMENTS

	baseurl -  the URL of the OpenReview server to connect to (live site: https://openreview.net)
 	username - the email address of the logging in user
	password - the user's password

See openreview-scripts/utils for utility function and template details.

"""

if client.username.lower() != "openreview.net": raise(Exception('This script may only be run by the superuser'))

path_components = config.CONF.split('/')
paths = ['/'.join(path_components[0:index+1]) for index, path in enumerate(path_components)]

for p in paths:
	if not client.exists(p) and p != config.CONF:
		client.post_group(openreview.Group(
			p,
			readers = ['everyone'],
			writers = [],
			signatures = [],
			signatories = [],
			members = []
		))
		print "Posting group: ", p

conf_group = client.post_group(openreview.Group(config.CONF, **config.conf_params))
print "Posting group: ", config.CONF

if not client.exists(config.ADMIN):
	admin_group = client.post_group(openreview.Group(
		config.ADMIN,
		readers = [config.ADMIN],
		signatories = [config.ADMIN]
	))
	print "Posting group: ", config.ADMIN
else:
	print "Group %s already exists" % config.ADMIN
	admin_group = client.get_group(config.ADMIN)

client.add_members_to_group(conf_group, [config.ADMIN])

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
	print "Added %s to %s: " % (username, config.CONF)









# TODO:
# webfield
# process functions

# Optional stuff:
# recruiting pipeline (maybe automate, maybe don't)
# bids
# blind submissions
