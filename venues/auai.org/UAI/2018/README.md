Before doing anything else, first ensure that the group auai.org/UAI/2018 already exists. It must be created by the OpenReview Super User.

To set up the submission infrastructure: run /python/setup-submission.py

To set up reviewer recruitment, run:
- /python/setup-pc-recruitment.py
- then, see /python/invite-pc.py for an example of how to send a recruitment message. (there may be several recruitment scripts in the repo).


Matching system for UAI:

Before performing any match: make sure that all members of the "matching_group" are tilde IDs. This is important for the user interface to work properly.

To set up the matching invitations/infrastructure:
- run /python/setup-matching.py
- run /python/setup-metadata.py

To match reviewers and create assignments, run:
- run /python/match-reviewers.py

