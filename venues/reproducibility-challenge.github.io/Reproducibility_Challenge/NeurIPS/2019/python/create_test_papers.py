import openreview

# live
#client = openreview.Client(baseurl='https://openreview.net')
# dev site
#client = openreview.Client(baseurl='https://dev.openreview.net', username='OpenReview.net', password='OpenReview_dev')
client = openreview.Client()
print(client.baseurl)
conference_id='reproducibility-challenge.github.io/Reproducibility_Challenge/NeurIPS/2019'

accepted_info = [{'title': 'Paper A','abstract':'This is my fruity abstract','authors': ['Haw-Shiuan Chang', 'Erik Learned-Miller', 'Andrew McCallum']},
                 {'title': 'Paper B','abstract':'Something mysterious','authors': 'George Gently'},
                 {'title': 'Paper C','abstract':'I\'ll give you a clue','authors': 'Professor Plum'},
                 {'title': 'Paper D','abstract':'Who framed Roger','authors': 'Jessica Rabbit'},
                ]

for info in accepted_info:
    client.post_note(openreview.Note(
                        id = None,
                        original= None,
                        invitation= conference_id+"/-/NeurIPS_Submission",
                        forum=None,
                        signatures= [conference_id+"/Program_Chairs"],
                        writers= [conference_id],
                        readers= ['everyone'],
                        content= {
                            "title": info['title'],
                            "authors": info['authors'],
                            "abstract": info['abstract']
                    }))
