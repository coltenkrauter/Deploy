# Credit for this function goes to dustyfresh https://gist.github.com/dustyfresh/10d4e260499612c055f91f824ebd8a64
def sanitize(inputstr):
    sanitized = inputstr
    badstrings = [
        ';',
        '$',
        '&&',
        '../',
        '<',
        '>',
        '%3C',
        '%3E',
        '\'',
        '--',
        '1,2',
        '\x00',
        '`',
        '(',
        ')',
        'file://',
        'input://'
    ]
    for badstr in badstrings:
        if badstr in sanitized:
            sanitized = sanitized.replace(badstr, '')
    return sanitized