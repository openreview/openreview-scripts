## Import statements
import argparse
import openreview
import re

'''
Requirements: 

Python3
openreview-py (version 0.9.6 and above)

Inputs to the script:

Use the --forum (or -f) flag to specify the paper forum. Forum is mandatory.
Use the --add (or -a) flag to specify an openreview username or an email address to assign.
Use the --remove (or -r) flag to specify an openreview username or an email address to remove.

The script uses forum as an input which represents a submission. You can retrieve the forum of a submission like this:
1. Open ACM SIGIR Badging page - https://dev.openreview.net/group?id=ACM.org/SIGIR/Badging
2. Click on the submission you want to modify reviewers for. 
3. Forum id is present in the url. E.g. https://dev.openreview.net/forum?id=H1xhIohNn7 has the forum id “H1xhIohNn7”.

Usage: 

>>> python assign-reviewer.py --baseurl https://dev.openreview.net --username chair@acmtest.org  --password 1234 --forum H1g2gTJZ2Q --remove muniyal@cs.umass.edu --add mspector@cs.umass.edu

Results in removal of 'muniyal@cs.umass.edu’ as a reviewer and addition of 'mspector@cs.umass.edu’ as a reviewer.

You can also just remove or just add reviewers. Examples:
>>> python assign-reviewer.py --baseurl https://dev.openreview.net --username chair@acmtest.org  --password 1234 -f H1g2gTJZ2Q -r mspector@cs.umass.edu
>>> python assign-reviewer.py --baseurl https://dev.openreview.net --username chair@acmtest.org  --password 1234 -f H1g2gTJZ2Q -a muniyal@cs.umass.edu


Also, if both --add or --remove flags are not provided, then the script prints the existing reviewers for the given forum id.
For example: 
>>> python assign-reviewer.py --baseurl https://dev.openreview.net --username chair@acmtest.org  --password 1234 -f H1xhIohNn7

Output: 
Reviewers for forum H1xhIohNn7 are
['~srreviewer_acm1', 'mspector@cs.umass.edu']
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
