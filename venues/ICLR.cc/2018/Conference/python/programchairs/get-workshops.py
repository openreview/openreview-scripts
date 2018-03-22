#!/usr/bin/env python

"""
Dump xlsx file of accepted workshop papers
"""

import argparse
import openreview
import openpyxl
import requests
import datetime
from pdb import set_trace as debug

year = datetime.datetime.now().year

## Argument handling
parser = argparse.ArgumentParser()
parser.add_argument('--baseurl', help="base url")
parser.add_argument('--username')
parser.add_argument('--password')
args = parser.parse_args()

# load in all acceptance decisions
def load_decisions(client):
    decisions = client.get_notes(invitation='ICLR.cc/{0}/Workshop/-/Acceptance_Decision'.format(year))
    dec_info = {decision.forum if decision.content['decision'].startswith('Accept') else None: decision.content['decision'] for decision in decisions}
    return dec_info

def main():
    ## Initialize the client library with username and password
    client = openreview.Client(baseurl=args.baseurl, username=args.username, password=args.password)
    submissions = client.get_notes(invitation='ICLR.cc/{0}/Workshop/-/Submission'.format(year))
    decision_info = load_decisions(client)

    # get all profile information ahead by first listing all authors needed
    authors = set()
    [authors.update(note.content.get("authorids")) for note in submissions if note.forum in decision_info]

    profile_info = {}
    for email in authors:
        print email,
        try:
            pf = client.get_profile(email)
            if type(pf) == type([]):
                debug()
            info = {}
            name = pf.content.get("names")[0]
            info['lastname'] = name.get("last")
            info['firstname'] = name.get("first")
            info['middleinitial'] = name.get("middle")
            preferred_email = pf.content.get("preferred_email")
            info['email'] = preferred_email if preferred_email else email
            history = sorted(pf.content['history'], key = lambda x:x['end'], reverse=True)
            info['institution'] = history[0].get("institution").get("name") if history else u""
            profile_info[email] = info
        except Exception as e:
            print e,
            profile_info[email] = {}
        print

    # Create a workbook and add a worksheet.
    workbook = openpyxl.Workbook()
    worksheet = workbook.active

    worksheet.append(['Unique Id', 'Paper Number', 'Title', 'Keywords', 'Type', 'Date', 'Start Time', 'End Time', 'Abstract',
        'External URL', 'Poster ID', 'Location', 'Author Count', 'Last Name', 'Middle Initial', 'First Name',
        'Email', 'Institution', 'Department', 'Last Name', 'Middle Initial', 'First Name', 'Email', 'Institution',
        'Department'])

    for note in submissions:
        if note.forum in decision_info:
            row = [note.forum, note.number, note.content['title'], None, "Accept(Workshop)", None, None, None, note.content['abstract'],
                note.content['pdf'], None, None, len(note.content['authorids'])]
    
            for author in note.content['authorids']:
                profile = profile_info.get(author)
                if profile:
                    row.extend([profile.get('lastname'), profile.get('middleinitial'), profile.get('firstname'), profile.get('email'), 
                        profile.get('institution'), None])
                else:
                    # skip names
                    try:
                        row.extend([None, None, None, author, None, None])
                    except:
                        debug()
            worksheet.append(row)

    workbook.save('ICLR_workshops.xlsx')

if __name__ == "__main__":
    main()