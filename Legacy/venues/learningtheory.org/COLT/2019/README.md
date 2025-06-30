# COLT 2019

The shared [COLT workflow document](https://docs.google.com/document/d/1j5H8Jo32nuN_2kKomLOmiPhAhgNZM_UkGeTiokL2ZSQ/edit?ts=5c49581d#) should be considered the "source of truth" for this conference.




## Technical Notes:
Disclaimer: if these notes contradict the COLT workflow document, the document should be considered up-to-date, not this README.

### Conference setup
Use the `init.py` script to setup the conference. At the time of this writing, this step has already been executed on the live site.

### Post-Submission Stage
Use the `post-submission-stage.py` script to do the following:
- post the blind notes
- post the groups needed for reviewing (paper group, reviewers, reviewers invited, reviewers declined)
- post the official review invitation

### Bidding Stage
Use the `bidding-stage.py` script to change the webfields and enable bidding.
COLT's bid webfield is special in that it allows bidders to also add a COI tag if necessary.

COLT's reviewing process is unusual in that it does not have separate reviewer and meta-reviewer pools.
Instead, each Program Committee member is responsible for ensuring that their assigned papers are reviewed, regardless of who ultimately submits the review.

In the bidding stage, only Program Committee Members bid on papers.

### Assignment and beyond
More details on the stages after bidding will be added later.

For now, instructions on how to proceed with the test:

1) assign a program committee member to a paper using `assign-program-committee.py`
2) use the Program Committee console to invite a subreviewer to the assigned paper (ensure that super invitations are enabled!)
3) accept the sub-reviewer's invitation to review, and log in with the subreviewer's account.
4) run `allocate-reviewers-job.py` to actually perform the subreviewer assignment, which does not take place in the process function. (this script has the word `job` at the end because it should be executed as frequently as possible. We need to figure out how to make the user experience smooth here)
5) The subreviewer should now be fully assigned to the paper, and the program committee member should be able to see their status in the Program Committee console.

