def process(client, note, invitation):

    paper_link = note.content['paper_link']
    paper_forum = paper_link.split('=')[-1]

    try:
        arr_submission = client.get_note(paper_forum)
    except openreview.OpenReviewException as e:
        raise openreview.OpenReviewException('Provided paper link does not correspond to a submission in OpenReview')

    if ('aclweb.org/ACL/ARR/2021' not in arr_submission.invitation) and ('aclweb.org/ACL/ARR/2022' not in arr_submission.invitation):
        raise openreview.OpenReviewException('Provided paper link does not correspond to an ARR submission')
