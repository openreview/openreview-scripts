<h1>NIPS 2016 Workshop: NAMPI Scripts</h1>

This directory contains scripts for NAMPI which use the [OpenReviewPy](https://github.com/iesl/OpenReviewPy) client library. To run these scripts, you must install this library using pip:
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


<h2>get-groups.py</h2>
Retrieves a single group based on id, or multiple groups based on id prefix. It is also capable of adding or removing members to or from the returned group(s). Please note that the specific groups that can be modified in this way are dependent on your OpenReview user permissions.

<h4>Usage</h4>
```
usage: get-groups.py [-h] [-g GROUP] [-p PREFIX] [-o OUTPUT] [-a ADD]
                     [-r REMOVE] [--baseurl BASEURL] [--password PASSWORD]
                     [--username USERNAME]

optional arguments:
  -h, --help            show this help message and exit
  -g GROUP, --group GROUP
                        The group to examine.
  -p PREFIX, --prefix PREFIX
                        The prefix for the set of groups to examine
  -o OUTPUT, --output OUTPUT
                        The directory to save the output file
  -a ADD, --add ADD     a member to add to this group or set of groups
  -r REMOVE, --remove REMOVE
                        a member to remove from this group or set of groups
  --baseurl BASEURL     base url
  --password PASSWORD
  --username USERNAME
```

<h4>Examples</h4>
```
python get-groups.py -g ICLR.cc/2017/conference                             # returns a single group, if available, with id = ICLR.cc/2017/conference
python get-groups.py -p ICLR.cc/2017/conference                             # returns all the groups with ICLR.cc/2017/conference as a prefix

python get-groups.py -p ICLR.cc/2017/conference -o conference.csv           # output groups to the file 'conference.csv'

python get-groups.py -g ICLR.cc/2017/areachairs -a newAC@openreview.net     # add the email address newAC@openreview.net as a member to the areachairs group
```



<h2>get-notes.py</h2>
Retrieves a single note based on forum id or invitation id

<h4>Usage</h4>
```
usage: get-notes.py [-h] [-f FORUM] [-i INVITATION] [-o OUTPUT]
                    [--baseurl BASEURL] [--username USERNAME]
                    [--password PASSWORD]

optional arguments:
  -h, --help            show this help message and exit
  -f FORUM, --forum FORUM
                        The desired note's forum id
  -i INVITATION, --invitation INVITATION
                        the desired note's invitation
  -o OUTPUT, --output OUTPUT
                        The directory to save the output file
  --baseurl BASEURL     base url
  --username USERNAME
  --password PASSWORD
```

<h4>Examples</h4>
```
python get-notes.py -f ABCxyz                                   # returns a list of notes that belong to the forum ABCxyz
python get-notes.py -i ICLR.cc/2017/conference/-/submission     # returns a list of all notes that respond to this invitation (i.e. all paper submissions)
```




<h2>get-reviewers.py</h2>
Retrieves reviewer assignments. 
Given a paper number, it will return that paper's reviewers.
Given a user, it will return the user's assigned papers.
With no arguments, it will return all papers and reviewers for the conference.

<h4>Usage</h4>
```
usage: get-reviewers.py [-h] [-n PAPER_NUMBER] [-u USER] [--baseurl BASEURL]
                        [--username USERNAME] [--password PASSWORD]

optional arguments:
  -h, --help            show this help message and exit
  -n PAPER_NUMBER, --paper_number PAPER_NUMBER
                        the number of the paper to assign this reviewer to
  -u USER, --user USER  the user whose reviewing assignments you would like to
                        see
  --baseurl BASEURL     base url
  --username USERNAME
  --password PASSWORD

```

<h4>Examples</h4>
```
python get-reviewers.py -n 3
python get-reviewers.py -u reviewer@mail.com
python get-reviewers.py
```





<h2>assign-reviewers.py</h2>
Assigns an email address to serve as a reviewer for a particular paper by paper number. The reviewer will be given membership to an anonymous reviewer group (e.g. ICLR.cc/2017/conference/paper123/reviewer1) which allows them to post reviews without revealing their identity.

You may also pass in a CSV file with reviewer/paper_number pairs in the following format:

```
<reviewer_email>,<paper_number>
```
e.g.
```
reviewer1@mail.com,1
reviewer2@mail.com,2
reviewer3@mail.com,3
...
etc.
```
Under normal circumstances, the program chairs and areachairs will be permitted to see the true identity of this anonymous reviewer. However, the anonymous reviewer group will be unreadable by those with a conflict of interest on the paper being reviewed. 

<h4>Usage</h4>
```
usage: assign-reviewers.py [-h] [--baseurl BASEURL] [--username USERNAME]
                           [--password PASSWORD]
                           assignments

positional arguments:
  assignments          either (1) a csv file containing reviewer assignments
                       or (2) a string of the format
                       '<email_address>,<paper#>' e.g.
                       'reviewer@cs.umass.edu,23'

optional arguments:
  -h, --help           show this help message and exit
  --baseurl BASEURL    base url
  --username USERNAME
  --password PASSWORD
```

<h4>Examples</h4>
```
python assign-reviewer.py reviewer1@mail.com,1
python assign-reviewer.py reviewer-assignments.csv
```






<h2>invite-reviewers.py</h2>
Deploys an email to all members of ICLR.cc/2017/conference/reviewers-invited asking whether or not they accept the invitation to serve as a reviewer.

Pass in a csv file to the --reviewers argument to invite reviewers to the workshop. Reviewers that have already been invited will not be emailed twice, so this script may be run multiple times.

<h4>Usage</h4>
```
usage: invite-reviewers.py [-h] [-r REVIEWERS] [--baseurl BASEURL]
                           [--username USERNAME] [--password PASSWORD]

optional arguments:
  -h, --help            show this help message and exit
  -r REVIEWERS, --reviewers REVIEWERS
                        a csv file containing the list of reviewers with rows
                        in the following format:
                        'firstname,lastname,emailaddress'
  --baseurl BASEURL     base URL
  --username USERNAME
  --password PASSWORD
```









