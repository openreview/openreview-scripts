#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Email decisions to paper authors
"""

## Import statements
import argparse
import csv
import openreview

## Handle the arguments
parser = argparse.ArgumentParser()
parser.add_argument('--baseurl', help="base URL")
parser.add_argument('--username')
parser.add_argument('--password')
parser.add_argument('--ifile')
args = parser.parse_args()

## Initialize the client library with username and password
client = openreview.Client(baseurl=args.baseurl, username=args.username, password=args.password)

def load_decisions(client):
    decisions = client.get_notes(invitation='ICLR.cc/2018/Conference/-/Acceptance_Decision')
    print len(decisions)
    dec_info = {}
    for decision in decisions:
        dec_info[decision.forum] =decision.content['decision']
    return dec_info

def load_file():
    csv_info = []
    if args.ifile:
        with open(args.ifile) as f:
            reader = csv.reader(f)
            csv_info = [r[0] for r in reader]
    print csv_info
    return csv_info



subjects = {}
subjects['Accept (Oral)'] = "ICLR 2018 conference track: final decision - oral"
subjects['Accept (Poster)'] = "ICLR 2018 conference track: final decision - poster"
subjects['Invite to Workshop Track'] = "ICLR 2018 conference track: final decision - invite to Workshop Track"
subjects['Reject'] = "ICLR 2018 conference track: final decision - rejection"

messages = {}
messages['Accept (Oral)'] = """Dear Author,

We are very pleased to inform you that your ICLR 2018 submission to the Conference Track
{0} - {1}
has been accepted to the Conference Track as an oral presentation.

Note that your paper will also have to be presented at one of our poster sessions, we will provide details about poster sessions and poster formats soon.

You should now prepare the de-anonymized camera ready version of your contribution, which should include inserting the statement \iclrfinalcopy in your LaTeX source file.

We ask that you update your paper on OpenReview with this latest version no later than February 23th, 2018.

https://openreview.net/group?id=ICLR.cc/2018/Conference

Please don't forget to make your travel arrangements. Registration for the conference will open on February 1, 2018, and you can register directly through the conference website https://iclr.cc/. There, you will also find suggestions for local accommodation.

Note that at least one author for each paper must be registered for ICLR 2018.

We received 935 Conference Track submissions -- up from 430 last year! Out of these we accepted only 23 conference submissions for oral presentation (2%) and  314 conference submissions for poster presentation in the Conference Track (34%).

Congratulations and thank you for your contribution.

We look forward to seeing you Vancouver, Canada!

Tara, Marc’Aurelio, Iain and Oriol -- the ICLR 2018 program committee
"""

messages['Accept (Poster)'] = """Dear Author,

We are pleased to inform you that your ICLR 2018 submission to the Conference Track
{0} - {1}
has been accepted to the Conference Track as a poster presentation.

You should now prepare the deanonymised camera ready version of your contribution, which should include inserting the statement \iclrfinalcopy in your LaTeX source file.

We ask that you update your paper on OpenReview with this latest version no later than February 23th, 2018.

https://openreview.net/group?id=ICLR.cc/2018/Conference

Please don't forget to make your travel arrangements. Registration for the conference will open on February 1, 2018, and you can register directly through the conference website https://iclr.cc/. There, you will also find suggestions for local accommodation.

Note that at least one author for each paper must be registered for ICLR 2017.

We received 935 Conference Track submissions -- up from 430 last year! Out of these we accepted only 23 conference submissions for oral presentation (2%) and  314 conference submissions for poster presentation in the Conference Track (34%).

Congratulations and thank you for your contribution.

We look forward to seeing you Vancouver, Canada!

Tara, Marc’Aurelio, Iain and Oriol -- the ICLR 2018 program committee
"""

messages['Invite to Workshop Track'] = """Dear Author,

We are writing to inform you that your ICLR 2018 submission to the Conference Track
{0} - {1}
was not accepted to the Conference Track. However, we'd be happy to have you present this work as a poster in the ICLR 2018 Workshop Track.

If you do not wish to present in the ICLR 2018 Workshop Track, you have nothing to do (converting to a workshop contribution is "opt-in").

But if you do (as we hope!), you should prepare a de-anonymized camera ready version of your contribution that uses the style file for Workshop Track papers, available here:
https://media.nips.cc/Conferences/ICLR2018/iclr_workshop_2018.zip
Simply, update the file style file (the top of the first page should state that your paper is a workshop contribution). There is no need to further reformat your paper; in particular, you do not need to (unless you want to) satisfy the 3 page length requirement. Your paper will not go under further review and it will be automatically accepted at the Workshop Track.

We will be accepting Workshop Track contributions until February 12th, 2018, 5PM EST. Papers can be submitted via OpenReview at:
https://openreview.net/group?id=ICLR.cc/2018/Workshop

Please don't forget to make your travel arrangements. Registration for the conference will open on February 1, 2018, and you can register directly through the conference website https://iclr.cc/. There, you will also find suggestions for local accommodation.

Note that at least one author for each paper must be registered for ICLR 2018.

We received 935 Conference Track submissions -- up from 430 last year! Out of these we accepted only 23 conference submissions for oral presentation (2%) and  314 conference submissions for poster presentation in the Conference Track (34%).

Thank you for your contribution. We look forward to seeing you Vancouver, Canada!

Tara, Marc’Aurelio, Iain and Oriol -- the ICLR 2018 program committee
"""
messages['Reject'] = """Dear Author,

We are writing to inform you that your ICLR 2018 submission
{0} - {1}
was not accepted.

We received 935 Conference Track submissions -- up from 430 last year! Out of these we accepted only 23 conference submissions for oral presentation (2%) and  314 conference submissions for poster presentation in the Conference Track (34%).

Thank you for your interest in the conference, and we hope you'll nevertheless consider joining us in Vancouver, Canada.

Tara, Marc’Aurelio, Iain and Oriol -- the ICLR 2018 program committee
"""


submissions = client.get_notes(invitation='ICLR.cc/2018/Conference/-/Blind_Submission')
decision_info = load_decisions(client)
csv_info = load_file()
subject = "ICLR decision"
for note in submissions:
    if note.forum in decision_info and note.forum not in csv_info:
        if decision_info[note.forum] in messages:
            message = messages[decision_info[note.forum]].format(note.number, note.content['title'].encode('utf-8'))
            client.send_mail(subjects[decision_info[note.forum]], note.content['authorids'], message)

            print note.forum
        else:
            print "ERROR Decision: <" + {0} + "> for paper {1}".format(decision_info[note.forum], note.number)