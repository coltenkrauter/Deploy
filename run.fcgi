#!/home4/specica9/public_html/Python-GitHub-Webhooks/deploy-venv/bin/python
import sys
sys.path.insert(0, '/home4/specica9/public_html')

from flup.server.fcgi import WSGIServer
from Deploy import app as application

WSGIServer(application).run()