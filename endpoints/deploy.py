from Deploy import app, jsonify, request
from Deploy.util import logger, sanitizer, responder
from Deploy.logic import deploy as logic
from Deploy.config import config

import hmac
import hashlib
import subprocess
import os

def verify_hmac_hash(data, signature):
    github_secret = bytes(config.GITHUB_SECRET, 'UTF-8')
    mac = hmac.new(github_secret, msg=data, digestmod=hashlib.sha1)
    return hmac.compare_digest('sha1=' + mac.hexdigest(), signature)
        
# export GITHUB_SECRET=secret

@app.route("/payload/", methods=['POST'])
def github_payload():
    return jsonify({'msg': 'invalid hash'})
