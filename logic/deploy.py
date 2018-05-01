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

    name = None
    avatar = None
    timestamp = None
    commit = None
    commitUrl = None
    repo = None
    repoUrl = None
    priority = "information"

    if "repository" in payload:
        repository = payload["repository"]

        if "full_name" in repository:
            repo = repository["full_name"]
            repoUrl = "https://github.com/"+repo

        if "owner" in repository:
            if "avatar_url" in repository["owner"]:
                avatar = repository["owner"]["avatar_url"]
        
    if "head_commit" in payload and payload["head_commit"]:
        headCommit = payload["head_commit"]

        if "committer" in headCommit:
            committer = headCommit["committer"]

            if "name" in committer:
                name = committer["name"]

            # if "username" in committer:
                # username = committer["username"]
            # if "email" in committer:
                # email = committer["email"]

        if "timestamp" in headCommit:
            timestamp = headCommit["timestamp"]

        if "url" in headCommit:
            commit = headCommit["id"]
            commitUrl = headCommit["url"]
    
    # Check that project config exists
    if projectName in config.PROJECT:

        # Check if there are any commits to pull
        if len(payload["commits"]) > 0 and payload["commits"][0]["distinct"] == True:
            try:
                cmd_output = subprocess.check_output(["git","pull","origin",config.PROJECT[projectName]["branch"]],cwd=config.PROJECT[projectName]["directory"]).decode("utf-8") 
                slack.log(
                    text=str(cmd_output),
                    name=name,
                    avatar=avatar,
                    timestamp=timestamp,
                    repo=repo,
                    repoUrl=repoUrl,
                    commit=commit,
                    commitUrl=commitUrl,
                    priority="success"
                )
                return responder.pack(code=0,description=str(cmd_output))

            except subprocess.CalledProcessError as error:
                slack.log(text=str(error.output),priority="error")
                return responder.pack(code=131,description=str(error.output))
        else:
            return responder.pack(code=34,description="Nothing to commit")
    else:
        return responder.pack(code=34,description="Project not found")

# Edit responses to use responder