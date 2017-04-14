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
            conflicts.update(get_user_domains(author, client))

        except openreview.OpenReviewException:
            pass

    if 'gmail.com' in conflicts: conflicts.remove('gmail.com')

    return conflicts


def get_user_domains(user, client):

    domains = set()
    members = client.get_groups(member = user)
    member_domains = [d.id for d in members if '@' in d.id]
    domains.update([p.split('@')[1] for p in member_domains])

    profile = client.get_profile(user)
    domains.update([p.split('@')[1] for p in profile.content['emails']])
    domains.update([p['institution']['domain'] for p in profile.content['history']])

    return domains
