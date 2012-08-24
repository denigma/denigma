#! /user/bin/env python
"""Toggles the admin interface on server."""

local_settings = "/home/denigma/denigma/local_settings.py"

# Recieve settings and change debug values:
input = open(local_settings, 'r').read()
data = []

for line in input.split('\n'):

    if line.startswith("GRAPPELLI"):
        value = not eval(line.split('GRAPPELLI = ')[1])
        data.append('GRAPPELLI = %s' % value)
    else:
        data.append(line)

# Sets settings:
print '\n'.join(data)
output = open(local_settings, 'w').writelines('\n'.join(data))
#234567891123456789212345678931234567894123456789512345678961234567897123456789

