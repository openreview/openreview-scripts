def process(client, edge, invitation):

    print(edge.id)

    if edge.ddate is None:

        ## Get the submission
        submission = client.get_note(id=edge.head)

        ## - Get profile
        user = edge.tail
        print(f'Get profile for {user}')
        user_profile=openreview.tools.get_profiles(client, [user], with_publications=True)[0]

        print(f'Check conflicts for {user_profile.id}')
        ## - Check conflicts
        authors = client.get_group(f'aclweb.org/ACL/2022/Conference/Paper{submission.number}/Authors')
        author_profiles = openreview.tools.get_profiles(client, authors.members, with_publications=True)
        conflicts=openreview.tools.get_conflicts(author_profiles, user_profile, policy = 'neurips', n_years=5)
        if conflicts:
            print('Conflicts detected', conflicts)
            raise openreview.OpenReviewException(f'Conflict detected for {user_profile.get_preferred_name(pretty=True)}')

    return edge



