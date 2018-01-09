from Deploy import app, jsonify, request
from Deploy.util import logger, sanitizer
from Deploy.logic import deploy as logic

@app.route('/', methods=['POST'])
def deploy():
    return jsonify(logic.deploy(sanitizer.sanitize(request.json), request.args.get('path')))



import hmac
import hashlib
import subprocess
import os

def verify_hmac_hash(data, signature):
    github_secret = bytes(os.environ['GITHUB_SECRET'], 'UTF-8')
    mac = hmac.new(github_secret, msg=data, digestmod=hashlib.sha1)
    return hmac.compare_digest('sha1=' + mac.hexdigest(), signature)

# export GITHUB_SECRET=secret

@app.route("/payload/", methods=['POST'])
def github_payload():
    return jsonify({'msg': 'invalid hash'})