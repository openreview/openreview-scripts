import mag_importer

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
pdf_text = mag_importer.pdf_to_text(note_content['pdf'])

# Pull out the emails (if possible)
emails = mag_importer.get_emails_from_text(pdf_text)

if emails:
	# Match emails to names. Current implementation is very inefficient.
	# You should replace it with the min cost flow implementation.
	ordered_emails, ordered_names = mag_importer.match_emails_to_ordered_authors(emails, note_content['authors'])

	# Complete the note content record by adding the emails
	note_content['authorids'] = ordered_emails

# Display the contents of the note. You could save this as a JSON if you wanted.
print note_content
