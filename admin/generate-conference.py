# For now, run this script from /openreview-scripts

import sys, os, shutil
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../utils"))
import utils
import templates

conference = raw_input("Enter the full path of the conference group you would like to create (e.g. my-conferece.org/MYCONF/2017): ")
directory = utils.get_path('../venues/%s' % conference, __file__)
submission_name = raw_input("Enter the name of the submission (e.g. \"Submission\"): " )
duedate = raw_input("Enter the duedate, in milliseconds, of the submission (e.g. 1524846935000): ")

assert not os.path.exists(directory)

os.makedirs(directory)
os.makedirs(directory + '/python')
os.makedirs(directory + '/webfield')
os.makedirs(directory + '/process')
os.makedirs(directory + '/data')

with open(directory + '/python/config.py', 'w') as new_configfile, open(utils.get_path('./conference-template/python/config.template', __file__)) as template_configfile:
	templatestring = template_configfile.read().replace('<<CONF>>', "\"%s\"" % conference)
	templatestring = templatestring.replace('<<UTILS_DIR>>', "\"%s\"" % utils.get_path('../utils', __file__))
	new_configfile.write(templatestring)

with open(directory + '/webfield/conf.html', 'w') as webfile:
	web_params = {
		"header": "This is the header",
		"title": "This is the title",
		"info": "This is the info",
		"url": "www.thisistheurl.com",
		"invitation": "%s/-/%s" % (conference, submission_name)
	}

	webfield = templates.Webfield(web_params)

	webfile.write(webfield.html)

with open(directory + '/python/superuser-init.py', 'w') as new_initfile, open(utils.get_path('./conference-template/python/superuser-init.template', __file__)) as template_initfile:
	templatestring = template_initfile.read().replace('<<UTILS_DIR>>', "\"%s\"" % utils.get_path('../utils', __file__))
	templatestring = templatestring.replace('<<SUBMISSION_DUEDATE>>', "\"%s\"" % duedate)
	new_initfile.write(templatestring)
