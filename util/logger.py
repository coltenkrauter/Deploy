import gzip
import json
import os
import shutil
from datetime import datetime
import requests
import inspect

def zip(filePath, today):
    # Gzip a text file
    with open(filePath, 'rb') as f_in, gzip.open(filePath + '.' + today + '.gz', 'wb') as f_out:
        shutil.copyfileobj(f_in, f_out)

def slack(message, webhookUrl):
    slack_data = {'text': message}
    response = requests.post(webhookUrl, data=json.dumps(slack_data),
        headers={'Content-Type': 'application/json'})

def rotateAndZip(filePath, today):
    # Check if the log file already exists
    if os.path.isfile(filePath):
        createdDate = os.path.getctime(filePath)

        # If the log file exists and the creation date was not today then zip it
        if datetime.fromtimestamp(createdDate).strftime('%Y%m%d') != today:
            zip(filePath, today)
            
            # If the zipped file exists then remove the original
            if os.path.isfile(filePath + '.' + today + '.gz'):
                os.remove(filePath)
def log(message, logType = None, traceback = None):
    # Force message to string
    message = str(message)

    # If no logType was passed then the log file will be named Application.log
    # If 'error' was passed as the logType then the log file will be named Application.error_log
    if logType is None: 
        logType = 'log'
    else: 
        logType = logType + '_log'
    
    # Initialize the path and application variables
    path = './logs/'
    application = 'Budgetface'

    # Initialize variables
    filePath = path + application + '.' + logType
    now = datetime.now()
    today = now.strftime('%Y%m%d')
    timestamp = today + ' ' + now.strftime('%H:%M:%S.%f')
    
    # Validate path: if the directory does not exist then create it
    if not os.path.exists(path):
        os.makedirs(path)

    # Rotate and zip files that were not created today
    rotateAndZip(filePath, today)
    
    # Write to todays log file
    with open(filePath, 'a') as file:
        file.write(timestamp + ' ' + message)
        if not traceback is None:
            file.write('\n')
            file.write(traceback)    
        file.write('\n')
        file.close()

    # Post error logs slack
    if logType == 'error_log':
        slack(message + '\n' + traceback, 'https://hooks.slack.com/services/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')
    elif logType == 'deploy_log':
        slack(message, 'https://hooks.slack.com/services/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')

def error(message): 
    tracebacks = inspect.getouterframes(inspect.currentframe())
    traceback = ""
    for lines in tracebacks:
        (frame, filename, line_number, function_name, line, index) = lines
        if not str(function_name) == 'error' and not str(function_name) == 'log':
            traceback = 'Traceback, filename: ' + str(filename) + ', function: ' + str(function_name) + '()'
            break
    log(message, logType='error', traceback=traceback)

def warning(message): 
    log(message, 'warning')

def information(message): 
    log(message, 'information')

def deploy(message): 
    log(message, 'deploy')