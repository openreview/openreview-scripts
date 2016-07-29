#!/usr/bin/python
import requests

import json
import os
import getpass
import ConfigParser
from Crypto.Hash import HMAC, SHA256



class Client(object):

    def __init__(self, base_url=None, config='./openreview_config.ini', process_dir='../process/', webfield_dir='../webfield/'):
        """CONSTRUCTOR DOCSTRING"""
        
        self.base_url = base_url if base_url != None else 'http://localhost:3000'
        self.config = config
        self.groups_url = self.base_url+'/groups'
        self.login_url = self.base_url+'/login'
        self.register_url = self.base_url+'/register'
        self.invitations_url = self.base_url+'/invitations'
        self.mail_url = self.base_url+'/mail'
        self.notes_url = self.base_url+'/notes'
        self.token = self.__login_user()
        self.headers = {'Authorization': 'Bearer ' + self.token, 'User-Agent': 'test-create-script'}
        self.user = {}

    ## PRIVATE FUNCTIONS

    def __login_user(self):
        
        config = ConfigParser.ConfigParser()
        config.read(self.config)
        try:
            username = config.get('credentials','username')
        except ConfigParser.NoOptionError:
            username = raw_input("Please provide your OpenReview username (e.g. username@umass.edu): ")
        
        try:    
            password = config.get('credentials','password')
        except ConfigParser.NoOptionError:   
            password = getpass.getpass("Please provide your OpenReview password: ")

        self.user = {'id':username,'password':password}
        token_response = requests.post(self.login_url, json=self.user)
        
        try:
            if token_response.status_code != 200:
                token_response.raise_for_status()
            else:
                return str(token_response.json()['token'])
        except requests.exceptions.HTTPError as e:
            for error in token_response.json()['errors']:
                print "ERROR: "+error

    ## PUBLIC FUNCTIONS

    def get_hash(self, data, secret):
        """Gets the hash of a piece of data given a secret value

        Keyword arguments:
        data -- the data to be encrypted
        secret -- the secret value used to encrypt the data
        """
        _hash = HMAC.new(secret, msg=data, digestmod=SHA256).hexdigest()
        return _hash

    def get_group(self, id):
        """Returns a single Group by id if available"""
        response = requests.get(self.groups_url, params={'id':id}, headers=self.headers)
        
        try:
            if response.status_code != 200:
                response.raise_for_status()
            else:
                g = response.json()['groups'][0]
                group = Group(g['id'],
                    writers = g['writers'],
                    members = g['members'], 
                    readers = g['readers'], 
                    signatories = g['signatories'], 
                    signatures = g['signatures'], 
                    )
                if group.web != None:
                    group.web = g['web']
                return group

        except requests.exceptions.HTTPError as e:
            for error in response.json()['errors']:
                print "ERROR: "+error


    def get_groups(self, prefix=None, member=None, host=None, signatory=None):
        """Returns a list of Group objects based on the filters provided."""
        groups=[]
        params = {}
        if prefix!=None:
            params['regex'] = prefix+'.*'
        if member!=None:
            params['member'] = member
        if host!=None:
            params['host'] = host
        if signatory!=None:
            params['signatory'] = signatory

        response = requests.get(self.groups_url, params=params, headers=self.headers)
        
        try:
            if response.status_code != 200:
                response.raise_for_status()
            else:
                for g in response.json()['groups']:
                    group = Group(g['id'], 
                                writers=g['writers'], 
                                members=g['members'], 
                                readers=g['readers'],
                                signatories=g['signatories'],
                                signatures=g['signatures'],
                                )
                    group.web=g['web']
                    groups.append(group)
                groups.sort(key=lambda x: x.id)
                return groups
                
        except requests.exceptions.HTTPError as e:
            for error in response.json()['errors']:
                print "ERROR: "+error

    def save_group(self, group):
        """Saves the group. Upon success, returns the original Group object."""
        response = requests.post(self.groups_url, json=group.to_json(), headers=self.headers)
        try:
            if response.status_code != 200:
                response.raise_for_status()
            else:
                return group
        except requests.exceptions.HTTPError as e:
            print response.json()
            for error in response.json()['errors']:
                print "ERROR: "+error

        

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


    def save_invitation(self, inputs, outputdir=None):
        r = requests.post(self.invitations_url, json=inputs, headers=self.headers)
        r.raise_for_status()
        print r.text
        if outputdir == None:
            return r
        else:
            print outputdir #TODO: Save output to csv
            return r

    def save_note(self, inputs, outputdir=None):
        r = requests.post(self.notes_url, json=inputs, headers=self.headers)
        r.raise_for_status()
        if outputdir == None:
            return r
        else:
            print outputdir #TODO: Save output to csv
            return r

    def send_mail(self, subject, recipients, message):
        r = requests.post(self.mail_url, json={'groups': recipients, 'subject': subject , 'message': message}, headers=self.headers)
        r.raise_for_status()






class Group(object):
    
    def __init__(self, id, writers=None, members=None, readers=None, signatories=None, signatures=None, web=None):
        # save attributes
        self.id=id
        self.writers=writers
        self.members=members
        self.readers=readers
        self.signatories=signatories
        self.signatures=signatures
        if web != None:
            with open(web) as f:
                self.web = f.read()
        else:
            self.web=None
    
    def to_json(self):
        body = {
            'id': self.id,
            'signatures': self.signatures,
            'writers': self.writers,
            'members': self.members,
            'readers': self.readers,
            'signatories': self.signatories
        }
        if self.web:
            body['web']=self.web
        return body

    def __str__(self):
        return '{:12}'.format('id: ')+self.id+'\n{:12}'.format('members: ')+', '.join(self.members)

    def add_member(self, member):
        if type(member) is Group:
            self.members.append(member.id)
        if type(member) is str:
            self.members.append(member)
        return self

    def save(self, client):
        client.save_group(self)



class Invitation(object):
    def __init__(self, inviter, suffix, writers=None, invitees=None, readers=None, reply=None, web=None, process=None, signatures=None):
        self.id = inviter+'/-/'+suffix
        self.readers=readers
        self.writers=writers
        self.invitees=invitees
        self.reply={} if reply==None else reply

        self.body = {
            'id': inviter+'/-/'+suffix,
            ## e.g. inviter = 'ICLR.cc/2017/conference', suffix = 'submission'

            'readers': readers,
            'writers': writers,
            'invitees': invitees,
            'signatures': signatures,
            ## double check that this is not a problem for the invitees;
            ## i.e., if readers are restricted but invitees are not, can the right invitees still respond to this invitation?

            'reply':{} if reply==None else reply
        }
        if web != None:
            with open(web) as f:
                self.body['web'] = f.read()

        if process != None:
            with open(process) as f:
                self.body['process'] = f.read()
