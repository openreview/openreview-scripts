'''

This is a one-time script that should be run to convert the conference to the new withdrawal protocol.

'''

import openreview
import config
import csv
client = openreview.Client()
print client.baseurl

# set up the new withdrawal procedure

# re-post the submission invitation (slow)
client.post_invitation(openreview.Invitation(config.SUBMISSION, duedate=config.DUE_TIMESTAMP, **config.submission_params))

# post the withdrawn submissions invitation
client.post_invitation(openreview.Invitation(config.WITHDRAWN_SUBMISSION, **config.withdrawn_submission_params))

# find all the improperly withdrawn notes
blinded = client.get_notes(invitation=config.BLIND_SUBMISSION)
withdrawn_blinded = [n for n in blinded if 'withdrawal' in n.content]
for w in withdrawn_blinded:
    print w.id, w.content['title']

# for all blinded notes, update the withdraw paper invitation
for n in blinded:
    withdraw_inv = client.get_invitation('ICLR.cc/2018/Conference/-/Paper{0}/Withdraw_Paper'.format(n.number))
    with open('../process/withdrawProcess_delete.js') as f:
        withdraw_inv.process = f.read()
    withdraw_inv.reply['content']['withdrawal']['description'] = 'Confirm your withdrawal. The blind record of your paper will be deleted. Your identity will NOT be revealed. This cannot be undone.'
    client.post_invitation(withdraw_inv)

# for each of these notes, set the ddate to be the date that the withdrawal was made:
for n in withdrawn_blinded:
    rev = client.get_revisions(n.id)
    withdrawals = [r for r in rev if 'Withdraw_Paper' in r.invitation]
    ddate = sorted([w.cdate for w in withdrawals])[0]
    print ddate
    n.ddate = ddate
    client.post_note(n)

# update webfield
conference = client.get_group(config.CONF)
conference.add_webfield('../webfield/conferenceWebfield_alt.js')
client.post_group(conference)
