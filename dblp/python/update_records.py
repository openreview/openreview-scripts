#!/usr/bin/python
import openreview

def post_or_update(client, content):
    '''
    Posts or updates a DBLP record. Returns the updated note.
    '''

    if 'pub_key' in content:
        pub_key = content['pub_key']
        matches = client.search_notes(pub_key)

        # If no matches, post a new note
        if len(matches) == 0:
            print "pub_key not found. Creating new note."
            new_note = client.post_note(openreview.Note.from_json(
                {
                    'invitation': 'DBLP.org/-/paper',
                    'readers': ['everyone'],
                    'signatures': ['DBLP.org/upload'],
                    'writers': ['DBLP.org/upload'],
                    'content': content
                }
            ))

            print "New note created."
            return new_note

        # If one match is found, post a revision to the note
        elif len(matches) == 1:
            print "pub_key found. Adding revision to %s" % pub_key
            match = matches[0]
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

            print "Existing note revised."
            return client.get_note(match.id)

        # If more than one match is found, something has gone wrong, so do nothing.
        elif len(matches) > 1:
            print "WARNING: Multiple notes found for pub_key %s. This should not happen." % pub_key
            return None

    else:
        print "content does not have pub_key"
        return None
