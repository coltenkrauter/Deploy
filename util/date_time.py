from datetime import datetime, timedelta

# Convert milliseconds since the epoch to an ISO8601 formatted timestamp
def to_iso8601(dateInMilliseconds):
    
    # Convert to seconds since the epoch
    dateInSeconds = dateInMilliseconds/1000

    # Convert seconds since the epoch to a Python datetime object
    dateInSeconds = datetime(1970, 1, 1) + timedelta(seconds=dateInSeconds)
    
    # Convert Python datetime object to iso8601 format
    dateString = dateInSeconds.strftime('%Y-%m-%dT%H:%M:%S.%fZ').replace("Z", "")[:-3] + "Z"

    return dateString

# Convert an ISO8601 formatted timestamp to milliseconds since the epoch
def to_milliseconds(dateString):
    dateString = dateString.upper()

    # deals with base case 2017:10:31T05:10:05
    dateFormat = '%Y-%m-%dT%H:%M:%S'

    # deals with the case 2017:10:31T05:10:05.098Z
    if 'Z' in dateString and '.' in dateString:
        dateFormat = '%Y-%m-%dT%H:%M:%S.%fZ'

    # deals with the case 2017:10:31T05:10:05Z
    elif 'Z' in dateString:
        dateFormat = '%Y-%m-%dT%H:%M:%SZ'

    # deals with the case 2017:10:31T05:10:05.098
    elif '.' in dateString:
        dateFormat = '%Y-%m-%dT%H:%M:%S.%f'
    
    # Convert ISO8601 to Python datetime object
    dateObject = datetime.strptime(dateString, dateFormat)
    
    # Convert Python datetime object to seconds since the epoch
    dateInSeconds = (dateObject - datetime(1970, 1, 1)).total_seconds()
    
    # Convert to millisseconds since the epoch
    dateInMilliseconds = dateInSeconds * 1000

    # Cast as int to remove trailing zeros
    return int(dateInMilliseconds)

# Convert milliseconds since the epoch to an ISO8601 formatted timestamp
def format_date(dateInMilliseconds, format):
    
    # Convert to seconds since the epoch
    dateInSeconds = dateInMilliseconds/1000

    # Convert seconds since the epoch to a Python datetime object
    dateInSeconds = datetime(1970, 1, 1) + timedelta(seconds=dateInSeconds)
    
    # Convert Python datetime object to given format
    dateString = dateInSeconds.strftime(format)

    return dateString

# Get the current time in milliseconds
def current_time():
    return to_milliseconds(datetime.now().isoformat())
