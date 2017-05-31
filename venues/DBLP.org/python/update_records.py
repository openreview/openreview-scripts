#!/usr/bin/python
import openreview
import datetime
import calendar

def post_or_update(client, content, verbose=False):
    '''
    Posts or updates a DBLP record. Returns the updated note.

    <arg>   : <description>
    client  : an instance of the openreview.Client class
    content : a dictionary representing the content of the record to be posted or updated.

    Note: "content" argument should conform to the reply field of the invitation "DBLP.org/-/Upload"

    '''

    if 'pub_key' in content:
        pub_key = content['pub_key']

        # we need to do a bit of special logic here. Some titles have matlab, latex,
        # or some other silliness in them,  the first '\' gets removed when the JSON
        # is read in. To match the paperhash we want to put that slash back in.
        if (pub_key.find("\\") != -1):
            pub_key = pub_key.replace("\\", "\\\\")

        matches = client.get_notes(paperhash = pub_key)

        # remove the pub_key, it'll get generated
        # when the note is inserted as a "paper hash"
        content.pop('pub_key')

        # if there is a date, make sure it is passed as a string
        if 'year' in content :
            content['year'] = str(content['year'])

        # If no matches, post a new note
        if len(matches) == 0:

            # add creation date
            yr = datetime.date.today().strftime("%Y")
            if content.get('year'):
                yr = content['year']
            date_text = "01JAN" + yr
            date = datetime.datetime.strptime(date_text, "%d%b%Y")
            cdate = calendar.timegm(date.utctimetuple())

            if verbose: print "pub_key not found. Creating new note. %s" % pub_key
            new_note = client.post_note(openreview.Note.from_json(
                {
                    'cdate' : cdate * 1000,
                    'invitation': 'DBLP.org/-/Upload',
                    'readers': ['everyone'],
                    'signatures': ['DBLP.org/upload'],
                    'writers': ['DBLP.org/upload'],
                    'content': content
                }
            ))

            # if verbose: print "New note created."
            return new_note

        # If one match is found, post a revision to the note
        elif len(matches) == 1:
            match = matches[0]

            # we often have to re-run a set of JSON files from DBLP so
            # we want to make sure we don't put duplicate revisions.
            # right now (5/2017) DBLP data has "UNK" for authors so we'll remove
            # that field from BOTH so the comparison doesn't take them into account.
            match.content.pop('authorids')
            content.pop('authorids')
            # also remove 'paperhash' from the existing record, the JSON has 'pub-key' which
            # we removed above.
            match.content.pop('paperhash')

            if match.content != content:
                if verbose: print "pub_key found. Adding revision to %s" % pub_key

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
                        'invitation': 'DBLP.org/-/Add/Revision',
                        'readers': ['everyone'],
                        'signatures': ['DBLP.org/upload'],
                        'writers': ['DBLP.org/upload'],
                        'content': content
                    }
                ))
                # if verbose: print "Existing note revised."
            else:
                if verbose: print "Provided content is the same as latest revision. No change."

            return None

        # If more than one match is found, something has gone wrong, so do nothing.
        elif len(matches) > 1:
            print "WARNING: Multiple notes found for pub_key %s. This should not happen." % pub_key
            return None

    else:
        print "content does not have pub_key"
        return None


def process_content(content):
    '''
    Modifies (in place) a dictionary representing the content of a DBLP record.
    Note: this is specifically useful for converting data from Ari's DBLP dataset into a usable format.

    <arg>   : <description>
    content : a dictionary representing the content of the record to be posted or updated.

    '''
    if 'dblp_coref_emails' in content: content['authorids'] = content.pop('dblp_coref_emails')
    if 'names_readable' in content: content['authors'] = content.pop('names_readable')
    if 'venue' in content: content['journal'] = content.pop('venue')
    return content
