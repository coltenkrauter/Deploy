# Thanks tomdaley92 for the simple slack logging solution with traceback
# Credit: https://github.com/tomdaley92

from codepuller import config
import requests
import traceback as error

ENVIRONMENT = "`Colten PC - DEV`\n\n\n\n"
config.SLACK_WEBHOOK_LOGGER = "https://hooks.slack.com/services/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"

def log(text=None, traceback=True):
    data = {
        "text":"",
        "traceback":"",
        "newlines":""
    }

    if text is not None:
        data["text"] = "*Message:* "+str(text)

    if traceback:
        data["traceback"] = " ```"+str(error.format_exc())+"``` "
    
    if data["text"] and data["traceback"]:
        data["newlines"] = "\n\n"

    slack = {
        "text":ENVIRONMENT+" "+data["text"]+data["newlines"]+data["traceback"]
    }
    # Post to Slack
    r = requests.post(config.SLACK_WEBHOOK_LOGGER, json=slack)
    
    # Print to standard out
    print(text)

if __name__ == '__main__':
    log("Testing functionality of Slack logger.", False)