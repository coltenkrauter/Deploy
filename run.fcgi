#!/home4/specica9/public_html/PythonGitHubWebhooks/deploy-venv/bin/python
import sys
sys.path.insert(0, '/home4/specica9/public_html')

from flup.server.fcgi import WSGIServer
from PythonGitHubWebhooks import app as application

WSGIServer(application).run()