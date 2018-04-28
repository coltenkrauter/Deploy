'''
    File name: deploy.py
    Author: Colten Krauter
    Date created: 1/21/2018
    Date last modified: 1/21/2018
    Python Version: 3.6
'''

from codepuller import app, jsonify, request, config
from codepuller.util import slack, responder
from codepuller.logic import deploy as logic
import hmac, hashlib


def verify_hmac_hash(data, signature):
    github_secret = config.GITHUB_SECRET
    mac = hmac.new(github_secret.encode('utf-8'), msg=data, digestmod=hashlib.sha1)
    return hmac.compare_digest('sha1=' + mac.hexdigest(), signature)
        
@app.route("/pull/<projectName>", methods=['POST'])
def github_payload(projectName):
    try:
        signature = request.headers.get('X-Hub-Signature')

        if signature and verify_hmac_hash(request.data, signature):
            if request.headers.get('X-GitHub-Event') == "ping":
                response, status = responder.pack(code=0,description="Ping event successful.")
                return jsonify(response), status

            if request.headers.get('X-GitHub-Event') == "push":
                response = logic.pull(request,projectName)
                response, status = responder.pack(code=0,response=response)
                return jsonify(response), status

        else:
            response, status = responder.pack(code=32,description="Unable to verify secret key.")
            return jsonify(response), status

    except Exception as error:
        slack.log()
        # Internal error
        response, status = responder.pack(131)
        return jsonify(response), status
