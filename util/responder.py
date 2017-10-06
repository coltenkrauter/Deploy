def responses(code = 200):
    codes = {
        200 : {'status' : 'OK', 'description' : 'Success!'},
        201 : {'status' : 'Created', 'description' : 'New resource created.'},
        202 : {'status' : 'Accepted', 'description' : 'Request accept, still processing.'},
        304 : {'status' : 'Not Modified', 'description' : 'Resource not modified.'},
        400 : {'status' : 'Bad Request', 'description' : 'Payload is invalid.'},
        401 : {'status' : 'Unauthorized', 'description' : 'Unauthorized for this request.'},
        404 : {'status' : 'Not Found', 'description' : 'Resource does not exist.'},
        410 : {'status' : 'Gone', 'description' : 'Resource has been permanently removed.'},
        420 : {'status' : 'Enhance Your Calm', 'description' : 'Request is being rate limited.'},
        429 : {'status' : 'Too Many Requests', 'description' : 'Request cannot be served as applications rate limit is exhausted.'},
        500 : {'status' : 'Internal Server Error', 'description' : 'An unexpected error has occured.'},
        502 : {'status' : 'Bad Gateway', 'description' : 'Invalid response from an upstream server.'},
        503 : {'status' : 'Service Unavailable', 'description' : 'Server is temporarily down due to maintenance or because it is overloaded.'},
        504 : {'status' : 'Gateway timeout', 'description' : 'Did not receive a timely response from an upstream server.'}
    }
    if code in codes:
        return codes[code]
    return { 'status' : 'Internal Error', 'description' : 'HTTP status code ' + code + ' is not defined.' }

def response(code = 200, message=None, identifier=None):
    response = responses(code)
    media = {
        'httpCode' : code,
        'httpStatus' : response['status'],
        'description' : response['description'],
        'message' : None
    }

    if message is not None:
        media['message'] = str(message)
    
    if identifier is not None:
        key, value = list(identifier.items())[0]
        media[key] = value

    return media, code