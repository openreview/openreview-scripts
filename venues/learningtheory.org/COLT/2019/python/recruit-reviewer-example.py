import colt19
import argparse
import openreview
import datetime
from Crypto.Hash import HMAC, SHA256
hash_seed = "1234"

if __name__ == '__main__':
    ## Argument handling
    parser = argparse.ArgumentParser()
    parser.add_argument('--baseurl', help="base url")
    parser.add_argument('--username')
    parser.add_argument('--password')
    args = parser.parse_args()

    client = openreview.Client(baseurl=args.baseurl, username=args.username, password=args.password)
    # Create super invitation
    recruit_invitation = openreview.Invitation(id = 'learningtheory.org/COLT/2019/Conference/-/Recruit_Reviewers',
                                            readers = ['everyone'],
                                            writers = ['learningtheory.org/COLT/2019/Conference'],
                                            signatures = ['learningtheory.org/COLT/2019/Conference'],
                                            process = '../process/recruitReviewersProcess.js',
                                            web = '../webfield/recruitResponseWebfield.js',
                                            reply = {
                                                'forum': None,
                                                'replyto': None,
                                                'readers': {
                                                    'values': ['~Super_User1']
                                                },
                                                'signatures': {
                                                    'values-regex': '\\(anonymous\\)'
                                                },
                                                'writers': {
                                                    'values': []
                                                },
                                                'content': {
                                                    'title': {
                                                        'order': 1,
                                                        'value': 'Invitation to review response'
                                                    },
                                                    'email': {
                                                        'description': 'email address',
                                                        'order': 2,
                                                        'value-regex': '.*@.*',
                                                        'required':True
                                                    },
                                                    'key': {
                                                        'description': 'Email key hash',
                                                        'order': 3,
                                                        'value-regex': '.{0,100}',
                                                        'required':True
                                                    },
                                                    'response': {
                                                        'description': 'Invitation response',
                                                        'order': 4,
                                                        'value-radio': ['Yes', 'No'],
                                                        'required':True
                                                    }
                                                }
        })
    recruit_invitation = client.post_invitation(recruit_invitation)

    #Get the first submission, SUBMIT A PAPER FIRST!
    paper = client.get_notes(invitation = 'learningtheory.org/COLT/2019/Conference/-/Submission', limit = 1)[0]

    sub_recruit_invitation = openreview.Invitation(id = 'learningtheory.org/COLT/2019/Conference/-/Paper' + str(paper.number) + '/Recruit_Reviewers',
                                                super = recruit_invitation.id,
                                                reply = {
                                                        'forum' : paper.id
                                                    }
                                                )
    sub_recruit_invitation = client.post_invitation(sub_recruit_invitation)

    #Create the necessary group, should we create them in the process function?
    paper_group = client.post_group(openreview.Group(id = 'learningtheory.org/COLT/2019/Conference/Paper' + str(paper.number),
    readers = ['learningtheory.org/COLT/2019/Conference'],
    writers = ['learningtheory.org/COLT/2019/Conference'],
    signatures = ['learningtheory.org/COLT/2019/Conference'],
    signatories = ['learningtheory.org/COLT/2019/Conference/Paper' + str(paper.number)]))

    pc_group = client.post_group(openreview.Group(id = paper_group.id + '/Program_Committee',
    readers = ['everyone'],
    writers = ['learningtheory.org/COLT/2019/Conference'],
    signatures = ['learningtheory.org/COLT/2019/Conference'],
    signatories = [paper_group.id + '/Program_Committee']))

    pc_declined_group = client.post_group(openreview.Group(id = pc_group.id + '/Declined',
    readers = ['everyone'],
    writers = ['learningtheory.org/COLT/2019/Conference'],
    signatures = ['learningtheory.org/COLT/2019/Conference'],
    signatories = [pc_group.id + '/Declined']))

    hashkey = HMAC.new(hash_seed.encode('utf-8'), msg='mbok@mail.com'.encode('utf-8'), digestmod=SHA256).hexdigest()
    print('http://localhost:3000/invitation?id=' + sub_recruit_invitation.id + '&email=mbok@mail.com&key=' + hashkey + '&response=Yes')
    print('DONE.')
