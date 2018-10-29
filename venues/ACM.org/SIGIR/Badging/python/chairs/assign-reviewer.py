## Import statements
import argparse
import openreview
import re

'''
Requirements:

openreview-py (version 0.9.6 and above)

Usage:

Use the --forum (or -f) flag to specify the paper forum.
Use the --add (or -a) flag to specify an openreview username or an email address to assign.
Use the --remove (or -r) flag to specify an openreview username or an email address to remove.

For example, after running the following:
python assign-reviewer.py --forum "H1g2gTJZ2Q" --remove "muniyal@cs.umass.edu" --add "mspector@cs.umass.edu"


ACM.org/SIGIR/Badging/-/Paper5/Review -> Invitees = ['muniyal@cs.umass.edu']
becomes
ACM.org/SIGIR/Badging/-/Paper5/Review -> Invitees = ['mspector@cs.umass.edu']

You can also just remove or just add reviewers. Examples:
python assign-reviewer.py --forum H1g2gTJZ2Q --remove mspector@cs.umass.edu
python assign-reviewer.py --forum H1g2gTJZ2Q --add muniyal@cs.umass.edu
'''

if __name__ == "__main__":
    ## Argument handling
    parser = argparse.ArgumentParser()
    parser.add_argument('-f','--forum', required=True)
    parser.add_argument('-a','--add')
    parser.add_argument('-r','--remove')
    parser.add_argument('--baseurl', help="base url")
    parser.add_argument('--username')
    parser.add_argument('--password')

    args = parser.parse_args()

    client = openreview.Client(baseurl=args.baseurl, username=args.username, password=args.password)

    paper_forum = args.forum
    reviewer_to_remove = args.remove
    reviewer_to_add = args.add

    conference = 'ACM.org/SIGIR/Badging'
    
    try:
        paper_number = client.get_note(paper_forum).number
    except Exception:
        print ("Cound not find the forum {}".format(paper_forum))
        print ("Exiting!")
        exit()
    
    if not (reviewer_to_add ) and not (reviewer_to_remove):
        paper_review_invitation = client.get_invitation(id = conference + "/-/Paper{}".format(paper_number)+"/Review")
        print ("\n\nReviewers for forum {} are \n{}\n".format(paper_forum,paper_review_invitation.invitees))

    if reviewer_to_remove :
        if '@' in reviewer_to_remove:
            reviewer_to_remove = reviewer_to_remove.lower()

        paper_review_invitation = client.get_invitation(id = conference + "/-/Paper{}".format(paper_number)+"/Review")
        invitees = paper_review_invitation.invitees
        if reviewer_to_remove in invitees:
            invitees.remove(reviewer_to_remove)
            paper_review_invitation.invitees = list(set(invitees))
            updated_invitation = client.post_invitation(paper_review_invitation)
            print("\n\n{:40s} removed as a reviewer for forum {}\n".format(reviewer_to_remove, paper_forum))
        else:
            print ("\n\n{:40s} is already not a reviewer for forum {}\n".format(reviewer_to_remove, paper_forum))

    if reviewer_to_add :
        if '@' in reviewer_to_add:
            reviewer_to_add = reviewer_to_add.lower()
        
        paper_review_invitation = client.get_invitation(id = conference + "/-/Paper{}".format(paper_number)+"/Review")
        invitees = paper_review_invitation.invitees
        if invitees and reviewer_to_add in invitees:
            print ("\n\n{:40s} is already a reviewer for forum {}\n".format(reviewer_to_add, paper_forum))
        else:
            invitees.append(reviewer_to_add)
            paper_review_invitation.invitees = list(set(invitees))
            updated_invitation = client.post_invitation(paper_review_invitation)
            print("\n\n{:40s} added as a reviewer for forum {}\n".format(str(reviewer_to_add), paper_forum))
