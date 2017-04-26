import sys, os, inspect
from subprocess import call
import argparse

def process_to_file(templatefile, outdir, suffix=None):
    params = [
        "node",
        os.path.join(os.path.dirname(__file__), "processToFile.js"),
        templatefile,
        outdir
    ]
    if suffix: params.append(suffix)
    call(params)

def get_path(rel_path, _file):
    return os.path.abspath(os.path.join(os.path.dirname(_file), rel_path))

def parse_args():
	parser = argparse.ArgumentParser()
	parser.add_argument('--baseurl', help="base URL")
	parser.add_argument('--overwrite', help="If set to true, overwrites existing groups")
	parser.add_argument('--username')
	parser.add_argument('--password')

	args = parser.parse_args()

	overwrite = True if (args.overwrite!=None and args.overwrite.lower()=='true') else False

	return args, parser, overwrite
