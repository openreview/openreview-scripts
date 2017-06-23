#!/usr/bin/python

import openreview
import sys, os
import config

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../../../../utils"))
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

utils.process_to_file(
    utils.get_path("../process/submissionProcess.template", __file__),
    utils.get_path("../process", __file__)
    )

groups = {}
prog_chairs = openreview.Group(config.PROGRAM_CHAIRS, **config.group_params)
prog_chairs.members = ["~Been_Kim1","~Adrian_Weller1"]
groups[config.PROGRAM_CHAIRS] = prog_chairs
groups[config.AREA_CHAIRS] = openreview.Group(config.AREA_CHAIRS, **config.group_params)
groups[config.REVIEWERS] = openreview.Group(config.REVIEWERS, **config.group_params)

invitations = {}
invitations[config.SUBMISSION] = openreview.Invitation(config.SUBMISSION, duedate=config.DUE_TIMESTAMP, **config.submission_params)
#invitations[config.COMMENT] = openreview.Invitation(config.COMMENT, **config.comment_params)

invitations[config.SUBMISSION].reply = templates.SubmissionReply().body

#invitations[config.COMMENT].reply = templates.CommentReply(params={'invitation': config.SUBMISSION}).body

for g in groups.values():
	print "Posting group: ", g.id
	client.post_group(g)

for i in invitations.values():
	print "Posting invitation: ", i.id
	client.post_invitation(i)

# TODO:
# webfield
# process functions

# Optional stuff:
# recruiting pipeline (maybe automate, maybe don't)
# bids
# blind submissions
