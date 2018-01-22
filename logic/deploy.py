'''
    File name: deploy.py
    Author: Colten Krauter
    Date created: 1/21/2018
    Date last modified: 1/21/2018
    Python Version: 3.6
'''

from Deploy.util import slack
import subprocess

def pull(request):
    payload = request.get_json()

    # Check if there are any commits to pull
    if len(payload['commits']) > 0 and payload['commits'][0]['distinct'] == True:
        try:
            cmd_output = subprocess.check_output(['git', 'pull', 'origin', 'master'], cwd="../" + request.args.get('folder')).decode("utf-8") 
            slack.log(cmd_output)
            return {'msg': str(cmd_output)}

        except subprocess.CalledProcessError as error:
            return {'msg': str(error.output)}

    else:
        return {'msg': 'Nothing to commit'}
