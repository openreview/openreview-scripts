import openreview
import sys, os
import config

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../../utils"))
import utils
import templates

params = {
	"header": "This is the header",
	"title": "This is the title",
	"info": "This is the info",
	"url": "www.thisistheurl.com",
	"invitation": "sample.conference/-/Submission"
}
args, parser, overwrite = utils.parse_args()
client = openreview.Client(baseurl=args.baseurl, username=args.username, password=args.password)
submissionReply = templates.SubmissionReply(params = {'forum': 'some_random_forum'})

submission_inv = openreview.Invitation(config.SUBMISSION, **config.invitation_params)

submission_inv.reply = templates.SubmissionReply().body

posted_inv = client.post_invitation(submission_inv)
print posted_inv.reply
