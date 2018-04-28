# Error code objects
error = {
    0: {
        "HTTPStatusCode": 200,
        "message": "Success"
    },
    1: {
        "HTTPStatusCode": 201,
        "message": "Resource created"
    },
    32: {
        "HTTPStatusCode": 401,
        "message": "Unable to authenticate"
    },
    34: {
        "HTTPStatusCode": 404,
        "message": "Resource does not exist"
    },
    35: {
        "HTTPStatusCode": 400,
        "message": "Invalid payload"
    },
    36: {
        "HTTPStatusCode": 400,
        "message": "Resource already exists"
    },
    37: {
        "HTTPStatusCode": 400,
        "message": "Invalid query parameters"
    },
    130: {
        "HTTPStatusCode": 500,
        "message": "Internal database error"
    },
    131: {
        "HTTPStatusCode": 500,
        "message": "Internal error"
    },
    132: {
        "HTTPStatusCode": 500,
        "message": "External error"
    }
}

# Pack response objects based on code
def pack(code, description=None, response=None):
    payload = {
        "code": code
    }

    if code in error:
        payload["message"] = error[code]["message"]

        if description:
            payload["description"] = str(description)
        
        if response:
            payload["data"] = response
        
        return payload, error[code]["HTTPStatusCode"]
    
    payload["message"] = "Undefined error code!"

    # return 500 (Internal server error) for undefined error codes
    return payload, 500
