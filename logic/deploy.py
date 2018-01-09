from Deploy.util import logger
import git 

def deploy(data, path):
    logger.deploy('Recieved payload')
    logger.deploy('Path: ' + path)
    
    g = git.cmd.Git("/home4/specica9/public_html/" + path)
    g.pull()

    message = "HTTP 200, OK: Success!"
    logger.deploy(message)

    return message, 200