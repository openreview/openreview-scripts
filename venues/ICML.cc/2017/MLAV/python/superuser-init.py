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

# create groups for each directory level:  Conf.org, Conf.org/2017, Conf.org/2017/Workshop
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

# CONF group needs a webpath - different configuation parameters
if not client.exists(config.CONF):
	conf_group = client.post_group(openreview.Group(config.CONF, **config.conf_params))
	print "Posting group: ", config.CONF
else:
	print "Group %s already exists" % config.CONF
	conf_group = client.get_group(config.CONF)

## PAM check REVIEWERS correct?
if not client.exists(config.REVIEWERS):
	reviewers = openreview.Group(config.REVIEWERS,
								 readers=['everyone'],
								 writers=[config.CONF],
								 signatures=[config.CONF],
								 signatories=[config.REVIEWERS],
								 members=[])  # more to be added later, from the list of Program_Committee members
	conf_group = client.post_group(reviewers)
	print "Posting group: ", config.REVIEWERS
else:
	print "Group %s already exists" % config.REVIEWERS
	conf_group = client.get_group(config.REVIEWERS)

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


##  Optionally create admin user, register user
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
				## PAM what is the confirmation token???
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


## Submission invitation
reply = {
	'forum': None,
	'replyto': None,
	'readers': {
		'description': 'The users who will be allowed to read the above content.',
		'values': ['everyone']
	},
	'signatures': {
		'description': 'How your identity will be displayed with the above content.',
		'values-regex': '~.*'
	},
	'writers': {
		'description': 'How your identity will be displayed with the above content.',
		'values-copied': ['{content.authorids}', '{signatures}']
	},
	'content': {
		'title': {
			'description': 'Title of paper.',
			'order': 1,
			'value-regex': '.{1,250}',
			'required': True
		},
		# [^;,\\n] means all chars except ';' ',' and '\n'
		'authors': {
			'description': 'Comma separated list of author names, as they appear in the paper.',
			'order': 2,
			'values-regex': "[^;,\\n]+(,[^,\\n]+)*",
			'required': True
		},
		'authorids': {
			'description': 'Comma separated list of author email addresses, in the same order as above.',
			'order': 3,
			# a list of email addresses
			'values-regex': "([a-z0-9_\-\.]{2,}@[a-z0-9_\-\.]{2,}\.[a-z]{2,},){0,}([a-z0-9_\-\.]{2,}@[a-z0-9_\-\.]{2,}\.[a-z]{2,})",
			'required': True
		},
		'abstract': {
			'description': 'Abstract of paper.',
			'order': 4,
			# is this up to 5,000 words, because \\S is not white space followed by \\s which is white space
			'value-regex': '[\\S\\s]{1,5000}',
			'required': True
		},
		'pdf': {
			'description': 'Upload a PDF file that ends with .pdf)',
			'order': 8,
			'value-regex': 'upload',
			# 'value-regex': 'upload|http://arxiv.org/pdf/.+',
			# 'description': 'Either upload a PDF file or provide a direct link to your PDF on ArXiv (direct links must begin with http(s) and end with .pdf)'
			'required': True
		},
		'conflicts': {
			'description': 'Comma separated list of email domains of people who would have a conflict of interest in reviewing this paper, (e.g., cs.umass.edu;google.com, etc.).',
			'order': 9,
			'values-regex': "[^;,\\n]+(,[^,\\n]+)*",
			'required': True
		},
	}
}
submit_invitation = openreview.Invitation(config.CONF + '/-/Submission',
											  readers=['everyone'],
											  writers=[config.CONF],
											  invitees=['~'],
											  signatures=[config.CONF],
											  duedate=config.DUE_TIMESTAMP,
											  #process=utils.get_path('../process/submissionProcess.js',__file__)
										  )
submit_invitation.reply = reply.copy()

client.post_invitation(submit_invitation)





# TODO:
# webfield
# process functions

# Optional stuff:
# recruiting pipeline (maybe automate, maybe don't)
# bids
# blind submissions
