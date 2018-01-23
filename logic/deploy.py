'''
    File name: deploy.py
    Author: Colten Krauter
    Date created: 1/21/2018
    Date last modified: 1/21/2018
    Python Version: 3.6
'''

from Deploy.util import slack
import subprocess, pendulum

def pull(request):
    payload = request.get_json()

    username = ''
    email = ''
    timestamp = ''

    if 'repository' not in payload or 'name' not in payload['repository']:
        return {'msg': 'Repository name missing'}

    if 'head_commit' in payload:
        
        head_commit = payload['head_commit']

        if 'committer' in head_commit:
            committer = payload['head_commit']['committer']
            if 'username' in committer:
                username = 'Committer: ' + committer['username'] + '\n'
            if 'email' in committer:
                email = 'Email: ' + committer['email'] + '\n'

        if 'timestamp' in head_commit:
            timestamp = 'Timestamp: ' + pendulum.parse(head_commit['timestamp']).format('%m/%d/%Y %H:%M %p') + '\n'

    if 'head_commit' in payload and 'committer' in payload['head_commit'] and 'email' in payload['head_commit']['committer']:
        username = 'Committer: '+payload['head_commit']['committer']['username'] + '\n'
    
    repository = payload['repository']['name']

    info = username + email + timestamp + 'Repository: ' + repository + '\n\n'
    
    # Check if there are any commits to pull
    if len(payload['commits']) > 0 and payload['commits'][0]['distinct'] == True:
        try:
            cmd_output = subprocess.check_output(['git', 'pull', 'origin', 'master'], cwd="../" + repository).decode("utf-8") 
            slack.log(info + cmd_output)
            return {'msg': str(cmd_output)}

        except subprocess.CalledProcessError as error:
            slack.log(info + error.output)
            return {'msg': str(error.output)}

    else:
        slack.log(info + 'Nothing to commit')
        return {'msg': 'Nothing to commit'}
