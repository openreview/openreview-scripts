#!/usr/bin/env python

###############################################################################
# Script that will update the 'web' field of any group or invitation with the
# given ID. Will completely overwrite the existing value with the contents of
# the specified file.
###############################################################################

## Import statements
from __future__ import print_function
import os
import sys
import argparse
import openreview

def update_webfield(args):
    ## Initialize the client library
    client = openreview.Client(baseurl=args.baseurl, username=args.username, password=args.password)

    ## Retrieve the group or invitation
    is_group = True
    try:
        group = client.get_group(args.id)
    except openreview.OpenReviewException as e:
        is_group = False
        try:
            group = client.get_invitation(args.id)
        except openreview.OpenReviewException as e:
            print("Error: " + args.id + " not found")
            return False

    ## Read file and update the webfield
    if not os.path.exists(args.webfield):
        print("Error: the file " + args.webfield + " does not exist")
        return False

    with open(args.webfield) as f:
        group.web = f.read()

    if is_group:
        updated_group = client.post_group(group)
    else:
        updated_group = client.post_invitation(group)

    print(group.id + " updated")
    return True


if __name__ == "__main__":
    ## Parse the arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("id", help="ID of the group or invitation whose web field will be replaced")
    parser.add_argument("webfield", help="JavaScript file that will replace the contents of the current web field")
    parser.add_argument("--baseurl")
    parser.add_argument("--username")
    parser.add_argument("--password")
    args = parser.parse_args()

    exit_status = update_webfield(args)
    if exit_status is False:
        sys.exit(1)
