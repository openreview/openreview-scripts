import sys
import os
sys.path.append('../..')
from client import *

openreview = Client()

groups = openreview.get_groups(prefix="ICLR.cc/2017")