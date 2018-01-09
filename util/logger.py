import requests
import traceback

def log(text=None):
    if text != None:
        data = { 'text' : '```'+str(text)+'```'}
    else:
        data = { 'text' : '```'+traceback.format_exc()+'```'}
    r = requests.post(config.LOG_HOOK, json=data)
    if r.status_code != 200:
        # Send error to mod_wsgi log, if THIS fails
        print('Error: failed to POST error to slack.')
