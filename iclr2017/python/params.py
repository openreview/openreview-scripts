import pydash
import sys

rootUser = {
    'id':'OpenReview.net'
}

## This group should probably already exist by the time these scripts get sent to the PCs,
## so remember to remove it and test before then
iclr = {
    'id': 'ICLR.cc',
    'members': [rootUser['id']],
    'readers': ['everyone'],
    'signatories': ['ICLR.cc', rootUser['id']],
    'signatures': [rootUser['id']],
    'writers': ['ICLR.cc',rootUser['id']]
}

iclr2017 = {
    'id': iclr['id']+'/2017',
    'members': [],
    'readers': ['everyone'],
    'signatories': [iclr['id'], iclr['id']+'/2017'],
    'signatures': [iclr['id']],
    'writers': [iclr['id']] #iclr['id']+'/2017',
}

iclr2017programchairs = {
    'id': iclr2017['id']+'/pc',
    'members': [iclr2017['id']], #members of program chairs group are set by script
    'readers': ['everyone'],
    'signatories':[iclr2017['id']+'/pc'],
    'signatures': [iclr2017['id']],
    'writers': [iclr2017['id']+'/pc',iclr2017['id']]
}

iclr2017areaChairs = {
    'id': iclr2017['id']+'/areachairs',
    'signatures':[iclr2017['id']],
    'writers':[iclr2017['id']+'/areachairs',iclr2017['id']],
    'readers':['everyone'],
    'members':[], #members of area chairs group are set by script
    'signatories':[iclr2017['id']+'/areachairs']
}

iclr2017reviewers = {
    'id': iclr2017['id']+'/reviewers',
    'signatures': [iclr2017['id']],
    'writers': [iclr2017['id']+'/reviewers',iclr2017['id']],
    'readers': ['everyone'],
    'members': [], #members of reviewers group are set by script
    'signatories': []
}
iclr2017reviewersInvited = {
    'id': iclr2017['id']+'/reviewers-invited',
    'signatures': [iclr2017['id']],
    'writers': [iclr2017['id']+'/reviewers-invited',iclr2017['id']],
    'readers': [iclr2017programchairs['id']],
    'members': [], #members of reviewers-invited group are set by script
    'signatories': []   
}
iclr2017reviewersDeclined = {
    'id': iclr2017['id']+'/reviewers-declined',
    'signatures': [iclr2017['id']],
    'writers': [iclr2017['id']],
    'readers': [iclr2017programchairs['id']],
    'members': [], #members of reviewers-declined group are added based on reviewer responses
    'signatories': []
}

iclr2017conference = {
    'id': iclr2017['id']+'/conference',
    'signatures': [iclr2017['id']],
    'writers': [iclr2017['id']],
    'readers': ['everyone'],
    'members': [iclr2017programchairs['id'], iclr2017areaChairs['id']], #members of workshop group are set below
    'signatories': [iclr2017['id'], iclr2017['id']+'/conference']
}

with open('../webfield/iclr2017_webfield.html') as f: 
    iclr2017conference['web'] = f.read()

note1 = {
    'content': {
        'CMT_id':'',
        'abstract':'This is note 1',
        'author_emails':"author@gmail.com",
        'authors':'Author 1',
        'conflicts':'cs.berkeley.edu',
        'pdf':'http://arxiv.org/pdf/1407.1808v1.pdf',
        'title':'Note 1',
        'keywords':['keyword']
    },
    'forum': None,
    'invitation': iclr2017conference['id']+'/-/submission',
    'parent': None,
    'pdfTransfer':"url",
    'readers':["everyone"],
    'signatures':["~super_user1"],
    'writers':["~super_user1"],
}

## Create the submission invitation
subInvitationBody = { 
    'id':'ICLR.cc/2017/conference/-/submission', 
    'signatures':['ICLR.cc/2017/conference'],
    'writers':['ICLR.cc/2017/conference'], 
    'invitees':['~'],
    'reply':{
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
            },          
            'keywords': {
                'order': 5,
                'values-regex': '.*',
                'description': 'Comma separated list of keywords.'
            }
        }
    }
}
with open('../process/submissionProcess_iclr2017.js') as f: 
    subInvitationBody['process'] = f.read()

