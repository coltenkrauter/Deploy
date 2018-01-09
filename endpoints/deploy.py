from Deploy import app, jsonify, request
from Deploy.util import logger, sanitizer, responder
from Deploy.logic import deploy as logic

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
    try:
        signature = request.headers.get('X-Hub-Signature')
        data = request.data
        if verify_hmac_hash(data, signature):
            if request.headers.get('X-GitHub-Event') == "ping":
                return jsonify({'msg': 'Ok'})
            if request.headers.get('X-GitHub-Event') == "push":
                payload = request.get_json()
                if payload['commits'][0]['distinct'] == True:
                    try:
                        cmd_output = subprocess.check_output(
                            ['git', 'pull', 'origin', 'master'],)
                        
                        return jsonify({'msg': str(cmd_output)})
                    except subprocess.CalledProcessError as error:
        
                        return jsonify({'msg': str(error.output)})
                else:
                    return jsonify({'msg': 'nothing to commit'})

        else:
            return jsonify({'msg': 'invalid hash'})
    except Exception as error:
        
        return jsonify(responder.response(code=401, message='Unable to verify secret key.'))
