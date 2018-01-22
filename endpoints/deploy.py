from Deploy import app, jsonify, request
from Deploy.util import slack, sanitizer, responder
from Deploy.config import config

import hmac
import hashlib
import subprocess

def verify_hmac_hash(data, signature):
    github_secret = config.GITHUB_SECRET
    mac = hmac.new(github_secret.encode('utf-8'), msg=data, digestmod=hashlib.sha1)
    return hmac.compare_digest('sha1=' + mac.hexdigest(), signature)
        
@app.route("/payload/", methods=['POST'])
def github_payload():
    try:
        signature = request.headers.get('X-Hub-Signature')
        data = request.data

        if verify_hmac_hash(data, signature):
            if request.headers.get('X-GitHub-Event') == "ping":
                return jsonify({'msg': 'Ping event successful'})
            if request.headers.get('X-GitHub-Event') == "push":
                payload = request.get_json()

                # Check if there are any commits to pull
                if payload['commits'][0]['distinct'] == True:
                    try:
                        cmd_output = subprocess.check_output(['git', 'pull', 'origin', 'master'], cwd="../" + request.args.get('folder'))
                        slack.log(cmd_output)
                        return jsonify({'msg': str(cmd_output)})
                    except subprocess.CalledProcessError as error:
        
                        return jsonify({'msg': str(error.output)})
                else:
                    return jsonify({'msg': 'Nothing to commit'})

        else:
            slack.log()
            response, status = responder.response(code=401, message='Unable to verify secret key.')
            return jsonify(response), status
    except Exception as error:
        slack.log()
        response, status = responder.response(code=500, message='Internal error.')
        return jsonify(response), status
