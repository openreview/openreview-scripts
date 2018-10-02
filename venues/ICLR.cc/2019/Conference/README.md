# ICLR 2019 Scripts

This file contains notes and tips for administering ICLR 2019.

## Stage transition scripts
1. `post-submissions-stage.py` is run after the submission deadline.
2. `bidding-stage.py` is run a few days later, when we've received TPMS scores (these are needed to sort the bidding interface). It accepts as an argument a TPMS scores file formatted as `papernumber,profile_id,tpms_score`.
3. `review-assignment-stage.py` sets up the metadata needed to suggest paper-reviewer matches and visual the suggested matches through the matching browser. It accepts as an argument a TPMS scores file formatted as `papernumber,profile_id,tpms_score`.
	- [`match.py`](https://github.com/iesl/openreview-matcher/blob/master/samples/match.py), from the `openreview-matcher` repo, generates the suggestions given a configuration JSON. There is [a configuration JSON for the reviewers](https://github.com/iesl/openreview-scripts/blob/master/venues/ICLR.cc/2019/Conference/data/iclr19-match-config-example.json), and [one for the area chairs](https://github.com/iesl/openreview-scripts/blob/master/venues/ICLR.cc/2019/Conference/data/ac-match-config.json).
4. `reviewing-stage.py` reads the assignments as suggested by the matching system (with any modifications made by hand) and creates reviewer and area chair groups for each paper. (This step can be thought of as "confirming" the assignments)
5. `rebuttal-stage.py`: Coming soon.
