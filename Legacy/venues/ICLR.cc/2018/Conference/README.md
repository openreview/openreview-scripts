Properties of ICLR 2018:

- Double-blind reviewing: Authors are anonymous until after the reviewing process, when they will be revealed.
- Open comments: anyone can comment on submissions.
- Reviewer bidding: Sign up reviewers may want to bid for papers instead of being assigned. This allows for some interesting opportunities (if no one bids, maybe a paper won't be reviewed / considered).
- Rolling submissions: We may consider a submission window of months, in which papers can be reviewed anytime (i.e., each paper sets its own deadlines / review process).

Description of files and scripts:

- `config.py`: contains constants and configuration parameters, to be used by other scripts.
- `admin-init.py`: Initializes the conference. Runnable by an ICLR administrator or the OpenReview super user.
- `toggle-invitation.py`: can be used to enable or disable most invitations in the conference.
-

Notes for administrators:
- Many of the invitations in `config.py` have an empty `invitees` field. These invitations must be enabled by the `toggle-invitation.py` script.
