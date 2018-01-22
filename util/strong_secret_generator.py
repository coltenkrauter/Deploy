# 
# http://code.activestate.com/recipes/578169-extremely-strong-password-generator/
# Credit: Commentor Matt Hubbard 2012
# 
from random import choice

charsets = [
    'abcdefghijklmnopqrstuvwxyz',
    'ABCDEFGHIJKLMNOPQRSTUVWXYZ',
    '0123456789',
    '^!$&/()=?+#-_:<>',
    ]

def generatePassword(length=16):
    password = []
    charset = choice(charsets)
    while len(password) < length:
        password.append(choice(charset))
        charset = choice(list(set(charsets) - set([charset])))
    return "".join(password)

print(generatePassword(64))