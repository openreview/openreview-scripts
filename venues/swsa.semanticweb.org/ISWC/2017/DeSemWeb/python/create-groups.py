import sys, os
import argparse
import openreview
import config

## Argument handling
parser = argparse.ArgumentParser()
parser.add_argument('--baseurl', help="base url")
parser.add_argument('--username')
parser.add_argument('--password')
parser.add_argument('--overwrite',action='store_true')

args = parser.parse_args()

client = openreview.Client(baseurl=args.baseurl, username=args.username, password=args.password)

submissions = client.get_notes(invitation=config.SUBMISSION)

for n in submissions:
    #create a group for the paper
    papergroup = openreview.Group(config.CONF+'/Paper{0}'.format(n.number), **config.group_params)
    client.post_group(papergroup)

    #create a group for the authors
    authorgroup = openreview.Group(config.CONF + '/Paper{0}/Authors'.format(n.number), **config.group_params)
    authorgroup.members = n.content['authorids']
    authorgroup = client.post_group(authorgroup)

    #create a reviewers group
    reviewergroup = openreview.Group(papergroup.id+'/Reviewers', **config.group_params)
    reviewergroup.members += [config.ADMIN, config.PROGRAM_CHAIRS]
    client.post_group(reviewergroup)

    #create an anonymous reviewers group
    anonreviewergroup = openreview.Group(papergroup.id + '/AnonReviewer', **config.group_params)
    anonreviewergroup.readers += [anonreviewergroup.id]
    anonreviewergroup.signatories += [anonreviewergroup.id]
    anonreviewergroup.members += [config.ADMIN]
    anonreviewergroup.nonreaders = [authorgroup.id]
    client.post_group(anonreviewergroup)

    print "Submission %s" % n.number
