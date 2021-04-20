def had_cmd(message: str, cmd_list):
    # функция проверяет начинается ли команда со строки или с "алиса" + строка
    if isinstance(cmd_list, list):
        for cmd in cmd_list:
            if message.startswith(cmd) or message.startswith('алиса ' + cmd):
                return True
        return False
    else:
        return message.startswith(cmd_list)