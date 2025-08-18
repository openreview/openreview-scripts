# ICML 2019 Paper Matching

## Requested services:
- Match Senior ACs to ACs
- Match ACs to Papers

## Data Management
- All data is provided to us through a [shared Google Sheet](https://docs.google.com/spreadsheets/d/1G3AFQyO7-dwNrIJOCc-GYL4QPwhT-QzKYIoY-Y-SMjI/edit#gid=1928338508)
- Download each sheet and place them in a directory called `ICML.cc/2019/Conference/data/icml-sheets`. Give them the following names: `areachairs.csv`, `reviewer_quotas.csv`, `reviewers.csv`, `sac_ac_bids.csv`, and `sr_areachairs.csv`.
- Run `parse_sheets.py` to process them into a format that is recognized by our scripts.

## Matching Setup
- Run `init.py`. This builds the groups and invitations needed to do the match. This script can be run multiple times without negative consequences.

### Matching Sr. ACs and ACs
- Run `sac_ac_match.py` to set up the system for matching Sr. ACs to Jr. ACs.
- The script will post a Note that represents each Jr. AC, and then use the matching system as normal on the Sr. ACs and the Jr. AC "placeholder" papers.
- Export the results by running `export_sac_match.py`
