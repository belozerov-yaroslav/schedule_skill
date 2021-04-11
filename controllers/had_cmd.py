def had_cmd(message: str, cmd_list):
    if isinstance(cmd_list, list):
        for cmd in cmd_list:
            if message.startswith(cmd) or message.startswith('алиса ' + cmd):
                return True
        return False
    else:
        return message.startswith(cmd_list)