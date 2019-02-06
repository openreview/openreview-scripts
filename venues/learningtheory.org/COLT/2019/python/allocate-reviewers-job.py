import openreview
import config

client = openreview.Client()
conference = config.get_conference(client)

reviewer_groups = list(openreview.tools.iterget_groups(client, '{}/Paper.*/Reviewers'.format(conference.id)))

for r in reviewer_groups:
    if not any([suffix in r.id for suffix in ['/Invited', '/Declined']]):
        components = r.id.split('/')
        paper_num_string = components[4]
        number = int(paper_num_string.replace('Paper',''))

        for member in r.members:
            print(member)
            assigned_user, assigned_groups = openreview.tools.assign(client=client,
                conference='learningtheory.org/COLT/2019/Conference',
                paper_number=number,
                reviewer_to_add=member,
                parent_label = 'Reviewers',
                individual_label = 'AnonReviewer',
                individual_group_params = {
                   'readers': [
                       'learningtheory.org/COLT/2019/Conference',
                       'learningtheory.org/COLT/2019/Conference/Program_Chairs',
                       'learningtheory.org/COLT/2019/Conference/Paper{}/Program_Committee'.format(number)
                   ],
               },
                parent_group_params = {
                   'readers': [
                       'learningtheory.org/COLT/2019/Conference',
                       'learningtheory.org/COLT/2019/Conference/Program_Chairs',
                       'learningtheory.org/COLT/2019/Conference/Paper{}/Program_Committee'.format(number)
                   ]
               },
                use_profile=False)

            print('assignment', assigned_user, assigned_groups)
