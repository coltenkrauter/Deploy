# Thanks tomdaley92 for the simple slack logging solution with traceback
# Credit: https://github.com/tomdaley92

from codepuller import config
import requests
import traceback
import time
import pendulum

ENVIRONMENT = "COLTEN LAPTOP - DEV"

color = {
    "success": "#689F38",
    "information": "#1565C0",
    "warning": "#FFCE31",
    "error": "#cd201f"
}

def log(text=None,name=None,avatar=None,timestamp=None,repo=None,repoUrl=None,commit=None,commitUrl=None,priority="information"):
    slack = {
        "attachments": [
            {   
                "pretext": ENVIRONMENT,
                "fallback": "Slack log",
                "color": color[priority],
                "fields": [],
                "thumb_url": "https://raw.githubusercontent.com/coltenkrauter/emojione/2.2.7/assets/png_512x512/1f98d.png",
                "ts": time.time()
            }
        ]
    }

    # If there is text, add it to the slack message attachment
    if text is not None:
        slack["attachments"][0]["text"] = str(text)

    # If there is a traceback, add it to the slack message attachment
    tb = str(traceback.format_exc())
    if not ("NoneType:" in tb and len(tb) < 50):
        slack["attachments"][0]["fields"].append(
            {
                "title": "Traceback",
                "value": tb
            }
        )

    # If there is a name, add it to the slack message attachment as the footer
    if name:
        slack["attachments"][0]["footer"] = name

        # Add avatar 
        if avatar:
            slack["attachments"][0]["footer_icon"] = avatar
        else:
            slack["attachments"][0]["footer_icon"] = "https://raw.githubusercontent.com/coltenkrauter/emojione/2.2.7/assets/png_128x128/1f464.png"

    # If there is a timestamp, add timestamp
    if timestamp:
        slack["attachments"][0]["ts"] = pendulum.parse(timestamp).timestamp()

    # If there is a repoUrl, add it to the slack message attachment as the footer
    if repo and repoUrl:
        slack["attachments"][0]["title"] = repo
        slack["attachments"][0]["title_link"] = repoUrl

    # If there is a commit link, add it to the slack message attachment
    if commit and commitUrl:
        slack["attachments"][0]["author_name"] = commit
        slack["attachments"][0]["author_link"] = commitUrl
        slack["attachments"][0]["author_icon"] = "https://assets-cdn.github.com/images/modules/logos_page/GitHub-Mark.png"
    
    # Post to Slack
    r = requests.post(config.SLACK_WEBHOOK_LOGGER,json=slack)
    
    # Print to standard out
    print(str(slack))