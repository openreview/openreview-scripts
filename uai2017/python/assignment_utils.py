def single_assignment_valid(s):
    try:
        user, paper_number= s.split(',')

        try:
            int(paper_number)
        except ValueError:
            return False

        if not '@' in user and not '~' in user:
            return False

        return True
    except IndexError:
        return False

def get_nonreaders(paper_number, client):
    # nonreaders are a list of all domain groups of the authors of the paper

    authors = client.get_group('auai.org/UAI/2017/Paper%s/Authors' % paper_number)
    conflicts = set()
    for author in authors.members:
        try:
            author_members = client.get_groups(member=author)
            member_domains = [d.id for d in author_members if '@' in d.id]
            conflicts.update([p.split('@')[1] for p in member_domains])

            author_profile = client.get_profile(author)
            conflicts.update([p.split('@')[1] for p in author_profile.content['emails']])
            conflicts.update([p['institution']['domain'] for p in author_profile.content['history']])

        except openreview.OpenReviewException:
            pass

    if 'gmail.com' in conflicts: conflicts.remove('gmail.com')

    return list(conflicts)
