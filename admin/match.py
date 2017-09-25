#!/usr/bin/python

"""
Initializes the structures used for paper/user metadata
"""

import argparse
import openreview
import openreview_matcher

# Argument handling
parser = argparse.ArgumentParser()
parser.add_argument('config', help='the ID of the configuration note to use')
parser.add_argument('--username')
parser.add_argument('--password')
parser.add_argument('--baseurl', help="base URL")
args = parser.parse_args()

client = openreview.Client(username=args.username, password=args.password, baseurl=args.baseurl)

# get the already-posted configuration note
configuration_note = client.get_note(args.config)

matcher = openreview_matcher.Matcher(client=client)

# solving the matcher returns a configuration note object with the content.assignments field filled in.
configuration_note = matcher.solve(configuration_note)

# Post a note with the configuration and assignments for later use
configuration_note = client.post_note(configuration_note)
print "posted assignment note {0}".format(configuration_note.forum)
