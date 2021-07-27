class IsNotACharacterException(Exception):
    """
    Exceção que é lançada quando um objeto que não é um caractere é passado por parâmetro em uma função para caractere.
    """

    def __init__(self, msg="It is not a character", *args, **kwargs):
        if args:
            super().__init__(*args, **kwargs)
        else:
            super().__init__(msg, **kwargs)


class IsNotAStringException(Exception):
    """
    Exceção que é lançada quando um objeto que não é uma string é passado por parâmetro em uma função para string.
    """

    def __init__(self, msg="It is not a string", *args, **kwargs):
        if args:
            super().__init__(*args, **kwargs)
        else:
            super().__init__(msg, **kwargs)


class StringDoesNotEndWithNumberException(Exception):
    """
    Exceção que é lançada quando uma string não termina com um número.
    """

    def __init__(self, msg="String does not end with number", *args, **kwargs):
        if args:
            super().__init__(*args, **kwargs)
        else:
            super().__init__(msg, **kwargs)


def string_is_single_character(string: str) -> bool:
    """
    Verifica se uma string é um caractere: se ela não é nula e o tamanho é igual a um.
    :param string: String a ser verificada)
    :return: Valor booleano indicando se ela é um caractere.
    """
    if type(string) is not str:
        raise IsNotAStringException()

    if len(string) == 1:
        return True

    return False


def character_is_letter(character: str) -> bool:
    """
    Verifica se um caractere é uma letra.
    :param character: Caractere a ser verificado.
    :return: Valor booleano indicando se o caractere é uma letra.
    """

    if not string_is_single_character(character):
        raise IsNotACharacterException()

    if "a" <= character <= "z":
        return True
    if "A" <= character <= "Z":
        return True

    return False


def character_is_number(character: str) -> bool:
    """
    Verifica se um caractere é um número.
    :param character: Caractere a ser verificado.
    :return: Valor booleano indicando se o caractere é um número.
    """

    if not string_is_single_character(character):
        raise IsNotACharacterException()

    if "0" <= character <= "9":
        return True

    return False


def string_ends_with_number(string: str) -> bool:
    """
    Verifica se uma string termina com um número.
    :param string: String a ser verificada.
    :return: Valor booleano indicando se a string termina com um número
    """
    if type(string) is not str:
        raise IsNotAStringException()

    ultima_posicao = len(string) - 1

    if not character_is_number(string[ultima_posicao]):
        return False

    return True


def string_get_real_number_at_the_end(string: str) -> float:
    """
    Obtém o número no final da String.
    :param string: String onde o número será procurado.
    :return Número real no final da string.
    """
    if not string_ends_with_number(string):
        raise StringDoesNotEndWithNumberException()

    posicao_final = len(string) - 1
    posicao_inicial = posicao_final

    ponto_detectado = False

    while posicao_inicial > 0 and (character_is_number(string[posicao_inicial - 1]) or string[posicao_inicial - 1] == "."):
        if string[posicao_inicial - 1] == ".":
            if ponto_detectado:
                break
            else:
                ponto_detectado = True

        posicao_inicial -= 1

    return float(string[posicao_inicial:posicao_final + 1])


def string_last_indexes_of_real_number(string: str) -> [int, int]:
    """
    Obtém a posição do indice superior e inferior respectivamente da posição do último e do primeiro caractere numérico, do primeiro número real encontrado da direita para a esquerda da string.
    :param string: String onde será obtido os índices.
    :return: Indices inferior e superior respectivamente
    """
    index = len(string) - 1

    while index >= 0 and (not (character_is_number(string[index]) or string[index] == ".")):
        index -= 1

    if index < 0:
        return None, None

    indice_superior = index

    ponto_detectado = False
    while index >= 0 and (character_is_number(string[index]) or string[index] == "."):
        if string[index] == ".":
            if ponto_detectado:
                break
            else:
                ponto_detectado = True
        index -= 1

    indice_inferior = index + 1

    return indice_inferior, indice_superior
