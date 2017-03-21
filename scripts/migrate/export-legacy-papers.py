# mcz 3/2017
# Migrate legacy OpenReview data (stored in a mongo DB) to current OR.
# This requires the pyMongo package which has its own implementation of
# the python bson package: https://api.mongodb.com/python/3.4.0/index.html
#
# mongod needs to be running so this script can read from the db.
#
# NOTE: this will *not* make any changes to the Arango Database, it outputs
# JSON records that you can then import into the Arango "note" collection.
# To avoid duplicates, each record has a 'legacy_migration' field which
# is set to true. Use this to remove records before re-importing the data.

from pymongo import MongoClient
import pprint
import shortid
import datetime
import time

DEBUG = False

mongoClient = MongoClient()

db = mongoClient['openreview-production']
legacyDocuments = db['document']
legacyAuthors = db['eventprocessor']
legacyEventProcessor = db['eventprocessor']
legacyUsers = db['user']
legacyEvent = db['event']
legacyVenue = db['venue']

# create a map from the mongo venue "slug" to the submission invitation
submissionInvitations = { "iclr2013" : "ICLR.cc/2013/-/submission" ,"icml-peer2013" : "ICML.cc/2013/PeerReview/-/submission" ,"akbc2013" : "AKBC.ws/2013/-/submission",  "inferning2013" : "ICML.cc/2013/Inferning/-/submission"}

# todo temp to test JUST the AKBC conf in dev
venues = legacyVenue.find({"slug": "akbc2013"})

for venue in venues:
    if DEBUG:  print venue['name'] + " : " + str(venue['_id'])

    # get the invitation based on the venue
    submitInvite = submissionInvitations[venue['slug']]
    if DEBUG: print "Submission invitation: " + submitInvite
    noteJSON = {}

    # We'd like to get just the papers for a venue, but the data is a bit
    # wacky - there can be a venue field OR a target field - so we'll get all the
    # papers and sort that out one by one.
    papers = legacyEvent.find()
    count = 0
    for paper in papers:
        # IFF we have a venue field, use that, else target field
        v = paper.get('venue', None)
        if (v is None):
            v = paper.get('target', '?')
        # the doc id is a couple layers down...
        t = paper.get("template", {})
        dt = t.get("docTemplate", {})
        docid = dt.get("doc", "")

        # check if this document is for the venue and has a doc id
        if (v == venue['_id'] and len(str(docid)) > 0):
            # after all this, get the actual document
            doc = legacyDocuments.find_one({"_id" : docid})

            count += 1
            if DEBUG : print '\t' + doc['title']

            # Was this paper accepted?
            endorsementRec = legacyDocuments.find_one({"type": "endorsement", "inResponseTo": doc['_id']})

            if endorsementRec is None:
                endorsement = 'reject'
            else:
                endorsement = endorsementRec.get('endorsementType', '')
                # get the conference track (if there is one) from the eventprocessor collection.
                # IF there is a parent, this is a track like a conference or workshop
                track = legacyEventProcessor.find({'_id' : endorsementRec['creator']})
                # we only want the record that has a 'slug' field. There has to be a better
                # way like specifing it in the "find()", but since this is a one-off script we'll just hack it
                for t in track:
                    if t.get('slug') is not None and t.get('parentVenue') is not None:
                        endorsement += '-' + t['slug']

            if DEBUG: print '\t\t' + endorsement

            authors = legacyAuthors.find_one({"_id" : doc['authors']})

            pdf = doc.get('arXivID')
            if (pdf is not None):
                pdf = 'https://arxiv.org/abs/' + pdf
            else:
                # strip off the little something extra at the front of the URL field
                pdf = doc.get('url', '???').replace('URL~', '')
            if DEBUG: print "PDF: " + pdf

            tauthor = None
            authorNames = []
            authorEmails = []
            if DEBUG: print("\t\tAuthors: " + authors['name'])
            for sub in authors['subscribers']:
                user = legacyUsers.find_one({"_id" : sub})
                if DEBUG: print '\t\t\t' + user['fullname']
                authorNames.append('"' +  user['fullname'] + '"')
                # take the first email for this author (they can specify multiple emails)
                # We may want to check that it's verified or the preferred email
                firstEmail = next(iter(user['emails'] or []), None)
                authorEmails.append('"' + str(firstEmail['email']) + '"')
                # assume the first person listed is the "true author"
                if tauthor is None:
                    tauthor = firstEmail['email']

            authorEmailList = ', '.join(authorEmails)
            authorNameList = ', '.join(authorNames)

            dttm = doc['created'];
            t =  datetime.datetime(dttm.year, dttm.month, dttm.day, dttm.hour, dttm.minute)
            createddt = str(time.mktime(t.timetuple()) * 1000)

            forumid = shortid.ShortId().generate()

            # note: for now, we'll just use count for the paper number, normally this
            # would come from the "counter" collection in Arango

            # rather than replacing double quotes with '\"', we'll replace them with a
            # single quote. There is some data that the escaped double quote wouldn't work for
            # such as 'na\"ive'. So rather than handle all special cases, just use a single quote.
            abstract = doc['summary'].replace('"', '\'')
            # the import process to Arango wants one JSON record per line.
            noteJSON = ('{'
                '"tddate": null,'
                '"replyto": null,'
                '"active": true,'
                '"tmdate": ' + createddt + ','
                '"tcdate": ' + createddt + ','
                '"number": ' + str(count) + ','
                '"id": "' + forumid + '",'
                '"invitation": "' + submitInvite + '",'
                '"forum":   "' + forumid + '",'
                '"tauthor":  "' + tauthor + '",'
                '"signatures": [],'
                '"readers": ["everyone"],'
                '"writers": [],'
                '"content": {'
                '"decision" : "' + endorsement + '",'
                '"title": "' + doc['title'] + '",'
                    '"abstract": "' + abstract + '",'
                    '"pdf":  "' + pdf + '",'
                    '"conflicts": [],'
                    '"authors":   [' + authorNameList + '],'
                    '"keywords": [],'
                    '"authorids":   [' + authorEmailList + ']'
                '},'
                '"legacy_migration" : true'
            '}')
            # the last field (legacy_migration) will allow us to easily remove these records if needed.

            # some of the summaries contain line breaks which we don't want for the JSON import.
            print noteJSON.replace('\r\n', ' ').replace('\n', ' ')

