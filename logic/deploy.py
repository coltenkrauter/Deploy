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

    username = ''

    if not payload['repository'] or not payload['repository']['name']:
        return {'msg': 'Repository name missing'}
    if payload['committer'] or payload['committer']['username']:
        username = 'Committed by '+payload['committer']['username']+'\n'
    
    repository = payload['repository']['name']

    slack.log(username + 'Repository: '+repository)
    
    # Check if there are any commits to pull
    if len(payload['commits']) > 0 and payload['commits'][0]['distinct'] == True:
        try:
            cmd_output = subprocess.check_output(['git', 'pull', 'origin', 'master'], cwd="../" + repository).decode("utf-8") 
            slack.log(cmd_output)
            return {'msg': str(cmd_output)}

        except subprocess.CalledProcessError as error:
            return {'msg': str(error.output)}

    else:
        slack.log('Nothing to commit')
        return {'msg': 'Nothing to commit'}
