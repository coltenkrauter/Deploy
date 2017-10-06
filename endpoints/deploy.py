from Deploy import app, jsonify, request
from Deploy.util import logger, sanitizer
from Deploy.logic import deploy as logic

@app.route('/', methods=['POST'])
def deploy():
    return jsonify(logic.deploy(sanitizer.sanitize(request.json), request.args.get('path')))

