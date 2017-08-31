"""
Demo for ICLR 2018

Instance needs to be set to "secure_activation: false"
"""

import openreview
import config
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--baseurl', help="base URL")
parser.add_argument('--username')
parser.add_argument('--password')

args = parser.parse_args()

client = openreview.Client(baseurl=args.baseurl, username=args.username, password=args.password)

print client.baseurl

client.register_user(email='greenreviewer@openreview.net', first='Green', last='Reviewer', password='1234')
client.register_user(email='bluereviewer@openreview.net', first='Blue', last='Reviewer', password='1234')
client.register_user(email='redreviewer@openreview.net', first='Red', last='Reviewer', password='1234')

client.activate_user('greenreviewer@openreview.net')
client.activate_user('bluereviewer@openreview.net')
client.activate_user('redreviewer@openreview.net')

client.register_user(email='redauthor@openreview.net', first='Red', last='Author', password='1234')
client.register_user(email='blueauthor@openreview.net', first='Blue', last='Author', password='1234')
client.register_user(email='greenauthor@openreview.net', first='Green', last='Author', password='1234')

client.register_user(email='author@openreview.net', first='Jane', last='Doe', password='1234')

client.activate_user('blueauthor@openreview.net')
client.activate_user('redauthor@openreview.net')
client.activate_user('greenauthor@openreview.net')

client.activate_user('author@openreview.net')

client.register_user(email='programchair@openreview.net', first='Program', last='Chair', password='1234')
client.register_user(email='areachair@openreview.net', first='Area', last='Chair', password='1234')

client.activate_user('programchair@openreview.net')
client.activate_user('areachair@openreview.net')

iclr2017papers = client.get_notes(invitation='ICLR.cc/2017/conference/-/submission')


def get_iclr_paper(iclr17_note):

    author_signature = "~Jane_Doe1"
    author_id = "author@openreview.net"

    note_readers = [
        "ICLR.cc/2018/Conference",
        "ICLR.cc/2018/Conference/Program_Chairs",
        author_id,
        author_signature
    ]

    note_signatures = [author_signature]

    return openreview.Note(**{
        "readers": note_readers,
        "nonreaders": [],
        "signatures": note_signatures,
        "writers": [],
        "invitation": "ICLR.cc/2018/Conference/-/Submission",
        "content": {
            'title': iclr17_note.content['title'],
            'abstract': iclr17_note.content['abstract'],
            'authors': iclr17_note.content['authors'],
            'keywords': iclr17_note.content['keywords'],
            'TL;DR': iclr17_note.content['TL;DR'],
            'authorids': [author_id],
            'pdf': iclr17_note.content['pdf']
        }
    })

def get_color_paper(color):
    author_signature = "~Jane_Doe1"
    author_id = "author@openreview.net"

    note_readers = [
        "ICLR.cc/2018/Conference",
        "ICLR.cc/2018/Conference/Program_Chairs",
        author_id,
        author_signature
    ]

    note_signatures = [author_signature]

    return openreview.Note(**{
        "readers": note_readers,
        "nonreaders": [],
        "signatures": note_signatures,
        "writers": [],
        "invitation": "ICLR.cc/2018/Conference/-/Submission",
        "content": {
            'title': '{0} Paper'.format(color),
            'abstract': 'This is the {0} abstract.'.format(color),
            'authors': '{0} authors'.format(color),
            'keywords': color,
            'TL;DR': 'This is the {0} TL;DR'.format(color),
            'authorids': [author_id],
            'pdf': "/pdf/813abccc0d09f502de96bbdca811a42e5ac59a2a.pdf"
        }
    })

def get_tag(signature, forum):
    return openreview.Tag(**{
        "tag": "I want to review",
        "forum": forum,
        "invitation": "ICLR.cc/2018/Conference/-/Add_Bid",
        "signatures": [
            signature
        ],
        "nonreaders": [],
        "readers": [
            signature,
            "ICLR.cc/2018/Conference"
        ],
    })

for n in iclr2017papers[0:10]:
    print "posting ICLR paper: ", n.content['title'], n.content['pdf']
    client.post_note(get_iclr_paper(n))


reviewers = client.get_group('ICLR.cc/2018/Conference/Reviewers')
client.remove_members_from_group(reviewers, reviewers.members)
client.add_members_to_group(reviewers, ['~Red_Reviewer1', '~Blue_Reviewer1', '~Green_Reviewer1'])

reviewers_invited = client.get_group('ICLR.cc/2018/Conference/Reviewers/Invited')
client.remove_members_from_group(reviewers_invited, reviewers_invited.members)
client.add_members_to_group(reviewers_invited, ['~Red_Reviewer1', '~Blue_Reviewer1', '~Green_Reviewer1'])

reviewers_emailed = client.get_group('ICLR.cc/2018/Conference/Reviewers/Emailed')
client.remove_members_from_group(reviewers_emailed, reviewers_emailed.members)
client.add_members_to_group(reviewers_emailed, ['~Red_Reviewer1', '~Blue_Reviewer1', '~Green_Reviewer1'])

areachairs = client.get_group('ICLR.cc/2018/Conference/Area_Chairs')
client.remove_members_from_group(areachairs, areachairs.members)
client.add_members_to_group(areachairs, ['~Area_Chair1'])

programchairs = client.get_group('ICLR.cc/2018/Conference/Program_Chairs')
client.remove_members_from_group(programchairs, programchairs.members)
client.add_members_to_group(programchairs, ['~Program_Chair1'])

red_note = client.post_note(get_color_paper('Red'))
blue_note = client.post_note(get_color_paper('Blue'))
green_note = client.post_note(get_color_paper('Green'))

papers = client.get_notes(invitation=config.BLIND_SUBMISSION)

id_by_original = {n.original: n.id for n in papers}

red_tag = client.post_tag(get_tag("~Red_Reviewer1", id_by_original[red_note.id]))
blue_tag = client.post_tag(get_tag("~Blue_Reviewer1", id_by_original[blue_note.id]))
green_tag = client.post_tag(get_tag("~Green_Reviewer1", id_by_original[green_note.id]))

for n in papers:
    ac = client.get_group('ICLR.cc/2018/Conference/Paper{0}/Area_Chair'.format(n.number))
    client.add_members_to_group(ac, '~Area_Chair1')


