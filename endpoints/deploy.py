from Deploy import app, jsonify, request
from Deploy.util import slack, sanitizer, responder
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
                return logic.pull(request.get_json())

        else:
            slack.log()
            response, status = responder.response(code=401, message='Unable to verify secret key.')
            return jsonify(response), status

    except Exception as error:
        slack.log()
        response, status = responder.response(code=500, message='Internal error.')
        return jsonify(response), status
