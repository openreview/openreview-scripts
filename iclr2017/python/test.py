import sys
import os
from openreview import *

openreview = Client()

groups = openreview.get_groups(prefix="ICLR.cc/2017")