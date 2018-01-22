from Deploy.util import slack
import subprocess

def pull(request):
    payload = request.get_json()
    
    # Check if there are any commits to pull
    if payload['commits'][0]['distinct'] == True:
        try:
            cmd_output = subprocess.check_output(['git', 'pull', 'origin', 'master'], cwd="../" + request.args.get('folder')).decode("utf-8") 
            slack.log(cmd_output)
            return jsonify({'msg': str(cmd_output)})

        except subprocess.CalledProcessError as error:
            return jsonify({'msg': str(error.output)})

    else:
        return {'msg': 'Nothing to commit'}