# For now, run this script from /openreview-scripts

import sys, os, shutil
import utils
import argparse
import datetime

parser = argparse.ArgumentParser()
parser.add_argument('--overwrite', action='store_true', help="if true, overwrites the conference directory")
args = parser.parse_args()


conference = raw_input("Enter the full path of the conference group you would like to create (e.g. my-conference.org/MYCONF/2017): ")
conference_title = raw_input("Enter the title of this conference (this will appear at the top of the homepage): ")
conference_subtitle = raw_input("Enter the subtitle of this conference (this will appear just below the title): ")
conference_location = raw_input("Enter the location of the conference: ")
conference_date = raw_input("Enter date of the conference in human-readable form:")
human_duedate = raw_input("Enter the human-readable due date string that will appear on the homepage (this will have no effect on the system due date): ")
url = raw_input("Enter the conference URL: ")
print "When users submit a paper, they will receive an email. Fill in the blank below: "
conference_phrase = raw_input("Your submission to ______ has been received. ")
directory = utils.get_path('../venues/%s' % conference, __file__)
submission_name = raw_input("Enter the name of the submission (press enter for default: \"Submission\"): " )

if submission_name.strip() == '':
	submission_name = "Submission"

# check if due date/time is valid and after current time
duedate_input = raw_input("Enter the duedate (DD/MM/YYYY): ")
try:
	day, month, year = duedate_input.split('/')
	day = int(day)
	month = int(month)
	year = int(year)
	# this will catch invalid values for date
	duedate = utils.get_duedate(year, month, day)
	now = datetime.datetime.now()
	assert duedate > now, "Cannot enter a date in the past"

	# get due time
	duetime_input = raw_input(
		"Enter the time of day that the \"%s\" is due in 24-hour format (e.g. enter 23:59 for 11:59 pm): " % submission_name)
	hour, minute = duetime_input.split(':')
	hour = int(hour)
	minute = int(minute)
	duedate = utils.get_duedate(year, month, day, hour, minute)
	assert duedate > now, "Cannot enter a time in the past"
except Exception, e:
	print "Duedate invalid: ", e
	sys.exit()

duedate_milliseconds = utils.date_to_timestamp(duedate)

if not args.overwrite: assert not os.path.exists(directory), "%s already exists" % conference

print "Creating conference directory at %s" % directory

makedir = lambda d: os.makedirs(d) if not os.path.exists(d) else None

makedir(directory)
makedir(directory + '/python')
makedir(directory + '/webfield')
makedir(directory + '/process')
makedir(directory + '/data')

print "writing %s/python/config.py" % directory
with open(directory + '/python/config.py', 'w') as new_configfile, open(utils.get_path('./conference-template/python/config.template', __file__)) as template_configfile:
	templatestring = template_configfile.read().replace('<<CONF>>', "\"%s\"" % conference)
	templatestring = templatestring.replace('<<SUBMISSION_NAME>>',submission_name)
	templatestring = templatestring.replace('<<TIMESTAMP>>',str(duedate_milliseconds))
	new_configfile.write(templatestring)

print "writing %s/webfield/conf.html" % directory
with open(directory + '/webfield/conf.html', 'w') as new_webfile, open(utils.get_path('./conference-template/webfield/conf.template',__file__)) as template_webfile:
	templatestring = template_webfile.read().replace('<<TITLE>>',"\"%s\"" % conference_title)
	templatestring = templatestring.replace('<<CONF>>',"\"%s\"" % conference)
	templatestring = templatestring.replace('<<SUBMISSION_NAME>>', submission_name)
	templatestring = templatestring.replace('<<SUBTITLE>>',"\"%s\"" % conference_subtitle)
	templatestring = templatestring.replace('<<LOCATION>>',"\"%s\"" % conference_location)
	templatestring = templatestring.replace('<<CONF_DATE>>',"\"%s\"" % conference_date)
	templatestring = templatestring.replace('<<DATE>>',"%s" % human_duedate)
	templatestring = templatestring.replace('<<URL>>',"\"%s\"" % url)
	new_webfile.write(templatestring)

print "writing %s/python/admin-init.py" % directory
with open(directory + '/python/admin-init.py', 'w') as new_initfile, open(utils.get_path('./conference-template/python/admin-init.template', __file__)) as template_initfile:
	templatestring = template_initfile.read().replace('<<SUBMISSION_DUEDATE>>', "%s" % duedate_milliseconds)
	new_initfile.write(templatestring)

print "writing %s/process/submissionProcess.template" % directory
with open(directory + '/process/submissionProcess.template', 'w') as new_submissionprocess, open(utils.get_path('./conference-template/process/submissionProcess.template', __file__)) as template_submissionprocess:
	templatestring = template_submissionprocess.read().replace('<<CONF>>', "\"%s\"" % conference)
	templatestring = templatestring.replace('<<PHRASE>>', "\"%s\"" % conference_phrase)
	new_submissionprocess.write(templatestring)

print "writing %s/process/commentProcess.js" % directory
with open(directory + '/process/commentProcess.js', 'w') as new_commentprocess, open(utils.get_path('./conference-template/process/commentProcess.template', __file__)) as template_commentprocess:
	templatestring = template_commentprocess.read().replace('<<PHRASE>>', "\"%s\"" % conference_phrase)
	new_commentprocess.write(templatestring)
