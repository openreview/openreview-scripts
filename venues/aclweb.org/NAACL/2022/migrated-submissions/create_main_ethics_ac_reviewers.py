# Just here for reference, removed them from reviewer_ac_groups because they shouldn't be created every time 
# Create Ethics AC group 
ethics = client.post_group(openreview.Group(
    id = 'aclweb.org/ACL/2022/Conference/Ethics_Chairs',
    signatures = [
        'aclweb.org/ACL/2022/Conference'
        ],
    signatories=[
        'aclweb.org/ACL/2022/Conference',
        'aclweb.org/ACL/2022/Conference/Ethics_Chairs'
        ],
    readers = [
        'aclweb.org/ACL/2022/Conference',
        'aclweb.org/ACL/2022/Conference/Ethics_Chairs'
    ],
    writers = [
            'aclweb.org/ACL/2022/Conference'
            ],
    members = [

    ]
))
# Create Ethics Reviewers Group 
ethics_reviewers = client.post_group(openreview.Group(
        id = f'aclweb.org/ACL/2022/Conference/Ethics_Reviewers',
        signatures = [
            'aclweb.org/ACL/2022/Conference'
            ],
        signatories=[
            'aclweb.org/ACL/2022/Conference'
            ],
        readers = [
            'aclweb.org/ACL/2022/Conference/Ethics_Chairs',
            'aclweb.org/ACL/2022/Conference/Ethics_Reviewers',
            'aclweb.org/ACL/2022/Conference'
            ],
        writers = [
            'aclweb.org/ACL/2022/Conference'
             ]
        ))