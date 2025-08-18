'''
Set up the PC recruitment pipeline
'''

import openreview
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--baseurl', help="base URL")
parser.add_argument('--username')
parser.add_argument('--password')

args = parser.parse_args()

client = openreview.Client(baseurl=args.baseurl, username=args.username, password=args.password)
print 'connecting to {0}'.format(client.baseurl)

# MODIFIED_BY_YCN: commented out post the root group
#client.post_group(openreview.Group(**{
#        'id': 'auai.org/UAI/2018',
#        'readers': ['everyone'],
#        'writers': ['~Super_User1'],
#        'signatures': ['~Super_User1'],
#        'signatories': ['auai.org/UAI/2018'],
#        'members': []
#    }))

# MODIFIED_BY_YCN: commented out post the program chairs group
#client.post_group(openreview.Group(**{
#        'id': 'auai.org/UAI/2018/Program_Chairs',
#        'readers': ['auai.org/UAI/2018','auai.org/UAI/2018/Program_Chairs'],
#        'writers': ['auai.org/UAI/2018'],
#        'signatures': ['auai.org/UAI/2018'],
#        'signatories': ['auai.org/UAI/2018/Program_Chairs'],
#        'members': ['~Yin_Cheng_Ng1','~Ricardo_Silva1','~Amir_Globerson1']
#    }))

# MODIFIED_BY_YCN: post the PC group(s)
# 1. changed 'id' from 'auai.org/UAI/2018/Senior_Program_Committee' -> 'auai.org/UAI/2018/Program_Committee'
client.post_group(openreview.Group(**{
        'id': 'auai.org/UAI/2018/Program_Committee',
        'readers': ['auai.org/UAI/2018','auai.org/UAI/2018/Program_Chairs','auai.org/UAI/2018/Senior_Program_Committee'],
        'writers': ['auai.org/UAI/2018'],
        'signatures': ['auai.org/UAI/2018'],
        'signatories': [],
        'members': []
    }))

# MODIFIED_BY_YCN: post the PC group(s)
# 1. changed 'id' from 'auai.org/UAI/2018/Senior_Program_Committee/Invited' -> 'auai.org/UAI/2018/Program_Committee/Invited'
# 2. allows SPC to view who's been invited
client.post_group(openreview.Group(**{
        'id': 'auai.org/UAI/2018/Program_Committee/Invited',
        'readers': ['auai.org/UAI/2018','auai.org/UAI/2018/Program_Chairs', 'auai.org/UAI/2018/Senior_Program_Committee'],
        'writers': ['auai.org/UAI/2018'],
        'signatures': ['auai.org/UAI/2018'],
        'signatories': [],
        'members': []
    }))

# MODIFIED_BY_YCN: post the PC group(s)
# 1. changed 'id' from 'auai.org/UAI/2018/Senior_Program_Committee/Declined' -> 'auai.org/UAI/2018/Program_Committee/Declined'
# 2. allows SPC to view who's declined
client.post_group(openreview.Group(**{
        'id':'auai.org/UAI/2018/Program_Committee/Declined',
        'readers': ['auai.org/UAI/2018','auai.org/UAI/2018/Program_Chairs', 'auai.org/UAI/2018/Senior_Program_Committee'],
        'writers': ['auai.org/UAI/2018'],
        'signatures': ['auai.org/UAI/2018'],
        'signatories': [],
        'members': []
    }))


# MODIFIED_BY_YCN: Create Senior_Program_Committee recruitment invitation/form
# 1. changed 'id' from 'auai.org/UAI/2018/-/SPC_Invitation' -> 'auai.org/UAI/2018/-/PC_Invitation'
# 2. changed 'process' from '../process/recruitSPCProcess.js' -> '../process/recruitPCProcess.js'
# 3. changed 'web' from '../webfield/recruitSPCWebfield.js' -> '../webfield/recruitPCWebfield.js'
# 4. modified object name spc_invitation -> pc_invitation
pc_invitation = openreview.Invitation(**{
        'id': 'auai.org/UAI/2018/-/PC_Invitation',
        'readers': ['everyone'],
        'writers': ['auai.org/UAI/2018'],
        'signatures': ['auai.org/UAI/2018'],
        'process': '../process/recruitPCProcess.js',
        'web': '../webfield/recruitPCWebfield.js'
    })

pc_invitation.reply = {
    'content': {
        'email': {
            'description': 'email address',
            'order': 1,
            'value-regex': '.*@.*'
        },
        'key': {
            'description': 'Email key hash',
            'order': 2,
            'value-regex': '.{0,100}'
        },
        'response': {
            'description': 'Invitation response',
            'order': 3,
            'value-radio': ['Yes', 'No']
        }
    },
    'readers': {
        'values': ['OpenReview.net']
    },
    'signatures': {
        'values-regex': '\\(anonymous\\)'
    },
    'writers': {
        'values-regex': '\\(anonymous\\)'
    }
}

client.post_invitation(pc_invitation)
