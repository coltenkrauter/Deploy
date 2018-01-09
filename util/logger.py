import requests
import traceback

def log(text=None):
    if text != None:
        data = { 'text' : '```'+str(text)+'```'}
    else:
        data = { 'text' : '```'+traceback.format_exc()+'```'}
    r = requests.post('https://hooks.slack.com/services/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', json=data)
    if r.status_code != 200:
        # Send error to mod_wsgi log, if THIS fails
        print('Error: failed to POST error to slack.')
