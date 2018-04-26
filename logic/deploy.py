'''
    File name: deploy.py
    Author: Colten Krauter
    Date created: 1/21/2018
    Date last modified: 1/21/2018
    Python Version: 3.6
'''

from codepuller.util import slack
import subprocess, pendulum

def pull(request):
    payload = request.get_json()

    name = ''
    username = ''
    email = ''
    timestamp = ''
    url = ''
    repository = ''
    repositoryFullName = ''

    if 'repository' not in payload or 'name' not in payload['repository']:
        return {'msg': 'Repository name missing'}
    
    repository = payload['repository']['name']

    if 'repository' in payload and 'full_name' in payload['repository']:
        repositoryFullName = 'Repository: ' + payload['repository']['full_name'] + '\n'
        
    if 'head_commit' in payload and payload['head_commit']:
        
        head_commit = payload['head_commit']

        if 'committer' in head_commit:
            committer = payload['head_commit']['committer']
            if 'name' in committer:
                name = 'Committer: ' + committer['name'] + '\n'
            if 'username' in committer:
                username = 'Username: ' + committer['username'] + '\n'
            if 'email' in committer:
                email = 'Email: ' + committer['email'] + '\n'

        if 'timestamp' in head_commit:
            timestamp = 'Timestamp: ' + pendulum.parse(head_commit['timestamp']).format('%m/%d/%Y %H:%M %p') + '\n'

        if 'url' in head_commit:
            url = 'Link: <' + head_commit['url'] + '|View Commit>\n'

    if 'head_commit' in payload and 'committer' in payload['head_commit'] and 'email' in payload['head_commit']['committer']:
        name = 'Committer: '+payload['head_commit']['committer']['name'] + '\n'
    
    message = name + username + email + timestamp +  repositoryFullName + url + '\n'
    
    # Check if there are any commits to pull
    if len(payload['commits']) > 0 and payload['commits'][0]['distinct'] == True:
        try:
            cmd_output = subprocess.check_output(['git', 'pull', 'origin', 'master'], cwd="../" + repository).decode("utf-8") 
            slack.log(message + cmd_output)
            return {'msg': str(cmd_output)}

        except subprocess.CalledProcessError as error:
            slack.log(message + error.output)
            return {'msg': str(error.output)}

    else:
        slack.log(message + 'Nothing to commit')
        return {'msg': 'Nothing to commit'}
