#!/usr/bin/python
import openreview

def post_or_update(client, content, verbose=False):
    '''
    Posts or updates a DBLP record. Returns the updated note.

    <arg>   : <description>
    client  : an instance of the openreview.Client class
    content : a dictionary representing the content of the record to be posted or updated.

    Note: "content" argument should conform to the reply field of the invitation "DBLP.org/-/paper"

    '''

    if 'pub_key' in content:
        pub_key = content['pub_key']
        matches = client.search_notes(pub_key)

        # If no matches, post a new note
        if len(matches) == 0:
            if verbose: print "pub_key not found. Creating new note."
            new_note = client.post_note(openreview.Note.from_json(
                {
                    'invitation': 'DBLP.org/-/paper',
                    'readers': ['everyone'],
                    'signatures': ['DBLP.org/upload'],
                    'writers': ['DBLP.org/upload'],
                    'content': content
                }
            ))

            if verbose: print "New note created."
            return new_note

        # If one match is found, post a revision to the note
        elif len(matches) == 1:
            match = matches[0]

            if match.content != content:
                if verbose: print "pub_key found. Adding revision to %s" % pub_key
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
                if verbose: print "Existing note revised."
            else:
                if verbose: print "Provided content is the same as latest revision. No change."

            return client.get_note(match.id)

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
