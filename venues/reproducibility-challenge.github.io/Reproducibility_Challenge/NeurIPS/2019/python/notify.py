
import argparse
import datetime
import openreview
from openreview import tools

parser = argparse.ArgumentParser()
parser.add_argument('--baseurl', help="base url")
parser.add_argument('--username')
parser.add_argument('--password')
parser.add_argument('--freq', required=True, help="Daily or Weekly")
parser.add_argument('--notify_author', default=False)
args = parser.parse_args()

client = openreview.Client(baseurl=args.baseurl, username=args.username, password=args.password)
print("Connected to "+client.baseurl)
conference_id = 'NeurIPS.cc/2019/Reproducibility_Challenge'

def get_author_id(forumNote):
    # get submission author and add to email list if author hasn't set a notification tag
    profile = None
    # if there is a primary author email, and it is not on the list already, add it
    author_email = next(s for s in forumNote.content['authorids'] if s)
    if author_email:
        try:
            profile = client.get_profile(forumNote.content['authorids'][0])
        except openreview.OpenReviewException as e:
            # throw an error if it is something other than "not found"
            if e.args[0][0] != 'Profile not found':
                raise e
        if profile:
            return profile.id
        else:
            # if submission author doesn't have profile, add email to email_list
            return author_email
    return None


# load recent comments
min_date = datetime.datetime.utcnow().timestamp()*1000
if args.freq == "Daily":
    min_date -= 24*60*60*1000
elif args.freq == "Weekly":
    min_date -= 7*24*60*60*1000
else:
    print("Invalid freq: "+args.freq)
    quit()

comments = tools.iterget_notes(client, mintcdate = min_date, invitation = conference_id+'/.*/-/Comment')
comment_by_forum = {}
for comment in comments:
    if comment.forum not in comment_by_forum:
        comment_by_forum[comment.forum] = []
    comment_by_forum[comment.forum].append(comment)

for forum in comment_by_forum.keys():
    forumNote = client.get_note(id=forum)
    # get all notification tags for this paper
    tags = tools.iterget_tags(client, invitation=conference_id+'/-/Notification_Subscription', forum = forum, tag=args.freq)
    email_list = [tag.signatures[0] for tag in tags]

    if args.notify_author:
        # add paper author if they haven't set a notification frequency
        author_id = get_author_id(forumNote)
        notify = client.get_tags(invitation=conference_id+'/-/Notification_Subscription', forum=forum, signature=author_id)
        if author_id and not notify:
            email_list.append(author_id)

    if email_list:
        # get paper info
        subject = '[NeurIPS Reproducibility Challenge] Paper Title: "' + forumNote.content['title'] + '" comment ' + args.freq + ' report'
        message = 'NeurIPS paper "'+forumNote.content['title']+'" received the following comments: \n\n'
        # show at most 3 comments
        max_comment = 3
        # assemble all comments into text
        comment_index = 0
        for comment in comment_by_forum[forum][:max_comment]:
            message += "  "+comment.signatures[0]+" - "+comment.content['title']+"\n  Comment: " + comment.content['comment']+"\n\n"
            comment_index += 1

        if comment_index >= max_comment:
            message += "  ...\n\n"

        message += 'To view all comments, click here: https://openreview.net/forum?id=' + forum
        message += '\n\nIf you wish to change your email notification preferences for comments on this paper, log into OpenReview.net, visit the link above and change the Notification Subscription frequency.'
        message += '\nIf you do not have an OpenReview account and want to stop receiving this email, send "Unsubscribe" to info@openreview.net'
        print(email_list)
        print('Subject:'+subject)
        print('Body:'+message)
        client.send_mail(subject, email_list, message)