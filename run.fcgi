#!/home4/specica9/public_html/coltenkrauter/dev/codepuller/venv/bin/python
# This file is for running a flask instance of the codepuller api

import sys
import os

# Add api package to the path
path = os.path.dirname(sys.modules[__name__].__file__)
path = os.path.join(path, '..')
sys.path.insert(0, path)

from flup.server.fcgi import WSGIServer
from codepuller import app as application

WSGIServer(application).run()