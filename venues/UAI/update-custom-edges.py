import argparse
import openreview
from tqdm import tqdm


"""
OPTIONAL SCRIPT ARGUMENTS

    baseurl -  the URL of the OpenReview server to connect to (live site: https://openreview.net)
    username - the email address of the logging in user
    password - the user's password

"""
parser = argparse.ArgumentParser()
parser.add_argument('--baseurl', help="base URL")
parser.add_argument('--username')
parser.add_argument('--password')
args = parser.parse_args()
client = openreview.Client(baseurl=args.baseurl, username=args.username, password=args.password)

edges_a = list(openreview.tools.iterget_edges(client, invitation = 'auai.org/UAI/2022/Conference/Reviewers/-/Conflict', label = 'exp conflict paper(B) reviewer(A)'))
edges_b = list(openreview.tools.iterget_edges(client, invitation = 'auai.org/UAI/2022/Conference/Reviewers/-/Conflict', label = 'exp conflict paper(A) reviewer(B)'))

ac_id = 'auai.org/UAI/2022/Conference/Area_Chairs'
confid = 'auai.org/UAI/2022/Conference'

for edge in tqdm(edges_a):
    edge.readers = [edge.tail, ac_id, confid]
    client.post_edge(edge)
for edge in tqdm(edges_b):
    edge.readers = [edge.tail, ac_id, confid]
    client.post_edge(edge)
