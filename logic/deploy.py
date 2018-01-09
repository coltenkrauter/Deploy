from Deploy.util import logger
import git 

def deploy(data, path):
    logger.log('Recieved payload')
    logger.log('Path: ' + path)
    
    g = git.cmd.Git("/home4/specica9/public_html/" + path)
    g.pull()

    message = "HTTP 200, OK: Success!"
    logger.log(message)

    return message, 200