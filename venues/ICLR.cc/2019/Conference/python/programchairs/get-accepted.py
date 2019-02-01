#!/usr/bin/python

"""
Dump csv file of meta-review information to make final decision.
"""
import argparse
import openreview
import xlsxwriter
import requests
import json

## Argument handling
parser = argparse.ArgumentParser()
parser.add_argument('--baseurl', help="base url")
parser.add_argument('--username')
parser.add_argument('--password')
parser.add_argument('--ofile', help="output file name - default to status.csv")
args = parser.parse_args()


# load in all acceptance decisions
def load_decisions(client):
    decisions = openreview.tools.iterget_notes(client, invitation='ICLR.cc/2019/Conference/-/Paper.*/Meta_Review')
    dec_info = {}
    for decision in decisions:
        if decision.content['recommendation'].startswith('Accept'):
            dec_info[decision.forum] = decision.content['recommendation']
    return dec_info

def load_profile(profile_info, author, profile):
    profile_info[author] = {}

    profile_info[author]['first'] = profile.content['names'][0]['first']
    if profile.content['names'][0]['middle'] and len(profile.content['names'][0]['middle']) > 0:
        profile_info[author]['mi'] = profile.content['names'][0]['middle'][0]
    else:
        profile_info[author]['mi'] = " "

    profile_info[author]['last'] = profile.content['names'][0]['last']
    profile_info[author]['email'] = author
    # check for most recent entry in history
    end_date = 0
    profile_info[author]['institute'] = ""
    for entry in profile.content.get('history', []):
        if entry['end'] and entry['end'] > end_date:
            end_date = entry['end']
            profile_info[author]['institute'] = entry['institution']['name']
    return profile_info

def main():
    ## Initialize the client library with username and password
    client = openreview.Client(baseurl=args.baseurl, username=args.username, password=args.password)

    submissions = list(openreview.tools.iterget_notes(client, invitation='ICLR.cc/2019/Conference/-/Blind_Submission'))
    decision_info = load_decisions(client)
    profile_info = {}

    # get all profile information ahead by first listing all authors needed
    authors = []
    for note in submissions:
        if note.forum in decision_info:
            authors.extend(note.content['authorids'])
    # remove duplicates
    authors = list(set(authors))

    # get all associated profiles
    profiles = client.get_profiles(authors)

    for email in profiles:
        author = email
        profile = profiles[email]
        if author not in profile_info:
            profile_info = load_profile(profile_info, author, profile)

    ## Initialize output file name
    file_name = 'ICLR_decisions.xlsx'
    if args.ofile!=None:
        file_name = args.ofile

    # Create a workbook and add a worksheet.
    workbook = xlsxwriter.Workbook(file_name)
    worksheet = workbook.add_worksheet()

    # Start from the first cell. Rows and columns are zero indexed.
    row = 0
    col = 0

    # write the header
    header = ['Unique Id', 'Paper Number', 'Title', 'Decision', 'Abstract', 'Keywords', 'External URL',
            'Author Count', 'Last Name', 'Middle Initial', 'First Name',
              'Email', 'Institution', 'Department', 'Last Name', 'Middle Initial', 'First Name', 'Email', 'Institution',
              'Department']
    for item in header:
        worksheet.write(row, col, item)
        col += 1
    row +=1

    for note in submissions:
        if note.forum in decision_info:
            # paper data
            col = 0
            worksheet.write(row, col, note.forum)
            col += 1
            worksheet.write(row, col, note.number)
            col += 1
            worksheet.write(row, col, note.content['title'])
            col += 1
            worksheet.write(row, col, decision_info[note.forum])
            col += 1
            worksheet.write(row, col, note.content['abstract'])
            col += 1
            worksheet.write(row, col, json.dumps(note.content['keywords']))
            col += 1
            worksheet.write(row, col, note.content['pdf'])
            col += 1
            # author data
            worksheet.write(row, col, len(note.content['authorids']))
            col += 1
            for index, author in enumerate(note.content['authorids']):
                if author not in profile_info:
                    ## A hack to get profiles that are missed by get_profiles
                    try:
                        profile_note = client.get_profile(author)
                        profile = openreview.Profile(content = profile_note.content)
                        profile_info = load_profile(profile_info, author, profile)
                    except openreview.OpenReviewException as e:
                        # cannot find author_id in profile notes
                        e =1
                        name_elements = note.content['authors'][index].split(' ')
                        profile_info[author] = {'first': '', 'mi': '', 'last': ''}
                        profile_info[author]['first'] = name_elements[0]
                        profile_info[author]['last'] = name_elements[-1]
                        profile_info[author]['mi'] = ''
                        profile_info[author]['email'] = author
                        profile_info[author]['institute'] = ''
                        if (len(name_elements) > 2):
                            profile_info[author]['mi'] = ' '.join(name_elements[1:-1])

                if author in profile_info:
                    worksheet.write(row, col, profile_info[author]['last'])
                    col += 1
                    worksheet.write(row, col, profile_info[author]['mi'])
                    col += 1
                    worksheet.write(row, col, profile_info[author]['first'])
                    col += 1
                    worksheet.write(row, col, profile_info[author]['email'])
                    col += 1
                    worksheet.write(row, col, profile_info[author]['institute'])
                    # skipping department
                    col += 2
                else:
                    # skip names
                    col += 3
                    worksheet.write(row, col, author)
                    # skipping institute and department
                    col += 3

            row += 1

    workbook.close()

if __name__ == "__main__":
    main()
