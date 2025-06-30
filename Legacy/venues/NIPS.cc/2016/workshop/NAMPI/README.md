<h1>NIPS 2016 Workshop: NAMPI Scripts</h1>

This directory contains scripts for the NAMPI 2016 Workshop use the [OpenReviewPy](https://github.com/iesl/OpenReviewPy) client library. To run these scripts, you must install this library using pip:
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


<h2>get-reviewers.py</h2>
Retrieves the reviewer assignments for the NAMPI 2016 workshops. You may specify a paper number or a user to retrieve assignments for on that particular paper or for that particular user.

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
>> python get-reviewers.py
Paper 1   [BkfmIt0R] mccallum@cs.umass.edu           
Paper 2   [BJnqmRAA] spector@cs.umass.edu            
Paper 3   [Sk6W5JJke] 
Paper 4   [HyiC6J1Je] 
Paper 5   [rJc0or11l] 
```



<h2>invite-reviewers.py</h2>
Accepts a csv file of the format firstname,lastname,email_address and invites them (by email) to the conference.

If a reviewer was already invited, the email will not be sent again.

A total list of reviewers that have accepted the invitation can be found by using the get-groups.py script (in the top level scripts directory of OpenReview-Scripts) or by visiting [http://openreview.net/groups?id=NIPS.cc/2016/workshop/NAMPI/reviewers](http://openreview.net/groups?id=NIPS.cc/2016/workshop/NAMPI/reviewers). Please note that you must be logged in as a user with appropriate permissions (e.g. your program chair account) to view the group by web browser.

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


<h2>assign-reviewers.py</h2>
Retrieves the reviewer assignments for the NAMPI 2016 workshops. You may specify a paper number or a user to retrieve assignments for on that particular paper or for that particular user.

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
>> python assign-reviewers.py spector@cs.umass.edu,1
## assigns spector@cs.umass.edu to be a reviewer for paper 1

>> python assign-reviewers.py nampi-reviewer-assignments.csv
## ingests a csv of the format email,papernumber
```


