'''
    File name: deploy.py
    Author: Colten Krauter
    Date created: 1/21/2018
    Date last modified: 1/21/2018
    Python Version: 3.6
'''

from Deploy import app, jsonify, request
from Deploy.util import slack, responder
from Deploy.config import config
from Deploy.logic import deploy as logic
import hmac, hashlib


def verify_hmac_hash(data, signature):
    github_secret = config.GITHUB_SECRET
    mac = hmac.new(github_secret.encode('utf-8'), msg=data, digestmod=hashlib.sha1)
    return hmac.compare_digest('sha1=' + mac.hexdigest(), signature)
        
@app.route("/payload/", methods=['POST'])
def github_payload():
    try:
        signature = request.headers.get('X-Hub-Signature')

        if verify_hmac_hash(request.data, signature):
            if request.headers.get('X-GitHub-Event') == "ping":
                return jsonify({'msg': 'Ping event successful'})

            if request.headers.get('X-GitHub-Event') == "push":
                return jsonify(logic.pull(request))

        else:
            slack.log()
            response, status = responder.response(code=401, message='Unable to verify secret key.')
            return jsonify(response), status

    except Exception as error:
        slack.log()
        response, status = responder.response(code=500, message='Internal error.')
        return jsonify(response), status
