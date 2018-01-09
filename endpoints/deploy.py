from Deploy import app, jsonify, request
from Deploy.util import logger, sanitizer, responder
from Deploy.config import config

import hmac
import hashlib
import subprocess
import os

def verify_hmac_hash(data, signature):
    data_to_sign = str(data)
    signature_to_sign = signature.encode('utf-8')
    mac = hmac.new(config.GITHUB_SECRET, data_to_sign, hashlib.sha1)
    logger.log('sha1=' + mac.hexdigest())
    return hmac.compare_digest('sha1=' + mac.hexdigest(), signature_to_sign)

@app.route("/payload/", methods=['POST'])
def github_payload():
    try:
        signature = request.headers.get('X-Hub-Signature')
        logger.log(signature)
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
            logger.log()
            response, status = responder.response(code=401, message='Unable to verify secret key.')
            return jsonify(response), status
    except Exception as error:
        logger.log()
        response, status = responder.response(code=500, message='Internal error.')
        return jsonify(response), status
