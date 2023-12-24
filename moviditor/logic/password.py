'''module containing a password generator'''

import secrets, string

def generator(pw_length=30):
    '''generates a random password, of given length, each time the code is run'''
    password = ''
    alpha_num = string.digits + string.ascii_letters
    for i in range(pw_length):
        password += ''.join(secrets.choice(alpha_num))
    return password
