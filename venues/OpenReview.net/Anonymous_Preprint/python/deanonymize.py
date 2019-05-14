import openreview
import argparse

def deanonymize(mask, original):
    '''
    Deanonymizes an OpenReview Anonymous Archive submission by:
    1) Removing `authors` and `authorids` from the Blind_Submission reference
    2) Replacing the Authors field of the bibtex with the authors from the Original
    3) Placing the lowercased last name of the first author in the bibtex ID

    Returns the deanonymized reference to be posted.
    '''

    mask.content.pop('authors')
    mask.content.pop('authorids')
    mask.content['_bibtex'] = mask.content['_bibtex'].replace(
        '{Anonymous}',
        ', '.join(original.content['authors']))

    first_author = original.content['authors'][0]
    lastname = first_author.split(' ')[-1].lower()

    mask.content['_bibtex'] = mask.content['_bibtex'].replace(
        '\nanonymous',
        '\n'+lastname)

    return mask

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('forum_id')
    parser.add_argument('--baseurl', help="base url")
    parser.add_argument('--username')
    parser.add_argument('--password')
    args = parser.parse_args()

    client = openreview.Client(baseurl=args.baseurl, username=args.username, password=args.password)

    blind = client.get_note(args.forum_id)
    original = client.get_note(blind.original)
    references = client.get_references(referent=blind.forum)
    blind_refs = [ref for ref in references if ref.invitation=='OpenReview.net/Anonymous_Preprint/-/Blind_Submission']

    assert len(blind_refs) == 1, 'something went wrong; multiple blind references'

    mask = blind_refs[0]

    new_mask = deanonymize(mask, original)

    client.post_note(new_mask)
