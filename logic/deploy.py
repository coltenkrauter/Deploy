"""
    File name: deploy.py
    Author: Colten Krauter
    Date created: 1/21/2018
    Date last modified: 1/21/2018
    Python Version: 3.6
"""

from codepuller.util import slack,responder
from codepuller import config
import subprocess,pendulum

def pull(request,projectName):
    payload = request.get_json()

    name = ""
    username = ""
    email = ""
    timestamp = ""
    url = ""
    repository = ""

    if "repository" in payload and "full_name" in payload["repository"]:
        repository = "Repository: "+payload["repository"]["full_name"]+"\n"
        
    if "head_commit" in payload and payload["head_commit"]:
        
        head_commit = payload["head_commit"]

        if "committer" in head_commit:
            committer = payload["head_commit"]["committer"]
            if "name" in committer:
                name = "Committer: "+committer["name"]+"\n"
            if "username" in committer:
                username = "Username: "+committer["username"]+"\n"
            if "email" in committer:
                email = "Email: "+committer["email"]+"\n"

        if "timestamp" in head_commit:
            timestamp = "Timestamp: "+pendulum.parse(head_commit["timestamp"]).format("%m/%d/%Y %H:%M %p")+"\n"

        if "url" in head_commit:
            url = "Link: <"+head_commit["url"]+"|View Commit>\n"

    if "head_commit" in payload and "committer" in payload["head_commit"] and "email" in payload["head_commit"]["committer"]:
        name = "Committer: "+payload["head_commit"]["committer"]["name"]+"\n"
    
    message = "\n"+name+username+email+timestamp+ repository+url+"\n"
    
    # Check that project config exists
    if projectName in config.PROJECT:

        # Check if there are any commits to pull
        if len(payload["commits"]) > 0 and payload["commits"][0]["distinct"] == True:
            try:
                cmd_output = subprocess.check_output(["git","pull","origin",config.PROJECT[projectName]["branch"]],cwd=config.PROJECT[projectName]["directory"]).decode("utf-8") 
                slack.log(message+cmd_output)
                return responder.pack(code=0,description=str(cmd_output))

            except subprocess.CalledProcessError as error:
                slack.log(message+str(error.output))
                return responder.pack(code=131,description=str(error.output))
        else:
            return responder.pack(code=34,description="Nothing to commit")
    else:
        return responder.pack(code=34,description="Project not found")

# Edit responses to use responder