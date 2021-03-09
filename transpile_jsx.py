 #!/usr/bin/env python3
import os

source = './frontend_forms/static/frontend_forms/js/frontend_forms.jsx'
target = './frontend_forms/static/frontend_forms/js/frontend_forms.js'

if os.path.exists(target):
    print('Removing target "%s" ...' % target)
    os.remove(target)

command = "node ./example/node_modules/babel-cli/bin/babel.js --presets {presets} {source} > {target}".format(
    presets=os.path.abspath('./example/node_modules/babel-preset-es2015'),
    source=source,
    target=target,
)

print("\n" + command + "\n")
os.system(command)

print('New target "%s" created' % target)
