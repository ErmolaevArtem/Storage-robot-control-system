def convert(words_list):
    # Список команд содержит первым элементом число команд, далее сами команды
    command_list = [0]
    # Набор списков возможных интерпретаций команд
    forward_list = ["вперёд", "перед"]
    backward_list = ["назад"]
    right_list = ["направо", "вправо", "право", "права", "справа"]
    left_list = ["налево", "влево", "лево", "слева"]
    stop_list = ["стоп"]

    # Определение команд по словам
    for word in words_list:
        for command in forward_list:
            if word == command:
                command_list.append('forward')
                command_list[0] += 1
        for command in backward_list:
            if word == command:
                command_list.append('backward')
                command_list[0] += 1
        for command in right_list:
            if word == command:
                command_list.append('right')
                command_list[0] += 1
        for command in left_list:
            if word == command:
                command_list.append('left')
                command_list[0] += 1
        for command in stop_list:
            if word == command:
                command_list.append('stop')
                command_list[0] += 1

    return command_list
