from __future__ import print_function, unicode_literals
import argparse
import openreview
import openreview.tools as tools

## Argument handling
parser = argparse.ArgumentParser()
parser.add_argument('--baseurl', help="base url")
parser.add_argument('--username')
parser.add_argument('--password')
parser.add_argument('--tcdate')

args = parser.parse_args()

client = openreview.Client(baseurl=args.baseurl, username=args.username, password=args.password)
conference = 'learningtheory.org/COLT/2019/Conference'

def run(args):
    new_official_reviews = list(openreview.tools.iterget_notes(client, invitation = conference+'/-/Paper.*/Official_Review', mintcdate = args.tcdate))
    
    for review in new_official_reviews:
        if 'AnonReviewer' in review.signatures[0]:
            invited_reviewer = client.get_group(review.signatures[0]).members[0]
            paper_number = review.signatures[0].split('Paper')[1].split('/')[0]
            acceptance_notes = client.get_notes(
                invitation = conference + '/Program_Committee/-/Paper' + paper_number + '/Recruit_Reviewers')
            
            # If multiple PC members invited the same subreviewer, we mark all the PC members as Submitted
            submitted_pc_members = []
            for accept_note in acceptance_notes:
                if (accept_note.content['email'] == invited_reviewer and accept_note.content['response'] == 'Yes'):
                    submitted_pc_members.append(accept_note.content['invitedBy'])
            
            submitted_pc_anon_groups = []
            for pc in submitted_pc_members:
                grp = client.get_groups(
                    regex = conference + '/Paper' + paper_number +'/Program_Committee_Member[0-9]*',
                    member = pc)
                if len(grp):
                    submitted_pc_anon_groups.append(grp[0].id)
            
            if (len(submitted_pc_anon_groups)):
                pc_submitted_group = client.get_group(id = conference + '/Paper' + paper_number + '/Program_Committee/Submitted')
                pc_unsubmitted_group = client.get_group(id = conference + '/Paper' + paper_number + '/Program_Committee/Unsubmitted')

                # Adding members to group: submitted_pc_anon_groups
                client.add_members_to_group(pc_submitted_group, submitted_pc_anon_groups)
                # Removing members from group: submitted_pc_anon_groups
                client.remove_members_from_group(pc_unsubmitted_group, submitted_pc_anon_groups)

def main():
    run(args)

if __name__ == "__main__":
    main()
