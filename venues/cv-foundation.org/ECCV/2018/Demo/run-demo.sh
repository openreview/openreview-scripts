#!/bin/bash

python python/setup-demo.py
python python/precreate-profiles.py
python python/submit-papers.py
config_id=$(python python/generate-metadata.py)
python ~/projects/openreview/openreview-scripts/admin/match.py $config_id
