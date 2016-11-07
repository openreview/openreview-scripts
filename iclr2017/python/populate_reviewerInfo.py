from time import sleep
import datetime
import time
import openreview
import dblp
import inspect
import json
import os

# reviewersInfo = {}
# initializing openreview_client to post notes.
username = 'OpenReview.net' #fill in your email address that you use to log in to OpenReview
password = '1234567890' #fill in your password
baseurl  = 'http://localhost:3000' #fill in your desired baseurl (e.g. 'http://localhost:3000', or 'http://dev.openreview.net', etc.)

openreview_client = openreview.Client(username=username, password=password, baseurl=baseurl)
# reading the reviewer info from csv file and obtaining information about the user
fp = open("./iclr_accepted_reviewers.csv")
no_name = 0
more_than_one = 0
no_hits = 0
no_match = 0
no_pub = 0
author_disambiguation = {}
no_hits_names = []
no_name_list = []
no_matched_author = []
no_pub_list = []
notes_count = 0

for eachLine in fp.readlines():
    emailId, firstName, lastName = eachLine.split(',')
    name = firstName + " " + lastName.strip()
    file_name = firstName + "_" + lastName.strip()

    if name == '' or name == ' ':
        print emailId
        no_name += 1
        no_name_list.append(emailId)
    else:
        try:
            authors = dblp.search(name)
        except Exception as e:
            sleep(2)
            authors = dblp.search(name)
        if authors:
            if len(authors) > 1:
                print "More than one authors found! "
                more_than_one += 1
                author_disambiguation[name] = []
                author = None
                for ath in authors:
                    author_disambiguation[name].append(ath.name)
                    if name.lower() == ath.name.lower():
                        author = ath
                if not author:
                    no_matched_author.append(name)
                    print "No perfect match found for: ", name
                    print author_disambiguation[name]
                    no_match += 1
                if author and len(author.publications) == 0:
                    print "No publications found for ", name
                    no_pub += 1
                    no_pub_list.append(name)
                    continue
                if author and len(author.publications) > 0:
                    print len(author.publications)
                    publications_set = set()
                    for publication in author.publications:
                        try:
                            pub_title = publication.title
                        except Exception as e:
                            sleep(2)
                            pub_title = publication.title
                        if pub_title in publications_set:
                            continue
                        note = openreview.Note()
                        publications_set.add(pub_title)
                        ath_ids = []
                        for ath_name in publication.authors:
                            if ath_name.lower() == author.name.lower():
                                ath_ids.append(emailId)
                            else:
                                ath_ids.append('_')
                        note.content = {
                            'abstract': '',
                                       'school': publication.school ,
                                       'publisher':publication.publisher ,
                                       'chapter': publication.chapter,
                                       'crossref': publication.crossref,
                                       'pages': publication.pages,
                                       'volume': publication.volume,
                                       'journal': publication.journal,
                                       'type': publication.type,
                                       'sub_type': publication.sub_type,
                                       'editors': ','.join(publication.editors),
                                       'booktitle': publication.booktitle,
                                       'year': publication.year,
                                       'month': publication.month,
                                       'mag_number': publication.number,
                                       'series': publication.series,
                                       'electronic_edition': publication.ee,
                                       'isbn': publication.isbn,
                                       'DBLP_url': 'publication.url',
                                       'authorids': ath_ids,
                                       'authors': publication.authors,
                                       'title': publication.title,
                        }
                        note.invitation = 'DBLP.org/-/paper'
                        note.signatures = ['DBLP.org/upload']
                        note.writers = note.signatures
                        note.readers = ['everyone']
                        # creating a timestamp for cdate
                        if publication.year:
                            dt_obj = datetime.datetime(month=01, day=01,
                                                       year=publication.year)
                            timestamp_obj = int(time.mktime(dt_obj.timetuple()))
                        else:
                            # if the year is not mentioned then cdate = None
                            timestamp_obj = None
                        note.cdate = timestamp_obj
                        note.to_json()
                        try:
                            openreview_client.post_note(note)
                            notes_count += 1
                        except Exception as e:
                            print "EXCEPTION !!", e

            else:
                author = authors[0]
                if len(author.publications) == 0:
                    print "No publications found for ", name
                    no_pub += 1
                    no_pub_list.append(name)
                if len(author.publications) > 0:
                    print len(author.publications)
                    publications_set = set()
                    for publication in author.publications:
                        try:
                            pub_title = publication.title
                        except Exception as e:
                            sleep(2)
                            pub_title = publication.title
                        if pub_title in publications_set:
                            continue
                        note = openreview.Note()
                        publications_set.add(pub_title)
                        ath_ids = []
                        for ath_name in publication.authors:
                            if ath_name.lower() == author.name.lower():
                                ath_ids.append(emailId)
                            else:
                                ath_ids.append('_')

                        note.content = {
                            'abstract': '',
                            'school': publication.school,
                            'publisher': publication.publisher,
                            'chapter': publication.chapter,
                            'crossref': publication.crossref,
                            'pages': publication.pages,
                            'volume': publication.volume,
                            'journal': publication.journal,
                            'type': publication.type,
                            'sub_type': publication.sub_type,
                            'editors': ','.join(publication.editors),
                            'booktitle': publication.booktitle,
                            'year': publication.year,
                            'month': publication.month,
                            'mag_number': publication.number,
                            'series': publication.series,
                            'electronic_edition': publication.ee,
                            'isbn': publication.isbn,
                            'DBLP_url': 'publication.url',
                            'authorids': ath_ids,
                            'authors': publication.authors,
                            'title': publication.title,
                        }
                        note.invitation = 'DBLP.org/-/paper'
                        note.signatures = ['DBLP.org/upload']
                        note.writers = note.signatures
                        note.readers = ['everyone']
                        # creating a timestamp for cdate
                        if publication.year:
                            dt_obj = datetime.datetime(month=01,day=01,year=publication.year)
                            timestamp_obj = int(time.mktime(dt_obj.timetuple()))
                        else:
                            # if the year is not mentioned then cdate = None
                            timestamp_obj = None
                        note.cdate = timestamp_obj
                        note.to_json()
                        try:
                            openreview_client.post_note(note)
                            notes_count += 1
                        except Exception as e:
                            print "EXCEPTION !!", e
                        # for title in publications_set:
                        #     title = unicode(title).encode('utf-8')
        else:
            print "No hit in dblp for ", name
            no_hits_names.append(name)
            no_hits += 1

print "Stats: "
print "No names for: ", no_name
print "No names list: ", no_name_list
print "More than 1 author hits for ", more_than_one
print "No hits for ", no_hits
print "No hit list: ", no_hits_names
print "No matches count ", no_match
print "No matches list", no_matched_author
print "No publications: ", no_pub
print "No publications list: ", no_pub_list
print "No. of notes created are: ", notes_count
