# Thanks tomdaley92 for the simple slack logging solution with traceback
# Credit: https://github.com/tomdaley92

import requests
import traceback
from Deploy.config import config


def log(message = None):
    data = { 'text' : '```'+traceback.format_exc()+'```' }

    if message:
        data = { 'text' : '```'+str(message)+'```' }
        
    requests.post(config.SLACK_WEBHOOK_DEPLOY, json=data)
    