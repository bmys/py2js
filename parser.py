#! /usr/bin/python3

import sys, re

# Loading file
file_name = sys.argv[1]
file_content = None

try:
    with open(file_name, 'r') as file:
        file_content = file.readlines()

except FileNotFoundError:
    print(f'File "{file_name}" not found')
    sys.exit(1)


intent_val = [(value.count('  '), value.strip()) for value in file_content]
local_vars = dict()
in_loop = False

for cur, nx in zip(intent_val, intent_val[1:]):
    if in_loop:
        for key, value in local_vars.items():
            cur = (cur[0], cur[1].replace(key, value))

    loop = re.search('for\s(.+)\sin\s(.+):', cur[1])
    # assign = re.search('\s*(\w+)\s*=\s*(.+)', cur[1])

    assign = re.search('\s*(.+)\s*=\s*(.+)', cur[1])

    comment = re.search('\s*#(.*)\s*', cur[1])
    msg = re.search('\s*print\((.*)\)', cur[1])

    if loop is not None:
        loop = loop.groups()
        # print(a.groups())
        print(f'var {loop[0]} = 0;')
        print(f'for(;{loop[0]}<{loop[1]}.length; {loop[0]}++)', end='')
        local_vars[loop[0]] = f'{loop[1]}[{loop[0]}]'
        in_loop = True

    elif assign is not None:
        assign = assign.groups()
        print(f'var {assign[0]} = {assign[1]};')

    elif comment is not None:
        comment = comment.groups()
        print(f'// {comment[0]}')

    elif msg is not None:
        msg = msg.groups()
        print(f'console.log({msg[0]});')

    else:
        print(cur[0] * ' ' + cur[1])

    if cur[0] < nx[0]:
        print(cur[0] * ' ' + '{')

    if cur[0] > nx[0]:
        print(nx[0] * ' ' + '}')
        if in_loop:
            in_loop = False
            local_vars = dict()
