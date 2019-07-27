import uuid


def generate_token():

    token = uuid.uuid4().hex

    return token


import random


def get_code():
    code = ''
    for i in range(6):
        code += str(random.randrange(10))
    return code
