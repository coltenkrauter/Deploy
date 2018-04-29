# Thanks tomdaley92 for the simple slack logging solution with traceback
# Credit: https://github.com/tomdaley92

from codepuller import config
import requests
import traceback

ENVIRONMENT = "COLTEN LAPTOP - DEV"
color = {
    "information": "",
    "warning": "",
    "error": ""
}

def log(text=None,name=None,link=None,alias=None,priority="information"):
    slack = {
        "attachments": [
            {   
                "pretext": ENVIRONMENT,
                "fallback": "Slack log",
                "color": color[priority],
                "fields": [],
                "thumb_url": "https://raw.githubusercontent.com/coltenkrauter/emojione/2.2.7/assets/png_512x512/1f98d.png",
                "ts": 
            }
        ]
    }

    # If there is text, add it to the slack message attachment
    if text is not None:
        slack["attachments"][0]["text"] = str(text)

    # If there is a traceback, add it to the slack message attachment
    if str(traceback.format_exc()) is not "NoneType: None":
        slack["attachments"][0]["fields"].append(
            {
                "title": "Traceback",
                "value": str(traceback.format_exc())
            }
        )

    # If there is a name, add it to the slack message attachment as the footer
    if name:
        slack["attachments"][0]["footer"] = name
        slack["attachments"][0]["footer_icon"] = "https://raw.githubusercontent.com/coltenkrauter/emojione/2.2.7/assets/png_128x128/1f464.png"

    # If there is a link, add it to the slack message attachment as the footer
    if alias and link:
        slack["attachments"][0]["title"] = alias
        slack["attachments"][0]["title_link"] = link

    # Post to Slack
    r = requests.post(config.SLACK_WEBHOOK_LOGGER,json=slack)
    
    # Print to standard out
    print(text)

if __name__ == '__main__':
    log("Testing functionality of Slack logger",False)