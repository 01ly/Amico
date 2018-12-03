
import re

def camelcase(string):
    pattern = re.compile('[^a-zA-Z\d]')
    return pattern.sub('', string.title())


