[Link](#11-hello-world)

# openreview-scripts
This is a public repository containing scripts used to generate conferences, workshops, and other events using [OpenReview.net](https://openreview.net).

Scripts use the [openreview python library](https://github.com/openreview/openreview-py) to interact with the OpenReview API. Code for specific events are organized in the `/venues` directory. Events are further organized by institution domain name, year, workshop name, etc.

## How to host your own event
If you would like to use OpenReview to host your own event, please contact us at info@openreview.net.

Once your conference has been approved, we will provide you with an administrator-level username and password, and will help you get started with your event and provide technical support. For larger events, we can also provide some degree of administrative support.

OpenReview can also be used as an internal paper archive and reviewing system for labs and other organizations.

## ARR Commitments

There are two ways of migrating commitment submissions, (1) posting the ARR submission replies directly to the commitment submissions or (2) posting the original ARR submissions and their contents to the receiving venue and they're accessed via a `migration_link` field added to the commitment submission.

The scripts for both methods are found at `openreview-scripts/venues/aclweb.org/Workshops`

(1) The script: `migrate_from_venue.py`

Run in your terminal:
`python migrate_from_venue.py --baseurl_v1 '' --baseurl_v2 ''  --username '' --password '' --confid '' --post_to_commitment`

baseurl_v1: api 1 url  
baseurl_v2: api 2 url  
confid: the venue ID of the venue you want to migrate the replies to  

(2) The scripts:

Make sure that the venueid of the mirgated submissions are /Migrated_Submission

First, run `create_invitations_workshops_one.py` to create the invitations for the migrating notes.
`python create_invitations_workshops_one.py --baseurl '' --username '' --password '' --confid ''`

baseurl: api 2 url

Second, run `migrate_submissions_workshops_one.py` to migrate the submissions and replies.
`python migrate_submissions_workshops_one.py --baseurl '' --baseurl_v2 '' --username '' --password '' --confid ''`

baseurl: api 1 url  
baseurl_v2: api 2 url  
confid: the venue ID of the venue you want to migrate the notes to



