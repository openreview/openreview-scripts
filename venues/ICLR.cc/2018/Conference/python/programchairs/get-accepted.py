#!/usr/bin/python

"""
Dump csv file of meta-review information to make final decision.
"""
import argparse
import openreview
import xlsxwriter
import requests
import json
from pdb import set_trace as debug

## Argument handling
parser = argparse.ArgumentParser()
parser.add_argument('--baseurl', help="base url")
parser.add_argument('--username')
parser.add_argument('--password')
parser.add_argument('--ofile', help="output file name - default to status.csv")
args = parser.parse_args()


# load in all acceptance decisions
def load_decisions(client):
    decisions = client.get_notes(invitation='ICLR.cc/2018/Conference/-/Acceptance_Decision')
    dec_info = {}
    for decision in decisions:
        if decision.content['decision'].startswith('Accept'):
            dec_info[decision.forum] = decision.content['decision']
    return dec_info


def main():
    ## Initialize the client library with username and password
    client = openreview.Client(baseurl=args.baseurl, username=args.username, password=args.password)

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
    header = ['Unique Id','Paper Number','Title', 'Keywords', 'Type', 'Date', 'Start Time', 'End Time', 'PosterDate AMPM', 'Session','Abstract', 'External URL','Poster ID','Location','Author Count','Last Name', 'Middle Initial', 'First Name', 'Email','Institution', 'Department','Last Name', 'Middle Initial', 'First Name', 'Email','Institution', 'Department']
    for item in header:
        worksheet.write(row, col, item)
        col += 1
    row +=1

    submissions = client.get_notes(invitation='ICLR.cc/2018/Conference/-/Blind_Submission')
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
    response = requests.post(client.baseurl + '/user/profiles', json={'emails': authors})

    profiles = response.json()
    profiles = profiles['profiles']
    for item in profiles:
        author = item['email']
        profile = item['profile']
        if author not in profile_info:
            profile_info[author] = {}
            profile_info[author]['first'] = profile['content']['names'][0]['first']
            if len(profile['content']['names'][0]['middle']) > 0:
                profile_info[author]['mi'] = profile['content']['names'][0]['middle'][0]
            else:
                profile_info[author]['mi'] = " "

            profile_info[author]['last'] = profile['content']['names'][0]['last']
            # if preferred email isn't set, use email from form
            if profile['content']['preferred_email'] != "":
                profile_info[author]['email'] = profile['content']['preferred_email']
            else:
                profile_info[author]['email'] = author
            # check for most recent entry in history
            end_date = 0
            profile_info[author]['institute'] = ""
            for entry in profile['content']['history']:
                if entry['end'] > end_date:
                    end_date = entry['end']
                    profile_info[author]['institute'] = entry['institution']['name']

    for note in submissions:
        if note.forum in decision_info:
            print note.number
            # paper data
            col = 0
            worksheet.write(row, col, note.forum)
            col += 1
            worksheet.write(row, col, note.number)
            col += 1
            worksheet.write(row, col, note.content['title'])
            col += 1
            worksheet.write(row, col, json.dumps(note.content['keywords']))
            col += 1
            worksheet.write(row, col, decision_info[note.forum].replace(u"Accept (", u"" ).replace(u")", u""))
            # skipping Date, StartTime, EndTime, PosterAMPM and session
            #['uniqueid', "sourceid", "title", "keywords", "type", "date", "startime", 'endtime', "PosterDate_AMPM", "session", "abstract", "pdfuri", "location"]
            col += 4
            worksheet.write(row, col, note.content['abstract'])
            col += 1
            worksheet.write(row, col, note.content['pdf'])
            # skipping PosterID, Location
            col += 3
            # author data
            worksheet.write(row, col, len(note.content['authorids']))
            col += 1
            for author in note.content['authorids']:
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
