import sys, os, inspect
from subprocess import call

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
