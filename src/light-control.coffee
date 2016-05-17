# Description:
#   Run light commands.
#
# Commands:
#   hubot light <subcommand>

{spawn, exec}  = require 'child_process'
path = require 'path'

module.exports = (robot) ->
 scriptsPath = path.resolve(__dirname, '../')

 # Deploy to staging
 robot.respond /light (.*)/i, (msg) ->
    send = (text, prefix='') ->
        msg.send prefix+text

    # Get subcommand
    subcommand = msg.match[1]
    # Tell the user hubot is working on the request
    msg.send "Turning light #{subcommand}..."
    # Execute a pyinvoke command
    command = "invoke #{subcommand}"
    if subcommand == 'on'
        invoke = exec scriptsPath + '/io/pt2262.py -c 123'
    else if subcommand == 'off'
        invoke = exec scriptsPath + '/io/pt2262.py -c 132'
    else
        invoke = exec scriptsPath + '/io/pt2262.py'

    invoke.stderr.on 'data', (data) ->
        for line in data.toString().split('\n')
            send line, 'Error: '

    invoke.stdout.on 'data', (data) ->
        for line in data.toString().split('\n')
            send '`' + line + '`' if !!line

    invoke.on 'exit', (code) ->
        if code == 0
            send "Done!"
        else
            send "FAILED #{command}. Returned #{code}"
