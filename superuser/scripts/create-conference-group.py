import argparse
import openreview

def build_groups(conference_group_id):
    '''
    Generates the conference group and its ancestors.
    Also generates the conference Admin group.
    '''

    # create list of subpaths (e.g. Test.com, Test.com/TestConference, Test.com/TestConference/2018)
    path_components = conference_group_id.split('/')
    paths = ['/'.join(path_components[0:index+1]) for index, path in enumerate(path_components)]

    empty_params = {
        'readers': ['everyone'],
        'writers': [],
        'signatures': [],
        'signatories': [],
        'members': []
    }

    groups = {p: openreview.Group(p, **empty_params) for p in paths}
    groups[conference_group_id].writers = groups[conference_group_id].signatories = [conference_group_id]

    admin_id = conference_group_id + '/Admin'
    groups[admin_id] = openreview.Group(admin_id, readers=[admin_id], signatories=[admin_id])

    return groups

parser = argparse.ArgumentParser()
parser.add_argument('-v', '--venue', required=True, help = "the full path of the conference group to create.")
parser.add_argument('--overwrite', action='store_true', help="if true, overwrites the conference directory.")
parser.add_argument('--baseurl')
parser.add_argument('--username')
parser.add_argument('--password')
args = parser.parse_args()

client = openreview.Client(baseurl=args.baseurl, username=args.username, password=args.password)
conference_group_id = args.venue

groups = build_groups(conference_group_id)

for g in sorted([g for g in groups]):
    print "posting group {0}".format(g)
    client.post_group(groups[g])

# add admin group to the conference members
client.add_members_to_group(groups[conference_group_id], conference_group_id + '/Admin')
