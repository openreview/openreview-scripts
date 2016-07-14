###############################################################################
# Group dump python script will simply print the contents of any given group.  
# PCs can run this as they wish to inspect the system.
###############################################################################

import sys
import client
import requests

username = sys.argv[1]
password = sys.argv[2]
input_group = sys.argv[3]

## Initialize the client library with username and password
or3 = client.client(username, password)

group = requests.get(or3.grpUrl, params={'id':input_group}, headers=or3.headers)

or3.printPrettyNote(group)