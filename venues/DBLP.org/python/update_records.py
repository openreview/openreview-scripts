#!/usr/bin/python
import openreview
import datetime
import calendar

import pytz
import config

def post_or_update(client, _content, verbose=False):
    '''
    Posts or updates a DBLP record. Returns the updated note.

    <arg>   : <description>
    client  : an instance of the openreview.Client class
    content : a dictionary representing the content of the record to be posted or updated.

    '''

    ## Not all data from DBLP exactly fits the invitation we've defined, so we need to rename a few fields.
    content = process_content(_content)

    if 'pub_key' not in content:
        print "content does not have pub_key"
        return None

    # Note that I'm using "pop()" here rather than
    # content['pub_key']. This removes the pub_key, it'll get generated
    # when the note is inserted as a "paper hash" so we don't want to
    # have BOTH paperhash and pub_key in the note's contents.
    pub_key = content.pop('pub_key')


    # we need to do a bit of special logic here. Some titles have matlab, latex,
    # or some other silliness in them,  the first '\' gets removed when the JSON
    # is read in. To match the paperhash we want to put that slash back in.
    if (pub_key.find("\\") != -1):
        pub_key = pub_key.replace("\\", "\\\\")

    if (content['title'].find("\\") != -1):
        content['title'] = content['title'].replace("\\", "\\\\")

    matches = client.get_notes(paperhash = pub_key)

    # If more than one match is found, something has gone wrong, so do nothing.
    if len(matches) > 1:
        print "WARNING: Multiple notes found for pub_key %s. This should not happen." % pub_key
        return None

    # if there is a date, make sure it is passed as a string
    if 'year' in content :
        content['year'] = str(content['year'])

    # If no matches, post a new note
    if len(matches) == 0:

        if verbose: print "pub_key not found. Creating new note. %s" % pub_key

        # add creation date
        cdate = get_cdate(content)

        # DBLP titles end with a period, remove it
        if (content['title'][-1]  == '.'):
            content['title'] = content['title'][:-1]

        new_note = client.post_note(openreview.Note.from_json(
            {
                'cdate' : cdate,
                'invitation': config.INVITATION,
                'readers': ['everyone'],
                'signatures': [config.GROUP],
                'writers': [config.GROUP],
                'content': content
            }
        ))

        return new_note

    # get all the revisions
    revisions = client.get_revisions(matches[0].id)

    # check all the revisions and see if this adds any new information.
    # This prevents duplicate revisions if we re-run an upload. In reality this
    # will be run daily/weekly/monthly, so any NEW record should be added as it's
    # newer information.

    need_revision = True

    for rev in revisions:
        if rev['invitation'].startswith(config.BASE):
            if all(content.get(k) == rev['content'].get(k) for k in ("ee", "isbn", "journal", "volume")):
                need_revision = False
                break

    # If one match is found, post a revision to the note IF the new content adds information.
    if len(matches) == 1 and not need_revision:
        if verbose: print "Provided content is the same as latest revision. No change."
        return None

    # if we got here, we want to add a revision
    if verbose: print "pub_key found. Adding revision to %s" % pub_key
    match = matches[0]

    # don't overwrite any existing fields.
    # right now (5/2017) DBLP data has "UNK" for authors so we'll remove
    # that field so we don't overwrite the current authors. This requires
    # the invitation to have this as a non-required field (it usually is required)
    if content.get('authorids'):
        content.pop('authorids')
    if content.get('authors'):
        content.pop('authors')
    if content.get('title'):
        content.pop('title')

    client.post_note(openreview.Note.from_json(
        {
            'forum': match.forum,
            'referent': match.forum,
            'invitation': config.INVITATION,
            'readers': ['everyone'],
            'signatures': [config.GROUP],
            'writers': [config.GROUP],
            'content': content
        }
    ))

    return None


def process_content(content):
    '''
    Modifies (in place) a dictionary representing the content of a DBLP record.
    Note: this is specifically useful for converting data from Ari's DBLP dataset into a usable format.

    <arg>   : <description>
    content : a dictionary representing the content of the record to be posted or updated.

    '''
    if 'url' in content : content['url'] = "http://dblp.dagstuhl.de/" + content['url']

    return content

def get_cdate(content):

    date_mask = "%d%b%Y" # default
    # To get the creation date, we'll use the most specific date field we have.
    if content.get("date"):
        date_text = content.get('date')
        date_mask = "%Y-%m-%d"
    elif content.get("year"):
        date_text = "01JAN" + content['year']
    else:
        date_text = "01JAN" + datetime.date.today().strftime("%Y")

    date = datetime.datetime.strptime(date_text, date_mask)

    # since we could be creating notes for conferences in the past
    # we want to make sure we localize the date. Without this, we
    # sometimes get a 'cdate' that is the day prior to what we
    # really want due to timezones.
    eastern = pytz.timezone('US/Eastern')
    # we want the date/time in microseconds hence the multiplication by 1000
    return calendar.timegm(eastern.localize(date).utctimetuple()) * 1000
