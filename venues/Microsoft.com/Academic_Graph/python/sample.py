import mag_importer
import pdf_tools
import openreview

'''
Set up openreview infrastructure

'''
client = openreview.Client()

microsoft = client.post_group(openreview.Group(**{
    'id': 'Microsoft.com',
    'readers': [],
    'writers': [],
    'signatures': [],
    'signatories': [],
    'members': []
}))

MAG = client.post_group(openreview.Group(**{
    'id': 'Microsoft.com/Academic_Graph',
    'readers': [],
    'writers': [],
    'signatures': [],
    'signatories': [],
    'members': []
}))

invitation = client.post_invitation(openreview.Invitation(**{
    'id': 'Microsoft.com/Academic_Graph/-/Upload',
    'readers': [],
    'writers': [],
    'signatures': [],
    'reply': {
        'readers': {'values': ['everyone']},
        'writers': {'values': []},
        'signatures': {'values': ['~Super_User1']},
        'content': {

        }
    },
    'transform': '../process/magTransform.js'
}))


'''
Retrieve information from Microsoft Academic Graph

'''
# Michael's Microsoft Azure API key
headers = {'Ocp-Apim-Subscription-Key': '77213bd18e094cc2892f149430270ba1'}

# Test out the pipeline on one of Andrew's papers
search_name = 'Andrew McCallum'

_, raw_entities = mag_importer.get_data_by_author(search_name, headers=headers)

# pick some paper (if they come in the same order, this one should have
# emails that are extractable from the PDF, but you may want to try others)
mag_raw = raw_entities[1]

# The output of this function is formatted as though it were the "content"
# field of an OpenReview Note record.
note_content = mag_importer.mag_transform(mag_raw)

# Get the PDF text. You could save this to a file if you wanted.
pdf_text = pdf_tools.pdf_to_text(note_content['pdf'])

# Pull out the emails (if possible)
emails = pdf_tools.get_emails_from_text(pdf_text)

if emails:
	# Match emails to names. Current implementation is very inefficient.
	# You should replace it with the min cost flow implementation.
	matched_emails, matched_names = pdf_tools.match_authors_to_emails(note_content['authors'], emails)

	# Complete the note content record by adding the emails
	note_content['authorids'] = matched_emails


'''
Package into a Note and post to OpenReview

'''
sample_note = openreview.Note(**{
    'readers': ['everyone'],
    'writers': [],
    'signatures': [],
    'invitation': 'Microsoft.com/Academic_Graph/-/Upload',
    'content': note_content
})

posted_note = client.post_note(sample_note)
print posted_note.id
