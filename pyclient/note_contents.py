###############################################################################
# Note dump python script will simply print the contents of papers/reviews/
# comments matching certain criteria. PCs can run this as they wish to inspect 
# the system.
###############################################################################

# This script depends on being able to search by prefix

import sys
import client
import requests

username = sys.argv[1]
password = sys.argv[2]
input_invitation = sys.argv[3]

## Initialize the client library with username and password
or3 = client.client(username, password)

notes = requests.get(or3.notesUrl, params={'invitation':input_invitation}, headers=or3.headers)

or3.printPrettyNote(notes)