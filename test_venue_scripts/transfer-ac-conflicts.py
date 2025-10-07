import openreview
import csv
from collections import defaultdict


### Transfer conflicts for AC pairs/triplets/any size AC group


# 0. Setup
venue_id = ''

client_v2 = openreview.api.OpenReviewClient(
    baseurl='https://api2.openreview.net',
    username='',
    password=''
)


# 1. Map ACs to all their conflicts
ac_to_conflicts =  { 
    group['id']['tail']: group['values'] 
    for group in client_v2.get_grouped_edges(
        invitation=f'{venue_id}/Area_Chairs/-/Conflict',
        groupby='tail',
        select='head,tail'
)}


# 2. Map paper IDs to list of users who have conflicts with that paper
paper_to_conflicted_acs = defaultdict(set)

for edges in ac_to_conflicts.values():
    for edge in edges:
        paper_to_conflicted_acs[edge['head']].add(edge['tail'])


# 3. Read pair/triplet file, gather all groupings and ACs listed in file
# - Called circles to generalize pair/triplet naming
# - Assumes file has no header and columns are: AC1, AC2, AC3, etc.
file_name = 'file.csv'
ac_circles = []
all_file_acs = set()

with open(file_name, 'r', newline='') as file:
    csv_reader = csv.reader(file, delimiter=',')
    for row in csv_reader:
        members = [ac.strip() for ac in row if ac.strip()]
        if not members:
            continue  # skip empty lines

        ac_circles.append(members)
        all_file_acs.update(members)


# 4. Check that ACs in file are profile IDs
ac_circle_profile_ids = [p.id for p in openreview.tools.get_profiles(client_v2, all_file_acs)]

print('AC profile IDs not in file: ', set(ac_circle_profile_ids) - set(all_file_acs))
print('IDs in file that do not map to a profile: ', set(all_file_acs) - set(ac_circle_profile_ids))


# 5. Check that ACs in file match ACs in group
ac_mems = client_v2.get_group(f'{venue_id}/Area_Chairs').members
ac_profile_ids = [p.id for p in openreview.tools.get_profiles(client_v2, ac_mems)]

print('ACs in the group that are not in file: ', set(ac_profile_ids) - set(ac_circle_profile_ids))
print('ACs in the file that are not in the group: ', set(ac_circle_profile_ids) - set(ac_profile_ids))


# 6. Build conflict edges
conflict_edges = []

for circle in ac_circles:
    # Gather paper IDs of all conflicted papers in circle
    circle_paper_conflicts = set()
    for member in circle:
        if member in ac_to_conflicts:
            circle_paper_conflicts.update(edge['head'] for edge in ac_to_conflicts[member])

    # Propagate conflicts to everyone in the circle
    for member in circle:
        for paper_id in circle_paper_conflicts:
            # If user has no conflict with this paper create new edge
            if member not in paper_to_conflicted_acs[paper_id]:
                conflict_edges.append(openreview.api.Edge(
                    invitation=f'{venue_id}/Area_Chairs/-/Conflict',
                    label='Pair Conflict',
                    weight=-1,
                    head=paper_id,
                    tail=member,
                    signatures=[venue_id],
                    readers=[venue_id, member],
                    writers=[venue_id]
                ))

                # Add user as conflict so we don't dupe data
                paper_to_conflicted_acs[paper_id].add(member)

print('New conflict edges: ', len(conflict_edges))


# 7. Post edges
# openreview.tools.post_bulk_edges(client=client_v2, edges=conflict_edges)
