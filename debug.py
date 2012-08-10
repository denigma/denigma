#! /user/bin/env python
"""Toggles debug modus on server."""

local_settings = "/home/denigma/denigma/local_settings.py"

# Recieve settings and change debug values:
input = open(local_settings, 'r').read()
data = []

for line in input.split('\n'):

    if line.startswith("DEBUG"):
        value = not eval(line.split('DEBUG = ')[1])
        data.append('DEBUG = %s' % value)

    elif line.startswith("TEMPLATE_DEBUG"):
        value = not eval(line.split('TEMPLATE_DEBUG = ')[1])
        data.append('TEMPLATE_DEBUG = %s' % value) 
                    
    elif line.startswith("SERVE_MEDIA"):
        value = not eval(line.split('SERVE_MEDIA = ')[1])
        data.append("SERVE_MEDIA = %s" % value)

    else:
        data.append(line)

# Sets settings:
print '\n'.join(data)
output = open(local_settings, 'w').writelines('\n'.join(data))
#234567891123456789212345678931234567894123456789512345678961234567897123456789


