<h1>ICLR 2017 Scripts</h1>

This directory contains scripts for ICLR 2017 use the [OpenReviewPy](https://github.com/iesl/OpenReviewPy) client library. To run these scripts, you must install this library using pip:
```
pip install OpenReviewPy
```
The scripts make use of OpenReviewPy's Client class, which requires an OpenReview username and password. To avoid the need for the user to enter his/her credentials every time they run a script, the Client uses the environment variables OPENREVIEW_USERNAME, OPENREVIEW_PASSWORD, and OPENREVIEW_BASEURL. 

To set these environment variables, either enter the following lines in the bash terminal that you will use to run the scripts, or insert them into your ~/.bash_profile (on OS X) or ~/.bashrc (on linux):
```
export OPENREVIEW_USERNAME="username@gmail.com"
export OPENREVIEW_PASSWORD="password"
export OPENREVIEW_BASEURL="http://dev.openreview.net"
```
You may also enter these commands in the bash shell that you will use to execute these scripts.

If you do not set values for OPENREVIEW_USERNAME or OPENREVIEW_PASSWORD, you will be prompted for the missing credentials each time the Client is initialized (at the beginning of each script).


<h2>Descriptions of scripts</h2>

<h3>setup-invitations.py</h3>
Initializes the invitation to submit a paper to the conference and the process functions that trigger when a submission is made. Intended to be executed by a member of ICLR.cc/2017/pcs.

<h4>Examples</h4>
```
python setup-invitations.py
```


<h3>groups.py</h3>
Retrieves a single group based on id, or multiple groups based on id prefix. It is also capable of adding or removing members to or from the returned group(s). Please note that the specific groups that can be modified in this way are dependent on your OpenReview user permissions.

<h4>Examples</h4>
```
python groups.py -g ICLR.cc/2017/conference                             # returns a single group, if available, with id = ICLR.cc/2017/conference
python groups.py -p ICLR.cc/2017/conference                             # returns all the notes with ICLR.cc/2017/conference as a prefix

python groups.py -p ICLR.cc/2017/conference -o conference.csv           # output files to csv

python groups.py -g ICLR.cc/2017/areachairs -a newAC@openreview.net     # add the email address newAC@openreview.net to the areachairs group
```

<h3>notes.py</h3>
Retrieves a single note based on forum id or invitation id

<h4>Examples</h4>
```
python notes.py -f ABCxyz                                   # returns a list of notes that belong to the forum ABCxyz
python notes.py -i ICLR.cc/2017/conference/-/submission     # returns a list of all notes that respond to this invitation (i.e. all paper submissions)
```

<h3>homepage.py</h3>
Replaces a given group's webfield (for groups that represent conferences, workshops, or symposia, the webfield contains the html file that controls how the group is displayed in the UI)

<h4>Examples</h4>
```
python homepage.py ICLR.cc/2017/conference ../webfield/iclr2017conference_webfield.html     # replaces the current webfield of ICLR.cc/2017/conference with iclr2017conference_webfield.html
```

<h3>email-reviewers.py</h3>
Sends an email to the group of your choice. Intended for sending a message to reviewers, the default values are as follows:

```
Recipients: NONE

Subject: A message to reviewers

Message:
Dear invited reviewer,

Thank you for deciding to participate as a reviewer for ICLR 2017! 
You will be notified of further instructions shortly.

Sincerely,
the ICLR 2017 program chairs

```

Defaults may be changed with optional arguments to the script.

<h4>Examples</h4>
```
python email-reviewers.py --message "this is my new message"
python email-reviewers.py --recipients ICLR.cc/2017/conference/reviewers-invited
python email-reviewers.py --subject "This is a new subject line"
```

<h3>invite-reviewer.py</h3>
Allows PCs to invite an additional individual reviewer, taking a single email address as argument.  The script will add the email address to the reviewers-invited group, and send an invitation email to the person.

<h4>Examples</h4>
```
python invite-reviewer.py potentialreviewer@gmail.com       # sends an email to potentialreviewer@gmail.com and invites him/her to indicate his/her acceptance.
```

The reviewer will recieve the following email:
```
Recipients: potentialreviewer@gmail.com

Subject: OpenReview invitation response

Message:
You have been invited to serve as a reviewer for the International Conference on Learning Representations (ICLR) 2017 Conference.

To ACCEPT the invitation, please click on the following link:
    
(URL to accept invitation)

To DECLINE the invitation, please click on the following link:

(URL to decline invitation)

Thank you,
The ICLR 2017 Program Chairs
```

This message may be modified directly in the script.

<h3>assign-reviewer.py</h3>
Assigns an email address to serve as a reviewer for a particular paper by paper number (NOTE: paper number is an integer assigned to each paper in the order it was submitted, starting from 1. This is different from the forum ID, which is a six-digit sequence of letters, numbers, and symbols). The reviewer will be given membership to an anonymous reviewer group (e.g. ICLR.cc/2017/conference/paper123/reviewer1) which allows them to post reviews without revealing their identity.

<h4>Examples</h4>
```
python assign-reviewer.py assignedreviewer@openreview.net 1         # assigns assignedreviewer@openreview.net to be a reviewer for paper 1   
```


