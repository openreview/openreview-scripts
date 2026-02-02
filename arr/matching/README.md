# ARR Matching Utilities (`arr/matching`)

## ARR Matching Workflow (`arr/matching/run_arr_matching.ipynb`)

This notebook contains a set of cells to run through the complete ARR matching workflow. Inside the notebook, you'll find documentation on which cells perform what.

**Note**: In production, **MANY** of these cells can take at least an hour or more for large cycles.

## ARR Matching Core (`arr/matching/core.py`)

The `ARRMatcher` class is the main orchestrator for the ARR matching workflow. It is initialized with an OpenReview client and a request form ID, and coordinates the complete matching process through three distinct phases.

**Pre-matching Phase**: This phase prepares the venue for matching by setting up committee members and their configurations. Key activities include loading SACs into groups with track assignments, registering authors as reviewers or ACs, transferring members between roles, checking for role overlaps, and setting up matching data such as research areas, loads, affinity scores, and conflicts. This phase ensures all committee members are properly registered with correct loads and track preferences before matching begins.

**Matching Phase**: This phase executes the actual paper-to-reviewer/AC/SAC assignments. AC matching and reviewer matching follow the same pipeline: compute affinity scores, compute conflicts, sync loads, sync tracks, then run the automatic assignment. SAC-AC matching delegates to a specialized multi-stage workflow in `sac_core.py`. Matching uses the OpenReview matcher service with configurable solvers (FairIR for reviewers, FairFlow for ACs/SACs).

**Post-matching Phase**: This phase validates matching results and fills gaps. Comprehensive sanity checks verify there are no conflicts, load violations, or papers below minimum assignments. The recommend functions can suggest additional reviewers or ACs for papers that didn't receive enough assignments. Sanity checks should pass before deploying assignments to production.

### Technical Deep Dive

**ARRMatcher Class Constructor**

The constructor creates v1 and v2 API clients from the provided client, loads venue configuration from the request form, and initializes three helper objects:
- `AssignmentsBuilder` - handles assignment computation and edge management
- `SanityChecker` - runs validation checks on matching results
- `RegistrationDataLoader` - loads registration form data

**Pre-matching Functions**

| core.py Method | Delegates To | Purpose |
|----------------|--------------|---------|
| `load_sacs_into_group()` | `ProfileUtils.reset_group_members()`, `RegistrationDataLoader` methods | Validates SAC profiles, resets SAC group membership, posts registration notes with track assignments |
| `register_authors_as_reviewers()` | `client.add_members_to_group()`, `sync_reviewer_loads()` | Adds author profiles to reviewer group and sets their paper load |
| `register_authors_as_acs()` | `client.add_members_to_group()`, `sync_ac_loads()` | Adds author profiles to AC group and sets their paper load |
| `make_reviewers_available()` | `sync_reviewer_loads()` | Updates reviewer load capacity |
| `make_acs_available()` | `sync_ac_loads()` | Updates AC load capacity |
| `transfer_reviewers_to_acs()` | `transfer_between()` in registration.py | Moves members from Reviewers to Area_Chairs group |
| `transfer_acs_to_reviewers()` | `transfer_between()` in registration.py | Moves members from Area_Chairs to Reviewers group |
| `check_reviewer_ac_overlap()` | `SanityChecker.check_role_overlap()` | Checks for members in both Reviewers and Area_Chairs |
| `check_ac_sac_overlap()` | `SanityChecker.check_role_overlap()` | Checks for members in both Area_Chairs and Senior_Area_Chairs |
| `check_sac_reviewer_overlap()` | `SanityChecker.check_role_overlap()` | Checks for members in both Senior_Area_Chairs and Reviewers |
| `setup_reviewer_matching_data()` | External `setup_reviewer_matching` script | Creates submitted reviewer groups, resets CMP edges, updates affinity for resubmissions, posts research area/status/seniority edges |
| `setup_ac_matching_data()` | External `setup_ac_matching` script | Resets CMP edges, updates affinity for resubmissions, posts research area/status edges |
| `setup_sac_matching_data()` | External `setup_sac_matching` script | Resets CMP edges assuming equal loads, posts research area edges |

**Post-matching Functions**

| core.py Method | Delegates To | Purpose |
|----------------|--------------|---------|
| `run_sanity_checks()` | `SanityChecker.run_sanity_checks()` | Runs all validation checks on current assignments |
| `recommend_reviewers()` | `AssignmentsBuilder.recommend_assignments()` | Suggests additional reviewer assignments for papers below target |
| `recommend_acs()` | `AssignmentsBuilder.recommend_assignments()` | Suggests additional AC assignments for papers below target |

**Helper Functions (sync_*, compute_*)**

These methods wrap `AssignmentsBuilder` calls with the appropriate group_id pre-filled:
- `compute_reviewer_conflicts()`, `compute_ac_conflicts()`, `compute_sac_conflicts()` → `AssignmentsBuilder.compute_conflicts()`
- `compute_reviewer_affinity_scores()`, `compute_ac_affinity_scores()`, `compute_sac_affinity_scores()` → `AssignmentsBuilder.compute_affinity_scores()`
- `sync_reviewer_loads()`, `sync_ac_loads()`, `sync_sac_loads()` → `AssignmentsBuilder.sync_max_loads()`
- `sync_reviewer_tracks()`, `sync_ac_tracks()`, `sync_sac_tracks()` → `AssignmentsBuilder.sync_research_areas()`

---

### Helper Module: assignments.py

The `assignments.py` module is the workhorse for paper matching operations. It contains two main classes that handle the core matching functionality.

**MatcherInterface** handles all communication with the OpenReview matcher service. It posts configuration notes that define matching parameters (solver type, constraints, score weights), submits matching jobs to the matcher API, and polls for completion. The matcher service runs optimization algorithms (FairIR for reviewers, FairFlow for ACs/SACs) to produce optimal assignments.

**AssignmentsBuilder** orchestrates the data preparation and matching execution. Before matching can run, it ensures all required edges exist: affinity scores (computed via SPECTER2+SciNCL), conflict-of-interest edges, custom max papers (load capacity), and research area edges (track constraints). It then triggers the matcher and waits for results. After matching, it can recommend additional assignments for papers that didn't receive enough reviewers/ACs.

#### Technical Dive

**MatcherInterface Class**

Called from `AssignmentsBuilder.run_automatic_assignment()` and `SACACMatching` in sac_core.py.

Functions:
- `post_configuration_note_edit()` - Creates an Assignment_Configuration note with matching parameters
- `post_matcher()` - Submits matching job to matcher service via HTTP POST
- `get_matcher_status()` - Reads configuration note to check matching status

| Primitive Type | Invitation Pattern | Operation | Purpose |
|---------------|-------------------|-----------|---------|
| Note | `{venue}/{committee}/-/Assignment_Configuration` | Write | Store matching configuration (solver, weights, constraints) |
| Note | `{venue}/{committee}/-/Assignment_Configuration` | Read | Poll for matching completion status |

---

**AssignmentsBuilder.run_automatic_assignment()**

Called from `ARRMatcher.run_ac_matching()` and `ARRMatcher.run_reviewer_matching()`.

Executes the complete matching workflow: create config, submit to matcher, poll until complete.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        run_automatic_assignment(group_id)                   │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│  1. Load Default Config                                                     │
│     ┌─────────────────────────────────────────────────────────────────┐     │
│     │ Reviewers  → DEFAULT_REVIEWER_MATCHING_CONFIG (FairIR solver)   │     │
│     │ Area_Chairs → DEFAULT_AC_MATCHING_CONFIG (FairFlow solver)      │     │
│     │ Senior_Area_Chairs → DEFAULT_SAC_MATCHING_CONFIG (FairFlow)     │     │
│     └─────────────────────────────────────────────────────────────────┘     │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│  2. Post Configuration Note                                                 │
│     ┌─────────────────────────────────────────────────────────────────┐     │
│     │ POST note_edit to {group_id}/-/Assignment_Configuration         │     │
│     │   - title: "run-{timestamp}"                                    │     │
│     │   - status: "Initialized"                                       │     │
│     │   - solver, scores, constraints from config                     │     │
│     └─────────────────────────────────────────────────────────────────┘     │
│                              Returns: config_note_id                        │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│  3. Submit to Matcher Service                                               │
│     ┌─────────────────────────────────────────────────────────────────┐     │
│     │ HTTP POST to {matcher_baseurl}/match                            │     │
│     │   Body: { "configNoteId": config_note_id }                      │     │
│     │   Headers: OpenReview auth token                                │     │
│     └─────────────────────────────────────────────────────────────────┘     │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│  4. Poll for Completion (up to 24 hours, 60s intervals)                     │
│     ┌─────────────────────────────────────────────────────────────────┐     │
│     │ LOOP:                                                           │     │
│     │   GET config_note.content.status                                │     │
│     │   IF status in ["Complete", "Error", "No Solution", "Cancelled"]│     │
│     │     → EXIT LOOP                                                 │     │
│     │   ELSE                                                          │     │
│     │     → sleep(60), continue                                       │     │
│     └─────────────────────────────────────────────────────────────────┘     │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│  5. Return Result                                                           │
│     ┌─────────────────────────────────────────────────────────────────┐     │
│     │ IF "Error" → raise OpenReviewException with error_message       │     │
│     │ IF timeout → raise OpenReviewException                          │     │
│     │ ELSE → return completed config_note                             │     │
│     └─────────────────────────────────────────────────────────────────┘     │
│                                                                             │
│  Side Effect: Matcher writes Proposed_Assignment edges                      │
└─────────────────────────────────────────────────────────────────────────────┘
```

| Primitive Type | Invitation Pattern | Operation | Purpose |
|---------------|-------------------|-----------|---------|
| Note | `{group}/-/Assignment_Configuration` | Write | Create matching configuration |
| Note | `{group}/-/Assignment_Configuration` | Read | Poll for completion status |
| Edge | `{group}/-/Proposed_Assignment` | Write (by matcher) | Matcher writes computed assignments |

---

**AssignmentsBuilder.sync_max_loads() → post_max_loads()**

Called from `ARRMatcher.sync_reviewer_loads()`, `ARRMatcher.sync_ac_loads()`, `ARRMatcher.sync_sac_loads()`.

Synchronizes Custom_Max_Papers edges with values from Max_Load_And_Unavailability_Request notes, with optional forced overrides.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                   sync_max_loads(group_id, forced_loads)                    │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│  1. Load Group Members                                                      │
│     ┌─────────────────────────────────────────────────────────────────┐     │
│     │ GET group = client.get_group(group_id)                          │     │
│     │ members = group.members  (list of profile IDs/emails)           │     │
│     └─────────────────────────────────────────────────────────────────┘     │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│  2. Load Max Loads from Registration Notes                                  │
│     ┌─────────────────────────────────────────────────────────────────┐     │
│     │ RegistrationDataLoader.get_loads(members, forced_loads)         │     │
│     │                                                                 │     │
│     │ For each member:                                                │     │
│     │   IF member in forced_loads:                                    │     │
│     │     → use forced value (override)                               │     │
│     │   ELSE:                                                         │     │
│     │     → GET notes from {group}/-/Max_Load_And_Unavailability_Request   │
│     │     → extract maximum_load_this_cycle from note.content         │     │
│     │                                                                 │     │
│     │ Returns: Dict[profile_id, load_value]                           │     │
│     └─────────────────────────────────────────────────────────────────┘     │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│  3. Build Custom_Max_Papers Edges                                           │
│     ┌─────────────────────────────────────────────────────────────────┐     │
│     │ For each (profile_id, load) in profile_id_to_loads:             │     │
│     │   permissions = EdgeUtils.build_readers_writers_signatures_...  │     │
│     │   edge = Edge(                                                  │     │
│     │     invitation = "{group}/-/Custom_Max_Papers",                 │     │
│     │     head = group_id,                                            │     │
│     │     tail = profile_id,                                          │     │
│     │     weight = load,                                              │     │
│     │     readers, writers, signatures from permissions               │     │
│     │   )                                                             │     │
│     └─────────────────────────────────────────────────────────────────┘     │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│  4. Delete Existing Edges (with polling)                                    │
│     ┌─────────────────────────────────────────────────────────────────┐     │
│     │ EdgeUtils.delete_edges_with_polling(                            │     │
│     │   invitation = "{group}/-/Custom_Max_Papers"                    │     │
│     │ )                                                               │     │
│     │ Polls until edge count = 0 (10s intervals)                      │     │
│     └─────────────────────────────────────────────────────────────────┘     │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│  5. Post New Edges in Bulk                                                  │
│     ┌─────────────────────────────────────────────────────────────────┐     │
│     │ EdgeUtils.post_bulk_edges(edges_to_post)                        │     │
│     │ Returns: { 'loads_posted': count }                              │     │
│     └─────────────────────────────────────────────────────────────────┘     │
└─────────────────────────────────────────────────────────────────────────────┘
```

| Primitive Type | Invitation Pattern | Operation | Purpose |
|---------------|-------------------|-----------|---------|
| Group | `{venue}/{committee}` | Read | Get list of committee members |
| Note | `{group}/-/Max_Load_And_Unavailability_Request` | Read | Extract load capacity from registration |
| Edge | `{group}/-/Custom_Max_Papers` | Delete | Remove stale load edges before refresh |
| Edge | `{group}/-/Custom_Max_Papers` | Write | Post updated load capacity for matcher |

---

**AssignmentsBuilder.sync_research_areas() → post_research_areas()**

Called from `ARRMatcher.sync_reviewer_tracks()`, `ARRMatcher.sync_ac_tracks()`, `ARRMatcher.sync_sac_tracks()`.

Creates Research_Area edges linking committee members to papers in their preferred tracks.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        sync_research_areas(group_id)                        │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│  1. Load Group Members                                                      │
│     ┌─────────────────────────────────────────────────────────────────┐     │
│     │ GET group = client.get_group(group_id)                          │     │
│     │ members = group.members                                         │     │
│     └─────────────────────────────────────────────────────────────────┘     │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│  2. Load Research Areas from Registration Notes                             │
│     ┌─────────────────────────────────────────────────────────────────┐     │
│     │ RegistrationDataLoader.get_research_areas(members, group_id)    │     │
│     │                                                                 │     │
│     │ Searches (in priority order):                                   │     │
│     │   1. {group}/-/Registration notes → research_area field         │     │
│     │   2. {Authors}/-/Submitted_Author_Form → indicate_your_research_areas│
│     │                                                                 │     │
│     │ Returns: Dict[profile_id, List[research_area_strings]]          │     │
│     └─────────────────────────────────────────────────────────────────┘     │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│  3. Load All Submissions and Build Track Mapping                            │
│     ┌─────────────────────────────────────────────────────────────────┐     │
│     │ GET submissions = client.get_all_notes({venue}/-/Submission)    │     │
│     │                                                                 │     │
│     │ Build: research_area_to_submissions = {                         │     │
│     │   "Computational Linguistics": [sub_id_1, sub_id_2, ...],       │     │
│     │   "Machine Learning": [sub_id_3, sub_id_4, ...],                │     │
│     │   ...                                                           │     │
│     │ }                                                               │     │
│     └─────────────────────────────────────────────────────────────────┘     │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│  4. Validate Research Areas                                                 │
│     ┌─────────────────────────────────────────────────────────────────┐     │
│     │ For each profile's research_area:                               │     │
│     │   IF research_area NOT IN submission tracks:                    │     │
│     │     → raise ValueError("Research area {x} not found")           │     │
│     └─────────────────────────────────────────────────────────────────┘     │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│  5. Build Research_Area Edges                                               │
│     ┌─────────────────────────────────────────────────────────────────┐     │
│     │ For each (profile_id, research_areas) in mapping:               │     │
│     │   For each research_area in research_areas:                     │     │
│     │     For each submission_id in research_area_to_submissions[...]:│     │
│     │       edge = Edge(                                              │     │
│     │         invitation = "{group}/-/Research_Area",                 │     │
│     │         head = submission_id,                                   │     │
│     │         tail = profile_id,                                      │     │
│     │         label = research_area,                                  │     │
│     │         weight = 1                                              │     │
│     │       )                                                         │     │
│     │                                                                 │     │
│     │ Result: Creates edge from each profile to each paper in their   │     │
│     │         preferred tracks                                        │     │
│     └─────────────────────────────────────────────────────────────────┘     │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│  6. Delete Existing + Post New Edges                                        │
│     ┌─────────────────────────────────────────────────────────────────┐     │
│     │ EdgeUtils.delete_edges_with_polling({group}/-/Research_Area)    │     │
│     │ EdgeUtils.post_bulk_edges(edges_to_post)                        │     │
│     │ Returns: { 'research_areas_posted': count }                     │     │
│     └─────────────────────────────────────────────────────────────────┘     │
└─────────────────────────────────────────────────────────────────────────────┘
```

| Primitive Type | Invitation Pattern | Operation | Purpose |
|---------------|-------------------|-----------|---------|
| Group | `{venue}/{committee}` | Read | Get list of committee members |
| Note | `{group}/-/Registration` | Read | Extract research areas from registration |
| Note | `{Authors}/-/Submitted_Author_Form` | Read | Fallback for author research areas |
| Note | `{venue}/-/Submission` | Read | Get all submissions with their tracks |
| Edge | `{group}/-/Research_Area` | Delete | Remove stale track edges |
| Edge | `{group}/-/Research_Area` | Write | Link profiles to papers in their tracks |

---

**AssignmentsBuilder.recommend_assignments()**

Called from `ARRMatcher.recommend_reviewers()` and `ARRMatcher.recommend_acs()`.

For papers with fewer than required assignments, recommends additional committee members based on affinity scores, research area matches, and load capacity.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│         recommend_assignments(group_id, num_required_assignments)           │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│  1. Load All Required Data                                                  │
│     ┌─────────────────────────────────────────────────────────────────┐     │
│     │ PARALLEL FETCHES:                                               │     │
│     │   members = client.get_group(group_id).members                  │     │
│     │   profiles = ProfileUtils.get_valid_profiles(members)           │     │
│     │   submissions = venue.get_submissions()                         │     │
│     │                                                                 │     │
│     │   assignments_by_paper = EdgeUtils.get_assignments(..., by=paper)    │
│     │   assignments_by_user = EdgeUtils.get_assignments(..., by=user) │     │
│     │   invite_assignments = get_grouped_edges(Invite_Assignment)     │     │
│     │                                                                 │     │
│     │   conflicts_by_paper = EdgeUtils.get_conflicts(..., by=paper)   │     │
│     │   affinity_scores_by_user = EdgeUtils.get_affinity_scores(...)  │     │
│     │   research_areas_by_user = EdgeUtils.get_research_areas(...)    │     │
│     │   custom_max_papers = EdgeUtils.get_custom_max_papers(...)      │     │
│     │                                                                 │     │
│     │   profile_id_to_max_load = RegistrationDataLoader.get_loads()   │     │
│     └─────────────────────────────────────────────────────────────────┘     │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│  2. Identify Papers Needing More Assignments                                │
│     ┌─────────────────────────────────────────────────────────────────┐     │
│     │ For each paper_id in all_submissions:                           │     │
│     │   current_count = len(assignments_by_paper[paper_id])           │     │
│     │   invite_count = len(invite_assignments[paper_id])              │     │
│     │   total = current_count + invite_count                          │     │
│     │                                                                 │     │
│     │   IF total < num_required_assignments:                          │     │
│     │     → add to papers_to_process                                  │     │
│     │     needed = num_required - total                               │     │
│     └─────────────────────────────────────────────────────────────────┘     │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│  3. For Each Paper: Filter Available Candidates                             │
│     ┌─────────────────────────────────────────────────────────────────┐     │
│     │ For each user_id in group_members:                              │     │
│     │   SKIP IF:                                                      │     │
│     │     - Already assigned to this paper                            │     │
│     │     - Already in invite_assignments for this paper              │     │
│     │     - Has conflict with this paper (in conflicts_by_paper)      │     │
│     │     - At or over load capacity:                                 │     │
│     │         current_load = len(assignments_by_user[user_id])        │     │
│     │         additional = additional_load[user_id]  (from this run)  │     │
│     │         max_load = custom_max_papers.get(user_id) or            │     │
│     │                    profile_id_to_max_load.get(user_id, 0)       │     │
│     │         IF current_load + additional >= max_load: SKIP          │     │
│     │                                                                 │     │
│     │   → remaining users are available_candidates                    │     │
│     └─────────────────────────────────────────────────────────────────┘     │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│  4. Score Available Candidates                                              │
│     ┌─────────────────────────────────────────────────────────────────┐     │
│     │ For each available user_id:                                     │     │
│     │   score = 0.0                                                   │     │
│     │                                                                 │     │
│     │   # Add affinity score (SPECTER2+SciNCL similarity)             │     │
│     │   IF paper_id in affinity_scores_by_user[user_id]:              │     │
│     │     score += affinity_scores_by_user[user_id][paper_id]         │     │
│     │                                                                 │     │
│     │   # Add research area bonus                                     │     │
│     │   IF paper_id in research_areas_by_user[user_id]:               │     │
│     │     score += 1.0                                                │     │
│     │                                                                 │     │
│     │   user_scores[user_id] = score                                  │     │
│     └─────────────────────────────────────────────────────────────────┘     │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│  5. Select Top Candidates and Build Edges                                   │
│     ┌─────────────────────────────────────────────────────────────────┐     │
│     │ sorted_users = sort by score (descending)                       │     │
│     │                                                                 │     │
│     │ For top {needed} users:                                         │     │
│     │   edge = Edge(                                                  │     │
│     │     invitation = "{group}/-/Proposed_Assignment" or "Assignment"│     │
│     │     head = paper_id,                                            │     │
│     │     tail = user_id,                                             │     │
│     │     weight = user_scores[user_id],                              │     │
│     │     label = assignment_title (if provided)                      │     │
│     │   )                                                             │     │
│     │   additional_load[user_id] += 1  # Track for next paper         │     │
│     └─────────────────────────────────────────────────────────────────┘     │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│  6. Post Recommendation Edges                                               │
│     ┌─────────────────────────────────────────────────────────────────┐     │
│     │ EdgeUtils.post_bulk_edges(edges_to_post)                        │     │
│     │                                                                 │     │
│     │ Returns: {                                                      │     │
│     │   'assignments_recommended': count,                             │     │
│     │   'papers_processed': papers_needing_more,                      │     │
│     │   'papers_filled': papers_that_reached_target                   │     │
│     │ }                                                               │     │
│     └─────────────────────────────────────────────────────────────────┘     │
└─────────────────────────────────────────────────────────────────────────────┘
```

| Primitive Type | Invitation Pattern | Operation | Purpose |
|---------------|-------------------|-----------|---------|
| Group | `{venue}/{committee}` | Read | Get list of committee members |
| Note | `{venue}/-/Submission` | Read | Get all submissions |
| Edge | `{group}/-/Assignment` or `Proposed_Assignment` | Read | Get current assignments per paper/user |
| Edge | `{group}/-/Invite_Assignment` | Read | Get pending invite assignments |
| Edge | `{group}/-/Conflict` | Read | Get conflicts to avoid |
| Edge | `{group}/-/Affinity_Score` | Read | Get semantic similarity scores |
| Edge | `{group}/-/Research_Area` | Read | Get track matches |
| Edge | `{group}/-/Custom_Max_Papers` | Read | Get load capacity |
| Note | `{group}/-/Max_Load_And_Unavailability_Request` | Read | Fallback for load capacity |
| Edge | `{group}/-/Assignment` or `Proposed_Assignment` | Write | Post recommended assignments |

---

### Helper Module: registration.py

The `registration.py` module handles loading committee member preferences from registration forms and managing role membership.

**RegistrationDataLoader** reads the registration notes that committee members fill out during signup. It extracts two key pieces of information: research areas (which tracks/topics they want to review) and maximum load (how many papers they can handle this cycle). The loader handles profile name normalization, merges data from multiple form types, and resolves the most recent submission when members update their preferences.

**transfer_between** is a utility function for moving members between committee roles. This is commonly used when an AC wants to also serve as a reviewer, or when someone needs to switch roles entirely. It properly handles profile name variants and prevents duplicate membership.

#### Technical Dive

**RegistrationDataLoader.get_research_areas()**

Called from `AssignmentsBuilder.sync_research_areas()` and used in track assignment workflows.

Loads research area preferences for a list of committee members from their registration notes.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│              get_research_areas(members, group_id=None)                     │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│  1. Normalize Member Identities                                             │
│     ┌─────────────────────────────────────────────────────────────────┐     │
│     │ profiles = ProfileUtils.get_valid_profiles(members)             │     │
│     │                                                                 │     │
│     │ Build mappings:                                                 │     │
│     │   profile_ids = {profile.id for profile in profiles}            │     │
│     │   name_to_profile_id = {                                        │     │
│     │     "~John_Smith1": "~John_Smith1",                             │     │
│     │     "john@example.com": "~John_Smith1",                         │     │
│     │     ...                                                         │     │
│     │   }                                                             │     │
│     └─────────────────────────────────────────────────────────────────┘     │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│  2. Load Registration Notes                                                 │
│     ┌─────────────────────────────────────────────────────────────────┐     │
│     │ IF group_id provided:                                           │     │
│     │   GET notes from {group_id}/-/Registration                      │     │
│     │ ELSE:                                                           │     │
│     │   GET notes from:                                               │     │
│     │     - {Reviewers}/-/Registration                                │     │
│     │     - {Area_Chairs}/-/Registration                              │     │
│     │     - {Senior_Area_Chairs}/-/Registration                       │     │
│     │                                                                 │     │
│     │ ALSO load author forms:                                         │     │
│     │   GET notes from {Authors}/-/Submitted_Author_Form              │     │
│     └─────────────────────────────────────────────────────────────────┘     │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│  3. Map Notes to Profiles                                                   │
│     ┌─────────────────────────────────────────────────────────────────┐     │
│     │ For each note in all_notes:                                     │     │
│     │   # Extract submitter identity                                  │     │
│     │   signature = note.signatures[0]                                │     │
│     │   IF 'profile_id' in note.content:                              │     │
│     │     signature = note.content['profile_id']['value']             │     │
│     │                                                                 │     │
│     │   # Resolve to canonical profile ID                             │     │
│     │   profile_id = name_to_profile_id.get(signature)                │     │
│     │   IF profile_id in profile_ids:                                 │     │
│     │     profile_id_to_notes[profile_id].append(                     │     │
│     │       (note, timestamp, source_type)                            │     │
│     │     )                                                           │     │
│     └─────────────────────────────────────────────────────────────────┘     │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│  4. Extract Research Areas (Most Recent Note Wins)                          │
│     ┌─────────────────────────────────────────────────────────────────┐     │
│     │ For each profile_id in profile_ids:                             │     │
│     │   notes = sorted by timestamp (most recent first)               │     │
│     │                                                                 │     │
│     │   For each note (in order):                                     │     │
│     │     TRY:                                                        │     │
│     │       # Registration note field                                 │     │
│     │       IF 'research_area' in note.content:                       │     │
│     │         research_areas = note.content['research_area']['value'] │     │
│     │         BREAK                                                   │     │
│     │                                                                 │     │
│     │       # Author form field                                       │     │
│     │       IF 'indicate_your_research_areas' in note.content:        │     │
│     │         research_areas = note.content[...]['value']             │     │
│     │         BREAK                                                   │     │
│     │                                                                 │     │
│     │   IF research_areas found:                                      │     │
│     │     profile_id_to_research_areas[profile_id] = research_areas   │     │
│     │   ELSE:                                                         │     │
│     │     missing_members.append(profile_id)                          │     │
│     └─────────────────────────────────────────────────────────────────┘     │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│  5. Return Mapping                                                          │
│     ┌─────────────────────────────────────────────────────────────────┐     │
│     │ Log: "notes_loaded={N}, mapped={M}, missing={X}"                │     │
│     │ Return: Dict[profile_id, List[research_area_str]]               │     │
│     └─────────────────────────────────────────────────────────────────┘     │
└─────────────────────────────────────────────────────────────────────────────┘
```

| Primitive Type | Invitation Pattern | Operation | Purpose |
|---------------|-------------------|-----------|---------|
| Profile | N/A (via get_profiles) | Read | Resolve member identities to canonical IDs |
| Note | `{group}/-/Registration` | Read | Extract research_area field from registration |
| Note | `{Authors}/-/Submitted_Author_Form` | Read | Fallback: extract indicate_your_research_areas |

---

**RegistrationDataLoader.get_loads()**

Called from `AssignmentsBuilder.sync_max_loads()` and `recommend_assignments()`.

Loads maximum paper load capacity for committee members, with support for forced overrides.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│              get_loads(members, forced_loads=None, group_id=None)           │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│  1. Validate Forced Loads                                                   │
│     ┌─────────────────────────────────────────────────────────────────┐     │
│     │ IF forced_loads provided:                                       │     │
│     │   For each (member_id, load_value):                             │     │
│     │     IF NOT isinstance(load_value, int) OR load_value < 0:       │     │
│     │       raise ValueError("Invalid forced_load value")             │     │
│     └─────────────────────────────────────────────────────────────────┘     │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│  2. Normalize Member Identities                                             │
│     ┌─────────────────────────────────────────────────────────────────┐     │
│     │ profiles = ProfileUtils.get_valid_profiles(members)             │     │
│     │ profile_ids = {profile.id for profile in profiles}              │     │
│     │ name_to_profile_id = map all names → canonical ID               │     │
│     │                                                                 │     │
│     │ # Normalize forced_loads keys to canonical IDs                  │     │
│     │ normalized_forced_loads = {}                                    │     │
│     │ For each (member_id, load) in forced_loads:                     │     │
│     │   canonical_id = name_to_profile_id[member_id] or member_id     │     │
│     │   IF canonical_id in profile_ids:                               │     │
│     │     normalized_forced_loads[canonical_id] = load                │     │
│     │   ELSE:                                                         │     │
│     │     log warning: "non-member in forced_loads"                   │     │
│     └─────────────────────────────────────────────────────────────────┘     │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│  3. Load Max Load Notes                                                     │
│     ┌─────────────────────────────────────────────────────────────────┐     │
│     │ IF group_id provided:                                           │     │
│     │   GET notes from {group_id}/-/Max_Load_And_Unavailability_Request    │
│     │ ELSE:                                                           │     │
│     │   GET notes from:                                               │     │
│     │     - {Reviewers}/-/Max_Load_And_Unavailability_Request         │     │
│     │     - {Area_Chairs}/-/Max_Load_And_Unavailability_Request       │     │
│     │     - {Senior_Area_Chairs}/-/Max_Load_And_Unavailability_Request│     │
│     └─────────────────────────────────────────────────────────────────┘     │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│  4. Map Notes to Profiles (Keep Most Recent)                                │
│     ┌─────────────────────────────────────────────────────────────────┐     │
│     │ For each note in all_load_notes:                                │     │
│     │   signature = resolve from note.signatures or content.profile_id│     │
│     │   profile_id = name_to_profile_id.get(signature)                │     │
│     │                                                                 │     │
│     │   IF profile_id in profile_ids:                                 │     │
│     │     IF profile_id NOT in profile_id_to_note:                    │     │
│     │       profile_id_to_note[profile_id] = note                     │     │
│     │     ELSE IF note.tmdate > existing.tmdate:                      │     │
│     │       profile_id_to_note[profile_id] = note  # Keep newer       │     │
│     └─────────────────────────────────────────────────────────────────┘     │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│  5. Extract Loads (Forced Override > Note Value)                            │
│     ┌─────────────────────────────────────────────────────────────────┐     │
│     │ For each profile_id in profile_ids:                             │     │
│     │                                                                 │     │
│     │   # Priority 1: Forced load                                     │     │
│     │   IF profile_id in normalized_forced_loads:                     │     │
│     │     profile_id_to_loads[profile_id] = forced_value              │     │
│     │     overrides_applied += 1                                      │     │
│     │     CONTINUE                                                    │     │
│     │                                                                 │     │
│     │   # Priority 2: Note value                                      │     │
│     │   IF profile_id in profile_id_to_note:                          │     │
│     │     note = profile_id_to_note[profile_id]                       │     │
│     │     load = note.content['maximum_load_this_cycle']['value']     │     │
│     │     IF load >= 0:                                               │     │
│     │       profile_id_to_loads[profile_id] = int(load)               │     │
│     │     ELSE:                                                       │     │
│     │       invalid_load_values += 1                                  │     │
│     └─────────────────────────────────────────────────────────────────┘     │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│  6. Return Mapping                                                          │
│     ┌─────────────────────────────────────────────────────────────────┐     │
│     │ Log: "notes_loaded={N}, overrides={O}, invalid={X}"             │     │
│     │ Return: Dict[profile_id, int]                                   │     │
│     └─────────────────────────────────────────────────────────────────┘     │
└─────────────────────────────────────────────────────────────────────────────┘
```

| Primitive Type | Invitation Pattern | Operation | Purpose |
|---------------|-------------------|-----------|---------|
| Profile | N/A (via get_profiles) | Read | Resolve member identities to canonical IDs |
| Note | `{group}/-/Max_Load_And_Unavailability_Request` | Read | Extract maximum_load_this_cycle field |

---

**transfer_between()**

Called from `ARRMatcher.transfer_reviewers_to_acs()` and `ARRMatcher.transfer_acs_to_reviewers()`.

Moves members from one committee role to another, handling profile name variants properly.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│     transfer_between(from_group, to_group, members, client, dry_run)        │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│  1. Validate Input                                                          │
│     ┌─────────────────────────────────────────────────────────────────┐     │
│     │ IF members is None:                                             │     │
│     │   raise ValueError("members parameter is required")             │     │
│     └─────────────────────────────────────────────────────────────────┘     │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│  2. Normalize Member Identities                                             │
│     ┌─────────────────────────────────────────────────────────────────┐     │
│     │ profiles = ProfileUtils.get_valid_profiles(members)             │     │
│     │ profile_ids = [profile.id for profile in profiles]              │     │
│     │                                                                 │     │
│     │ Build mappings:                                                 │     │
│     │   name_to_profile_id = any_name → canonical_id                  │     │
│     │   name_to_all_names = any_name → [all_names_for_that_profile]   │     │
│     └─────────────────────────────────────────────────────────────────┘     │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│  3. Load Current Group Memberships                                          │
│     ┌─────────────────────────────────────────────────────────────────┐     │
│     │ from_group_obj = client.get_group(from_group)                   │     │
│     │ to_group_obj = client.get_group(to_group)                       │     │
│     │                                                                 │     │
│     │ # Normalize group members to detect membership by any name      │     │
│     │ from_group_members_set = normalize_to_all_names(from_group.members)  │
│     │ to_group_members_set = normalize_to_all_names(to_group.members) │     │
│     └─────────────────────────────────────────────────────────────────┘     │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│  4. Determine Transfer Actions                                              │
│     ┌─────────────────────────────────────────────────────────────────┐     │
│     │ For each profile_id in profile_ids:                             │     │
│     │   all_names = name_to_all_names[profile_id]                     │     │
│     │                                                                 │     │
│     │   # Check source membership (by any name variant)               │     │
│     │   in_source = any(name in from_group_members_set for name in all_names)│
│     │                                                                 │     │
│     │   # Check target membership (by any name variant)               │     │
│     │   in_target = any(name in to_group_members_set for name in all_names) │
│     │                                                                 │     │
│     │   IF NOT in_source:                                             │     │
│     │     members_skipped_not_in_source += 1                          │     │
│     │   ELIF in_target:                                               │     │
│     │     members_skipped_already_in_target += 1                      │     │
│     │   ELSE:                                                         │     │
│     │     # Find actual identifier in from_group                      │     │
│     │     actual_from_member = find_in(from_group.members, all_names) │     │
│     │     members_to_remove.append(actual_from_member)                │     │
│     │     members_to_add.append(profile_id)  # Use canonical ID       │     │
│     └─────────────────────────────────────────────────────────────────┘     │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│  5. Execute Transfers (if not dry_run)                                      │
│     ┌─────────────────────────────────────────────────────────────────┐     │
│     │ IF NOT dry_run:                                                 │     │
│     │   # Remove from source group                                    │     │
│     │   client.delete_members_from_group(from_group, members_to_remove)    │
│     │                                                                 │     │
│     │   # Add to target group                                         │     │
│     │   client.add_members_to_group(to_group, members_to_add)         │     │
│     └─────────────────────────────────────────────────────────────────┘     │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│  6. Return Statistics                                                       │
│     ┌─────────────────────────────────────────────────────────────────┐     │
│     │ Return: {                                                       │     │
│     │   'members_added': len(members_to_add),                         │     │
│     │   'members_removed': len(members_to_remove),                    │     │
│     │   'members_skipped_not_in_source': count,                       │     │
│     │   'members_skipped_already_in_target': count                    │     │
│     │ }                                                               │     │
│     └─────────────────────────────────────────────────────────────────┘     │
└─────────────────────────────────────────────────────────────────────────────┘
```

| Primitive Type | Invitation Pattern | Operation | Purpose |
|---------------|-------------------|-----------|---------|
| Profile | N/A (via get_profiles) | Read | Resolve member identities and name variants |
| Group | `{venue}/{from_committee}` | Read | Get current source group membership |
| Group | `{venue}/{to_committee}` | Read | Get current target group membership |
| Group | `{venue}/{from_committee}` | Write (delete members) | Remove members from source group |
| Group | `{venue}/{to_committee}` | Write (add members) | Add members to target group |

---

### Helper Module: sanity.py

The `sanity.py` module validates matching results before they are deployed to production. The main entry point, `run_sanity_checks()`, runs a comprehensive suite of validation checks and returns a dictionary of results with counts of any violations found.

#### Technical Dive

**SanityChecker.run_sanity_checks()**

Called from `ARRMatcher.run_sanity_checks()`.

Orchestrates all validation checks and aggregates results.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│   run_sanity_checks(sac_assignment_title, ac_assignment_title,              │
│                     reviewer_assignment_title)                              │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
           ┌──────────────────────────┼──────────────────────────┐
           │                          │                          │
           ▼                          ▼                          ▼
┌─────────────────────┐  ┌─────────────────────┐  ┌─────────────────────┐
│ CHECK 1:            │  │ CHECK 2:            │  │ CHECK 3:            │
│ check_max_loads_    │  │ check_papers_below_ │  │ check_assignments_  │
│ against_cmp()       │  │ min_assignments()   │  │ atmost_max_load()   │
├─────────────────────┤  ├─────────────────────┤  ├─────────────────────┤
│ DATA ACCESSED:      │  │ DATA ACCESSED:      │  │ DATA ACCESSED:      │
│ ┌─────────────────┐ │  │ ┌─────────────────┐ │  │ ┌─────────────────┐ │
│ │Group: Reviewers │ │  │ │Edge: SAC/-/     │ │  │ │Edge: AC/-/      │ │
│ │Group: Area_Chairs│ │  │ │  Assignment     │ │  │ │  Assignment     │ │
│ │                 │ │  │ │Edge: AC/-/      │ │  │ │Edge: Reviewer/-/│ │
│ │Edge: AC/-/      │ │  │ │  Assignment     │ │  │ │  Assignment     │ │
│ │ Custom_Max_Papers│ │  │ │Edge: Reviewer/-/│ │  │ │                 │ │
│ │Edge: Reviewer/-/│ │  │ │  Assignment     │ │  │ │Edge: AC/-/      │ │
│ │ Custom_Max_Papers│ │  │ └─────────────────┘ │  │ │ Custom_Max_Papers│ │
│ │                 │ │  │                     │  │ │Edge: Reviewer/-/│ │
│ │Note: Max_Load_  │ │  │ VALIDATES:          │  │ │ Custom_Max_Papers│ │
│ │ And_Unavail...  │ │  │ - SAC: ≥1 per paper │  │ └─────────────────┘ │
│ └─────────────────┘ │  │ - AC: ≥1 per paper  │  │                     │
│                     │  │ - Rev: ≥3 per paper │  │ VALIDATES:          │
│ VALIDATES:          │  └─────────────────────┘  │ assignments ≤ CMP   │
│ CMP edge ≤ load note│                           │ for each user       │
└─────────────────────┘                           └─────────────────────┘
           │                          │                          │
           └──────────────────────────┼──────────────────────────┘
                                      │
           ┌──────────────────────────┼──────────────────────────┐
           │                          │                          │
           ▼                          ▼                          ▼
┌─────────────────────┐  ┌─────────────────────┐  ┌─────────────────────┐
│ CHECK 4:            │  │ CHECK 5:            │  │ CHECK 6:            │
│ check_sac_ac_       │  │ check_no_conflicts()│  │ check_role_overlap()│
│ mapping()           │  │ (called 3x)         │  │ (called 3x)         │
├─────────────────────┤  ├─────────────────────┤  ├─────────────────────┤
│ DATA ACCESSED:      │  │ DATA ACCESSED:      │  │ DATA ACCESSED:      │
│ ┌─────────────────┐ │  │ ┌─────────────────┐ │  │ ┌─────────────────┐ │
│ │Edge: SAC/-/     │ │  │ │Edge: {group}/-/ │ │  │ │Group: SAC       │ │
│ │  Assignment     │ │  │ │  Conflict       │ │  │ │Group: AC        │ │
│ │  (by user)      │ │  │ │Edge: {group}/-/ │ │  │ │Group: Reviewers │ │
│ │                 │ │  │ │  Assignment     │ │  │ └─────────────────┘ │
│ │Edge: AC/-/      │ │  │ └─────────────────┘ │  │                     │
│ │  Assignment     │ │  │                     │  │ VALIDATES:          │
│ │  (by user)      │ │  │ Runs for:           │  │ No member in        │
│ │                 │ │  │ - Senior_Area_Chairs│  │ multiple roles:     │
│ │Edge: AC/-/      │ │  │ - Area_Chairs       │  │ - SAC ∩ AC = ∅      │
│ │  Assignment     │ │  │ - Reviewers         │  │ - SAC ∩ Rev = ∅     │
│ │  (by paper)     │ │  │                     │  │ - AC ∩ Rev = ∅      │
│ └─────────────────┘ │  │ VALIDATES:          │  └─────────────────────┘
│                     │  │ No user assigned to │
│ VALIDATES:          │  │ paper they conflict │
│ All AC papers are   │  │ with                │
│ assigned to their   │  └─────────────────────┘
│ SAC's papers        │
└─────────────────────┘
           │                          │                          │
           └──────────────────────────┼──────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│  AGGREGATE RESULTS                                                          │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │ Returns Dict with counts:                                           │    │
│  │   'ac_max_papers_exceeding_max_load_note': int                      │    │
│  │   'reviewer_max_papers_exceeding_max_load_note': int                │    │
│  │   'sac_assignments_below_min_assignments': int                      │    │
│  │   'ac_assignments_below_min_assignments': int                       │    │
│  │   'reviewer_assignments_below_min_assignments': int                 │    │
│  │   'ac_assignments_exceeding_max_load': int                          │    │
│  │   'reviewer_assignments_exceeding_max_load': int                    │    │
│  │   'acs_with_sac_mismatch': int                                      │    │
│  │   '{group} with conflicts': int (3 entries)                         │    │
│  │   '{group1}-{group2} overlap': int (3 entries)                      │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
│                                                                             │
│  All zeros = matching ready for deployment                                  │
└─────────────────────────────────────────────────────────────────────────────┘
```

| Primitive Type | Invitation Pattern | Operation | Purpose |
|---------------|-------------------|-----------|---------|
| Group | `{venue}/Reviewers` | Read | Get members for overlap check |
| Group | `{venue}/Area_Chairs` | Read | Get members for overlap check |
| Group | `{venue}/Senior_Area_Chairs` | Read | Get members for overlap check |
| Edge | `{group}/-/Assignment` or `Proposed_Assignment` | Read | Get current assignments |
| Edge | `{group}/-/Custom_Max_Papers` | Read | Get load capacity limits |
| Edge | `{group}/-/Conflict` | Read | Get conflicts of interest |
| Note | `{group}/-/Max_Load_And_Unavailability_Request` | Read | Get registered load capacity |

---

### Utility Modules

#### edge_utils.py

Provides utilities for Edge CRUD operations and permission building.

**EdgeGroupBy Enum:**
- `user` (value: 'tail') - Group edges by the user (tail of edge)
- `paper` (value: 'head') - Group edges by the paper (head of edge)

**Functions:**

- `delete_edges_with_polling()` - Trigger async edge deletion and poll until edges disappear. Supports filtering by invitation, id, label, head, tail. Raises on timeout (default 20 minutes).

- `build_readers_writers_signatures_nonreaders()` - Build permission dict for edge based on role type (reviewers/ACs/SACs) and edge type (config/assignment). Handles paper-specific permissions for assignment edges.

- `post_bulk_edges()` - Post edges in bulk using `openreview.tools.post_bulk_edges()`.

- `post_sequential_edges()` - (Not implemented) Would post edges sequentially for notification triggers.

**Edge Getters (all return Dict[str, ...] keyed by head or tail):**

- `get_affinity_scores(group_id, by)` - Returns `Dict[outer_id, Dict[inner_id, weight]]` from Affinity_Score edges
- `get_aggregate_scores(group_id, by)` - Returns from Aggregate_Score edges
- `get_conflicts(group_id, by, full_edges)` - Returns conflict paper/user IDs or full edge dicts
- `get_research_areas(group_id, by, full_edges)` - Returns research area paper/user IDs or full edge dicts
- `get_custom_max_papers(group_id)` - Returns `Dict[user_id, load]` from Custom_Max_Papers edges
- `get_assignments(group_id, by, title, full_edges)` - Returns from Assignment or Proposed_Assignment edges (based on title param)

---

#### profile_utils.py

Provides utilities for profile validation and group membership management.

**Functions:**

- `reset_group_members()` - Reset a group's membership to exactly the target members list. Deletes all existing members, adds all target members. Returns counts of members deleted/added.

- `get_valid_profiles()` - Fetch profiles for a list of IDs/emails. Raises ValueError if any profile not found or if email-only profiles exist (no tilde ID).

- `get_all_profile_names()` - Extract all username variants from a list of profiles. Returns flat list of all `~Name1`, `~Name2`, etc.

- `map_profile_names_to_profile_id()` - Create mapping from any name variant to canonical profile.id. Useful for normalizing signatures.

- `map_profile_names_to_all_names()` - Create mapping from any name variant to list of all names for that profile. Useful for membership checks.

---

#### note_utils.py

Provides utilities for extracting profile information from notes.

**Functions:**

- `get_profile_ids_from_notes()` - Extract canonical profile IDs from a list of notes. Uses note signatures or profile_id content field.

- `map_profile_names_to_note()` - Create mapping from any profile name variant to their note. Useful when looking up a member's registration by any of their names.

- `map_profile_id_to_note()` - Create mapping from canonical profile.id to note. More precise than name-based lookup.

- `bulk_delete_notes()` - Soft-delete a list of notes by posting note_edit with ddate. Uses venue's meta invitation.

---

## ARR SAC-Matching Core (`arr/matching/sac_core.py`)

The `sac_core.py` module implements a sophisticated multi-stage SAC-AC matching workflow. Unlike the simpler reviewer matching which runs a single optimization pass, SAC-AC matching requires multiple iterations to properly handle the hierarchical assignment structure.

The core challenge is that SACs must be assigned to papers, ACs are assigned to papers, and we need ACs to only have 1 SAC. We cannot assign SACs to ACs because they need to have authority over the paper, which can only be done if they are assigned to papers. The solution is an iterative refinement approach: first run AC matching without constraints to infer track affinities, then constrain subsequent matchings based on those inferences.

### High-Level Steps in run_matching()

1. **Prepare Data** - Reset data structures if `reset_data` flags are set (reset_sac_tracks, reset_ac_tracks). Loads MatchingData with all venue information.

2. **Load Checkpoint** - Check for existing matching results to enable resumability. Determines which steps need to be re-run vs skipped.

3. **Create Priority Track Load Plan** - Calculate how many papers each SAC should handle per track based on their priority track and overall paper distribution. In the absence of priority track and research areas, it defaults to the first/only research area

4. **Merge SAC Tracks with Volunteers** - Incorporate volunteer SAC assignments into the track plan. Updates SAC track edges if reset_sac_tracks is set. This is skipped with a single track

5. **First AC Matching (Naive)** - Run AC-paper matching without any track constraints. Uses affinity scores and conflicts only.

6. **Map ACs to Tracks** - Analyze naive matching results to infer which tracks each AC is effectively reviewing. Extracts track labels from assigned papers.

7. **Second AC Matching (Track-Constrained)** - Re-run AC-paper matching with Research_Area constraints based on inferred tracks. Produces more track-coherent assignments.

8. **Map ACs to SACs** - Assign each AC to a SAC based on track overlap. Ensures ACs work with SACs in compatible tracks.

9. **Transfer Conflicts** - Propagate SAC conflicts of interest to their assigned ACs. Prevents ACs from reviewing papers their SAC is conflicted with.

10. **Third AC Matching (SAC-Constrained)** - Final AC-paper matching incorporating transferred SAC conflicts. Produces conflict-clean assignments.

11. **Infer SAC Assignments** - Create SAC-paper assignment edges based on which papers their ACs are assigned to. SAC inherits all papers from their ACs.

12. **Post Aggregate Scores** - Compute and post final SAC affinity aggregate scores for deployed assignments.

### Note on MatcherInterface

The `sac_core.py` module contains its own `MatcherInterface` class which is functionally identical to the one in `assignments.py`. See the assignments.py documentation above for details on how the matcher interface works.
