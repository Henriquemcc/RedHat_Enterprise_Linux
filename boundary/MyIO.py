def read_string(msg):
    """
    Serve para ler da entrada padrão uma string.
    :param msg: Mensagem pedindo qual valor espera que o usuario digite.
    :return: String lida.
    """
    erro = True
    while erro:
        try:
            input_data = input(msg)
            erro = False
        except ValueError as e:
            print(e)

    return input_data


def read_integer(msg):
    """
    Serve para ler da entrada padrão um numero inteiro.
    :param msg: Mensagem pedindo qual valor espera que o usuario digite.
    :return: Numero inteiro lido.
    """
    erro = True
    while erro:
        try:
            input_data = read_string(msg).strip()
            integer = int(input_data)
            erro = False
        except ValueError as e:
            print(e)

    return integer


def read_float(msg):
    """
    Serve para ler da entrada padrão um numero real.
    :param msg: Mensagem pedindo qual valor espera que o usuario digite.
    :return: Numero real lido.
    """
    erro = True
    while erro:
        try:
            input_data = read_string(msg).strip()
            float_value = float(input_data)
            erro = False
        except ValueError as e:
            print(e)

    return float_value


def read_bool(msg):
    """
    Serve para ler da entrada padrao um valor booleano
    :param msg: Mensagem pedindo qual valor espera que o usuario digite.
    :return: Valor booleano lido.
    """
    erro = True
    while erro:
        try:
            input_data = read_string(msg).strip()
            if "false" in input_data.lower():
                boolean = False
            elif "true" in input_data.lower():
                boolean = True
            else:
                raise ValueError("invalid literal for boolean: " + input_data)
            erro = False
        except ValueError as e:
            print(e)

    return boolean
