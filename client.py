#!/usr/bin/python
import requests
import pydash
import json
import os
from Crypto.Hash import HMAC, SHA256

class client(object):

    def __init__(self, username, password, base_url='http://localhost:3000', process_dir='../process/', webfield_dir='../webfield/'):
        self.base_url = base_url
        self.groups_url = self.base_url+'/groups'
        self.login_url = self.base_url+'/login'
        self.register_url = self.base_url+'/register'
        self.invitations_url = self.base_url+'/invitations'
        self.mail_url = self.base_url+'/mail'
        self.notes_url = self.base_url+'/notes'
        self.user = {'id':username, 'password':password}
        print str(requests.post(self.login_url, json=self.user).json())
        self.token = str(requests.post(self.login_url, json=self.user).json()['token'])
        self.headers = self.get_header(self.token)

    def get_header(self, token):
        return {
            'Authorization': 'Bearer ' + token,
            'User-Agent': 'test-create-script',
        }

    def get_hash(self, data, secret):
        hash = HMAC.new(secret, msg=data, digestmod=SHA256)
        return hash.hexdigest()

    def get_filename(self, id_, ext):
        new_id = id_.replace('.','')
        new_id = new_id.split('/')
        new_id.remove('-')
        return '_'.join(new_id) + ext


    def pretty_json(self, request):
        return json.dumps(json.loads(request.text), indent=4, sort_keys=True)


    def create_base_invitation(self, params=None):
        invitation = {
            'id': None,
            'signatures': [],
            'writers': [],
            'invitees': [],
            'noninvitees': [],
            'readers': ['everyone'],
            'reply': {
                'content': {}
            }
        }
        if params != None:
            pydash.assign(invitation, pydash.omit(params, 'reply'))
            if 'reply' in params:
                pydash.assign(invitation['reply'], pydash.omit(params['reply'], 'content'))
                if 'content' in params['reply']:
                    pydash.assign(invitation['reply']['content'], params['reply']['content'])
        return invitation

    def create_review_invitation(self, params=None):
        invitation = self.create_base_invitation()
        
        with open('./process/reviewProcess.js') as f: 
            invitation['process'] = f.read()
        
        reply = {
            'forum': None,
            'parent': None,
            'signatures': {
                'values-regex':'~.*',
                'description':'Your displayed identity associated with the above content.'
            },
            'writers': {
                'values-regex':'~.*'
            }, 
            'readers': { 
                'values': ['everyone'], 
                'description': 'The users who will be allowed to read the above content.'
            },
            'content': {
                'title': {
                    'order': 1,
                    'value-regex': '.{0,500}',
                    'description': 'Brief summary of your review.'
                },
                'review': {
                    'order': 2,
                    'value-regex': '[\\S\\s]{1,5000}',
                    'description': 'Please provide an evaluation of the quality, clarity, originality and significance of this work, including a list of its pros and cons.'
                },
                'rating': {
                    'order': 3,
                    'value-dropdown': [
                        '10: Top 5% of accepted papers, seminal paper', 
                        '9: Top 15% of accepted papers, strong accept', 
                        '8: Top 50% of accepted papers, clear accept', 
                        '7: Good paper, accept',
                        '6: Marginally above acceptance threshold',
                        '5: Marginally below acceptance threshold',
                        '4: Ok but not good enough - rejection',
                        '3: Clear rejection',
                        '2: Strong rejection',
                        '1: Trivial or wrong'
                    ]
                },
                'confidence': {
                    'order': 4,
                    'value-radio': [
                        '5: The reviewer is absolutely certain that the evaluation is correct and very familiar with the relevant literature', 
                        '4: The reviewer is confident but not absolutely certain that the evaluation is correct', 
                        '3: The reviewer is fairly confident that the evaluation is correct',
                        '2: The reviewer is willing to defend the evaluation, but it is quite likely that the reviewer did not understand central parts of the paper',
                        '1: The reviewer\'s evaluation is an educated guess'
                    ]
                }
            }
        }

        invitation['reply'] = reply

        if params != None:
            pydash.assign(invitation, pydash.omit(params, 'reply'))
            if 'reply' in params:
                pydash.assign(invitation['reply'], pydash.omit(params['reply'], 'content'))
                if 'content' in params['reply']:
                    pydash.assign(invitation['reply']['content'], params['reply']['content'])

        return invitation

    def create_submission_invitation(self, params=None):
        invitation = self.create_base_invitation()
        
        reply = {
            'forum': None,
            'parent': None,
            'signatures': {
                'values-regex': '~.*',
                'description':'Your displayed identity associated with the above content.'
            },
            'writers': {'values-regex': '~.*'},
            'readers': { 
                'values': ['everyone'], 
                'description': 'The users who will be allowed to read the above content.'
            },
            'content': {
                'title': {
                    'order': 3,
                    'value-regex': '.{1,100}',
                    'description': 'Title of paper.'
                },
                'abstract': {
                    'order': 4,
                    'value-regex': '[\\S\\s]{1,5000}',
                    'description': 'Abstract of paper.'
                },
                'authors': {
                    'order': 1,
                    'value-regex': '[^,\\n]+(,[^,\\n]+)*',
                    'description': 'Comma separated list of author names, as they appear in the paper.'
                },
                'author_emails': {
                    'order': 2,
                    'value-regex': '[^,\\n]+(,[^,\\n]+)*',
                    'description': 'Comma separated list of author email addresses, in the same order as above.'
                },
                'conflicts': {
                    'order': 100,
                    'value-regex': "^([a-zA-Z0-9][a-zA-Z0-9-_]{0,61}[a-zA-Z0-9]{0,1}\\.([a-zA-Z]{1,6}|[a-zA-Z0-9-]{1,30}\\.[a-zA-Z]{2,3}))+(;[a-zA-Z0-9][a-zA-Z0-9-_]{0,61}[a-zA-Z0-9]{0,1}\\.([a-zA-Z]{1,6}|[a-zA-Z0-9-]{1,30}\\.[a-zA-Z]{2,3}))*$",
                    'description': 'Semi-colon separated list of email domains of people who would have a conflict of interest in reviewing this paper, (e.g., cs.umass.edu;google.com, etc.).'
                },
                'pdf': {
                    'order': 4,
                    'value-regex': 'upload|http://arxiv.org/pdf/.+',
                    'description': 'Either upload a PDF file or provide a direct link to your PDF on ArXiv.'
                }
            }
        }
    
        invitation['reply'] = reply

        if params != None:
            pydash.assign(invitation, pydash.omit(params, 'reply'))
            if 'reply' in params:
                pydash.assign(invitation['reply'], pydash.omit(params['reply'], 'content'))
                if 'content' in params['reply']:
                    pydash.assign(invitation['reply']['content'], params['reply']['content'])

        return invitation

    def create_comment_invitation(self, params=None):
        invitation = self.create_base_invitation()
        
        with open('./process/commentProcess.js') as f: 
            invitation['process'] = f.read()
        
        reply = {
            'forum': None,
            #'parent' is intentionally unspecified. This allows comments on comments.
            'signatures': {
                'values-regex':'~.*',
                'description': 'Your displayed identity associated with the above content.' 
            },
            'writers': {'values-regex':'~.*'},
            'readers': { 
                'values': ['everyone'], 
                'description': 'The users who will be allowed to read the above content.'
            },
            'content': {
                'title': {
                    'order': 1,
                    'value-regex': '.{1,500}',
                    'description': 'Brief summary of your comment.'
                },
                'comment': {
                    'order': 2,
                    'value-regex': '[\\S\\s]{1,5000}',
                    'description': 'Your comment or reply.'
                }
            }
        }

        invitation['reply'] = reply

        if params != None:
            pydash.assign(invitation, pydash.omit(params, 'reply'))
            if 'reply' in params:
                pydash.assign(invitation['reply'], pydash.omit(params['reply'], 'content'))
                if 'content' in params['reply']:
                    pydash.assign(invitation['reply']['content'], params['reply']['content'])

        return invitation

    def add_group_member(self,groupId, member):
        r = requests.get(self.groups_url, params={'id':groupId}, headers=self.headers)
        group = json.loads(r.content)['groups'][0]
        pydash.assign(group, {'members': group['members']+[member]})
        rp = requests.post(self.groups_url, json=group, headers=self.headers)
        rp.raise_for_status()
        print "Group " + member + " added to " + groupId
    
    def remove_group_member(self,groupId, member):
        r = requests.get(self.groups_url, params={'id':groupId}, headers=self.headers)
        group = json.loads(r.content)['groups'][0]
        pydash.assign(group, {'members': pydash.without(group['members'], member)})
        requests.post(self.groups_url, json=group, headers=self.headers)
        print "Group " + member + " removed from " + groupId

    def get_group(self, inputs, outputdir=None):
        r = requests.get(self.groups_url, params=inputs, headers=self.headers)
        r.raise_for_status()
        if outputdir == None:
            return r
        else:
            print outputdir #TODO: Save output to csv
            return r

    def get_invitation(self, inputs, outputdir=None):
        r = requests.get(self.invitations_url, params=inputs, headers=self.headers)
        r.raise_for_status()
        if outputdir == None:
            return r
        else:
            print outputdir #TODO: Save output to csv
            return r

    def get_note(self, inputs, outputdir=None):
        r = requests.get(self.notes_url, params=inputs, headers=self.headers)
        r.raise_for_status()
        if outputdir == None:
            return r
        else:
            print outputdir #TODO: Save output to csv
            return r

    def set_group(self, inputs, outputdir=None):
        r = requests.post(self.groups_url, json=inputs, headers=self.headers)
        r.raise_for_status()
        if outputdir == None:
            return r
        else:
            print outputdir #TODO: Save output to csv
            return r

    def set_invitation(self, inputs, outputdir=None):
        r = requests.post(self.invitations_url, json=inputs, headers=self.headers)
        r.raise_for_status()
        if outputdir == None:
            return r
        else:
            print outputdir #TODO: Save output to csv
            return r

    def set_note(self, inputs, outputdir=None):
        r = requests.post(self.notes_url, json=inputs, headers=self.headers)
        r.raise_for_status()
        if outputdir == None:
            return r
        else:
            print outputdir #TODO: Save output to csv
            return r

    def send_mail(self, subject, recipients, message):
        requests.post(self.mail_url, json={'groups': recipients, 'subject': subject , 'message': message}, headers=self.headers)



class group(object):
    def __init__(self, id_, writers=None, members=None, readers=None, signatories=None, web=None):
        self.body = {
            'id': id_,
            'signatures': [id_] if writers==None else writers,
            'writers': [id_] if writers==None else writers,
            'members': [] if members==None else members,
            'readers': [id_] if readers==None and writers==None else writers if readers==None else readers,
            'signatories': [id_] if signatories==None else signatories,
            'web': web
        }

class invitation(object):
    def __init__(self, id_, web=None, process=None):
        self.body = {
            'id': id_,
            'signatures': [id_],
            'writers': [id_],
            'members': [],
            'readers': [id_],
            'signatories': [id_],
            'web': web,
            'process': process,
            'reply':{}
        }