
# coding: utf-8

# In[1]:


import openreview
from openreview import tools
import config
import functions

client = openreview.Client()
print client.baseurl


# In[3]:


'''
Post the reviewer groups. Warning! This will reset all members! 

TODO: make a function to post a group without overwriting members.
'''
reviewers = client.post_group(config.REVIEWERS)
reviewers_invited = client.post_group(config.REVIEWERS_INVITED)
reviewers_declined = client.post_group(config.REVIEWERS_DECLINED)


# In[4]:


'''
Post the recruitment invitation. This can be done multiple times without consequence.
'''
recruit_reviewers = client.post_invitation(config.RECRUIT_REVIEWERS)


# In[5]:


'''
Example of how to invite a reviewer.
'''

functions.recruit_reviewer(client, 'michael.l.spector@gmail.com', 'Michael')

