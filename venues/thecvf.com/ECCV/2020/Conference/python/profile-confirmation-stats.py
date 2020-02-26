import openreview
import csv
from tqdm import tqdm

client = openreview.Client(baseurl = 'https://openreview.net')

reviewer_group_name = 'Reviewers'

reviewer_group = client.get_group('thecvf.com/ECCV/2020/Conference/' + reviewer_group_name)

confirmations = {
    c.tauthor: c for c in list(
        openreview.tools.iterget_notes(
            client, 
            invitation='thecvf.com/ECCV/2020/Conference/{grp}/-/Profile_Confirmation'.format(grp=reviewer_group_name)))}
print ('Confirmations received: ', len(confirmations))

custom_loads = {
    c.content['user']: c for c in list(openreview.tools.iterget_notes(
        client, 
        invitation='thecvf.com/ECCV/2020/Conference/-/Reduced_Load'))}

print ('Custom loads received: ', len(custom_loads))



profile_map = {}

emails = []
tildes = []
for ac in reviewer_group.members:
    if ac.startswith('~'):
        tildes.append(ac)
    else:
        emails.append(ac)

active = 0
tilde_profiles=client.search_profiles(ids=tildes)
email_profiles=client.search_profiles(emails=emails)

inactives = []

for profile in tilde_profiles:
    profile_map[profile.id] = profile
    if profile.active and profile.password:
        active+=1
    else:
        inactives.append(profile.id)

for member in email_profiles:
    profile_map[member] = email_profiles[member]
    if profile_map[member].active and profile_map[member].password:
        active+=1
    else:
        inactives.append(member)


print (active)
print ('Number of inactive profiles:', len(inactives))
print (len(profile_map))



miss = 0
total_review_capacity = 0
consider_unconfirmed_profiles = True

with open('/Users/muniyal/Desktop/reviewer_out.csv', 'w') as f:
    csv_writer = csv.writer(f)
    csv_writer.writerow(['Reviewer ID', 'Profile Confirmed', 'Emergency review quota', 'Requested review Load', 'Normal review capacity'])
    for reviewer in tqdm(reviewer_group.members):
        review_capacity = 0
        
        profile = profile_map.get(reviewer, None)
        if not profile:
            miss += 1
            profile = openreview.tools.get_profile(client, reviewer)

        confirmation = None
        custom_load = None
        if profile:
            ids = profile.content['emailsConfirmed'] + [ n['username'] for n in profile.content['names'] if 'username' in n]
            for i in ids:
                if i in confirmations:
                    confirmation=confirmations[i]
                if i in custom_loads:
                    custom_load=custom_loads[i]

        output=[]
        output.append(reviewer)
        
        if confirmation or consider_unconfirmed_profiles:
            if not custom_load:
                review_capacity = 7 
            else:
                review_capacity = int(custom_load.content['reviewer_load'])

        if confirmation:
            output.append('Yes')
            output.append(confirmation.content.get('emergency_review_count', '0'))
            review_capacity -= int(confirmation.content.get('emergency_review_count', '0'))
            if review_capacity < 0:
                print ('capacity error for reviewer: ', profile.id)
        else:
            output.append('No')
            output.append('')

        if custom_load:
            print ('adding custom load {0} for reviewer {1}'.format(custom_load.content['reviewer_load'], profile.id))
            output.append(custom_load.content['reviewer_load'])
        else:
            output.append('7')
        output.append(review_capacity)
        csv_writer.writerow(output)

print ('Reviewers with no profiles: ', miss)