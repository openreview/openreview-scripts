import openreview

'''
You should be logged in as a program chair, or as the UAI Admin user.
'''
client = openreview.Client()

meta_reviews = client.get_notes(invitation='auai.org/UAI/2018/-/Paper.*/Meta_Review')

sample_meta_review = meta_reviews[0]

# e.g. for a given paper
decision_invitation = sample_meta_review.invitation.replace('Meta_Review','Final_Decision')
id_split = decision_invitation.split('/')
paper_number = id_split[4]
paper_forum = sample_meta_review.forum

'''
Keep all parameters the same except for the fields in 'content'

'decision' can take a value of "Accept" or "Reject". This can be changed if you would like.
'comment' is a text field. You can copy the metareview into this field.
'presentation format', 'best paper', and 'best student paper' are the same as the metareview.
'''

decision_note = openreview.Note(**{
    'invitation': decision_invitation,
    'forum': paper_forum,
    'replyto': paper_forum,
    'readers': ['auai.org/UAI/2018', 'auai.org/UAI/2018/Program_Chairs'],
    'signatures': ['auai.org/UAI/2018/Program_Chairs'],
    'writers': ['auai.org/UAI/2018', 'auai.org/UAI/2018/Program_Chairs'],
    'content': {
        'title': '{} Final Decision'.format(paper_number),
        'decision': 'Accept' if 'accept' in sample_meta_review.content['recommendation'].lower() else 'Reject',
        'comment': sample_meta_review.content['metareview'],
        'presentation format': sample_meta_review.content['presentation format'],
        'best paper': sample_meta_review.content['best paper'],
        'best student paper': sample_meta_review.content['best student paper'],
    }
})
