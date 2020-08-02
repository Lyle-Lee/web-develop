#!/usr/bin/python3

import os
import cgi, cgitb
import re

def calculate(l):
    stack = []
    sign = '+' # Assume the first number is positive
    num = 0
    while len(l) > 0:
        c = l.pop(0)
        if c.isdigit():
            num = 10 * num + int(c)
        if c == '(':
            num = calculate(l)
        if (not c.isdigit() and c != ' ' or len(l) == 0):
            if sign == '+':
                stack.append(num)
            elif sign == '-':
                stack.append(-num)
            elif sign == '*':
                stack[-1] = stack[-1] * num
            elif sign == '/':
                stack[-1] = stack[-1] / num
            num = 0
            sign = c
        if c == ')': break
    return sum(stack)

cgitb.enable()

s = os.environ['QUERY_STRING']

print('Content-Type: text/html') # HTML is following
print('')                         # Leave a blank line

try:
    if re.match(r'[a-zA-Z]+', s):
        print('ERROR')
    else:
        l = list(s)
        result = calculate(l)
        print('%d' % result)
except:
    print('Undefined input.')
    raise SystemExit(1)
