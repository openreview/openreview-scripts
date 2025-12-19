# ARR Matching Utilities (`arr/matching`)
## ARR SAC/AC Matching (`arr/matching/sac_core.py`)

This package contains the **SAC/AC matching workflow** used for the ARR cycles. The main entrypoint is `arr.matching.sac_core.SACACMatching`

---

### Writing a Script/Notebook to Run the SAC and AC Matchings
In the *root* of this repository, `openreview-scripts`, create your file and start by creating some useful objects - the API1 client, the API2 client, and an ARR object:

```python
import openreview
req_form_id = '' # <-- Venue Request Form ID
client = openreview.api.OpenReviewClient(
    baseurl='https://devapi2.openreview.net',
    username=<your dev username>,
    password=<your dev password>
)
client_v1 = openreview.Client(
    baseurl='https://devapi.openreview.net',
    username=<your dev username>,
    password=<your dev password>
)
venue = openreview.helpers.get_conference(client_v1, req_form_id)
```
For production/live, you can use the baseurls: `https://api.openreview.net` and `https://api2.openreview.net`

You can create an `SACACMatching` instance with:
```python
from arr.matching.sac_core import SACACMatching
matching = SACACMatching(
    client_v1, client, req_form_id,
    matcher_baseurl='https://devapi2.openreview.net'
)
```

And you can run the full SAC-AC matching pipeline with:
```python
matching.run_matching(
    ac_title='ac-matching',
    sac_title='sac-matching'
)
```

### Running the ARR-specific Matching Setup
Below is an example that runs the ARR matching scripts, which computes and uploads research area edges. These scripts get run in the OpenReview backend via a dateprocess function:
```python
matching_invitations = ['Setup_SAE_Matching', 'Setup_AE_Matching']
for matching_invitation in matching_invitations:
    client.post_invitation_edit(
        invitations=venue.get_meta_invitation_id(),
        readers=[venue.id],
        writers=[venue.id],
        signatures=[venue.id],
        invitation=openreview.api.Invitation(
            id = f"{venue.id}/-/{matching_invitation}",
            content = {
                'count': {'value': 1}
            }
        )
    )
```

### Resetting the Assignment Data
Sometimes, you need to reset the assignment data. You can use the following to reset all matching for all roles:
```python
import time
sac_configuration_notes = client.get_all_notes(
    invitation=f"{venue.get_senior_area_chairs_id()}/-/Assignment_Configuration",
)
ac_configuration_notes = client.get_all_notes(
    invitation=f"{venue.get_area_chairs_id()}/-/Assignment_Configuration",
)
for note in ac_configuration_notes + sac_configuration_notes:
    role = note.invitations[0].split('/-/')[0]
    title = note.content['title']['value']
    prop_asm_count = client.get_edges_count(
        invitation=f"{role}/-/Proposed_Assignment",
        label=title
    )
    agg_score_count = client.get_edges_count(
        invitation=f"{role}/-/Aggregate_Score",
        label=title
    )
    print(f"{role} {title} ({prop_asm_count} proposed assignments, {agg_score_count} aggregate scores)")

    if prop_asm_count > 0:
        client.delete_edges(
            invitation=f"{role}/-/Proposed_Assignment",
            label=title,
            wait_to_finish=True
        )
    if agg_score_count > 0:
        client.delete_edges(
            invitation=f"{role}/-/Aggregate_Score",
            label=title,
            wait_to_finish=True
        )
    
    if note.ddate is None:
        client.post_note_edit(
            invitation=venue.get_meta_invitation_id(),
            readers=[venue.id],
            writers=[venue.id],
            signatures=[venue.id],
            note=openreview.api.Note(
                id=note.id,
                ddate=int(time.time() * 1000)
            )
        )
```
You can also just pass a single note to the code inside the for-loop to only remove a single run. You can find out the note IDs you want to reset by looking at the return value of the first two `get_all_notes()` calls.

### Resetting the Changes to the Matching Data
If you need to rollback to completely re-do the matchings or to a specific point, you may need to reset at least one of the following: (1) the AC research area edges (2) the SAC research area edges or (3) the AC conflict edges

The easiest way to reset (1) and (2) is to run their respective ARR-specific matching scripts. See the previous sections for code on how to do this.

To reset (3), you can make a manual call to `setup_committee_matching`:
```python
venue.setup_committee_matching(
    venue.get_area_chairs_id(),
    None,
    'Default',
    num_years,
    alternate_matching_group=None,
    submission_track=None
)
```