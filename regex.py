"""
>>> check_email_edu()
True
>>> check_email_regular()
True
>>> check_email_negative()
False
"""

import re

pattern = r"(?<=student)[a-z]*\.[a-z]*@[a-z]*\.[a-z]*\.[a-z]*|[a-z]*[1-9]*@[a-z]*\.[a-z]*"

def check_email_edu():
    email = "student.muller@uni.edu.de"
    regexp = re.compile(pattern)
    return regexp.search(email) is not None

def check_email_regular():
    email = "student1234@gmail.com"
    regexp = re.compile(pattern)
    return regexp.search(email) is not None

def check_email_negative():
    email = "#-*&12@com"
    regexp = re.compile(pattern)
    return regexp.search(email) is not None

if __name__ == '__main__':
    import doctest
    doctest.testmod()