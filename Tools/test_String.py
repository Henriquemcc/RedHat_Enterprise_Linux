from unittest import TestCase

import Tools.String


class TestMethodStringGetRealNumberAtTheEnd(TestCase):
    """
    Testa o método string_get_real_number_at_the_end do arquivo Tools/String.py.
    """

    def test_somente_numero_real(self):
        string = "176.079"
        numero_retornado = Tools.String.string_get_real_number_at_the_end(string)
        self.assertEqual(numero_retornado, 176.079)

        string = "18349.678"
        numero_retornado = Tools.String.string_get_real_number_at_the_end(string)
        self.assertEqual(numero_retornado, 18349.678)

    def test_somente_numero_inteiro(self):
        string = "17804"
        numero_retornado = Tools.String.string_get_real_number_at_the_end(string)
        self.assertEqual(numero_retornado, 17804)

    def test_numero_real_com_outro_caractere_no_comeco(self):
        string = " 176.079"
        numero_retornado = Tools.String.string_get_real_number_at_the_end(string)
        self.assertEqual(numero_retornado, 176.079)

        string = "z18349.678"
        numero_retornado = Tools.String.string_get_real_number_at_the_end(string)
        self.assertEqual(numero_retornado, 18349.678)

    def test_numero_real_com_outro_caractere_no_final(self):
        string = "176.079 "
        with self.assertRaises(Tools.String.StringDoesNotEndWithNumberException):
            Tools.String.string_get_real_number_at_the_end(string)

        string = "7543.6489 "
        with self.assertRaises(Tools.String.StringDoesNotEndWithNumberException):
            Tools.String.string_get_real_number_at_the_end(string)

    def test_numero_real_com_outro_caractere_no_comeco_e_no_final(self):
        string = " 176.079 "
        with self.assertRaises(Tools.String.StringDoesNotEndWithNumberException):
            Tools.String.string_get_real_number_at_the_end(string)

        string = "18349.678a"
        with self.assertRaises(Tools.String.StringDoesNotEndWithNumberException):
            Tools.String.string_get_real_number_at_the_end(string)

    def test_numero_real_com_mais_de_um_ponto(self):
        string = ".176.079"
        numero_retornado = Tools.String.string_get_real_number_at_the_end(string)
        self.assertEqual(numero_retornado, 176.079)

        string = "176.079."
        with self.assertRaises(Tools.String.StringDoesNotEndWithNumberException):
            Tools.String.string_get_real_number_at_the_end(string)

        string = "789.987.176.079"
        self.assertEqual(176.079, Tools.String.string_get_real_number_at_the_end(string))

    def test_numero_real_com_virgula(self):
        string = "100,176.079"
        numero_retornado = Tools.String.string_get_real_number_at_the_end(string)
        self.assertEqual(numero_retornado, 176.079)

        string = "100.176,079"
        numero_retornado = Tools.String.string_get_real_number_at_the_end(string)
        self.assertEqual(numero_retornado, 79)

    def test_qualquer_outro_caractere(self):
        string = "rthtrjuyiouyjthiopiuyjhgtfrhjklioolikujh"
        with self.assertRaises(Tools.String.StringDoesNotEndWithNumberException):
            Tools.String.string_get_real_number_at_the_end(string)

        string = "qscwdcrfbtgnyhmuj,ikiklo´ç-=\//"
        with self.assertRaises(Tools.String.StringDoesNotEndWithNumberException):
            Tools.String.string_get_real_number_at_the_end(string)


class TestStringEndsWithNumber(TestCase):
    """
    Testa o método character_is_number do arquivo Tools/String.py.
    """

    def test_somente_numero_real(self):
        string = "176.079"
        boolean_retornado = Tools.String.string_ends_with_number(string)
        self.assertEqual(boolean_retornado, True)

        string = "18349.678"
        boolean_retornado = Tools.String.string_ends_with_number(string)
        self.assertEqual(boolean_retornado, True)

    def test_somento_numero_inteiro(self):
        string = "98798"
        boolean_retornado = Tools.String.string_ends_with_number(string)
        self.assertEqual(boolean_retornado, True)

        string = "32678"
        boolean_retornado = Tools.String.string_ends_with_number(string)
        self.assertEqual(boolean_retornado, True)

    def test_numero_real_com_outro_caractere_no_comeco(self):
        string = " 176.079"
        boolean_retornado = Tools.String.string_ends_with_number(string)
        self.assertEqual(boolean_retornado, True)

        string = "z18349.678"
        boolean_retornado = Tools.String.string_ends_with_number(string)
        self.assertEqual(boolean_retornado, True)

    def test_numero_real_com_outro_caractere_no_final(self):
        string = "176.079 "
        boolean_retornado = Tools.String.string_ends_with_number(string)
        self.assertEqual(boolean_retornado, False)

        string = "7543.6489 "
        boolean_retornado = Tools.String.string_ends_with_number(string)
        self.assertEqual(boolean_retornado, False)

    def test_numero_real_com_outro_caractere_no_comeco_e_no_final(self):
        string = " 176.079 "
        boolean_retornado = Tools.String.string_ends_with_number(string)
        self.assertEqual(boolean_retornado, False)

        string = "18349.678a"
        boolean_retornado = Tools.String.string_ends_with_number(string)
        self.assertEqual(boolean_retornado, False)

    def test_numero_real_com_mais_de_um_ponto(self):
        string = ".176.079"
        boolean_retornado = Tools.String.string_ends_with_number(string)
        self.assertEqual(boolean_retornado, True)

        string = "176.079."
        boolean_retornado = Tools.String.string_ends_with_number(string)
        self.assertEqual(boolean_retornado, False)

        string = "789.987.176.079"
        boolean_retornado = Tools.String.string_ends_with_number(string)
        self.assertEqual(boolean_retornado, True)

    def test_numero_real_com_virgula(self):
        string = "100,176.079"
        boolean_retornado = Tools.String.string_ends_with_number(string)
        self.assertEqual(boolean_retornado, True)

        string = "100.176,079"
        boolean_retornado = Tools.String.string_ends_with_number(string)
        self.assertEqual(boolean_retornado, True)

    def test_qualquer_outro_caractere(self):
        string = "rthtrjuyiouyjthiopiuyjhgtfrhjklioolikujh"
        boolean_retornado = Tools.String.string_ends_with_number(string)
        self.assertEqual(boolean_retornado, False)

        string = "qscwdcrfbtgnyhmuj,ikiklo´ç-=\//"
        boolean_retornado = Tools.String.string_ends_with_number(string)
        self.assertEqual(boolean_retornado, False)


class TestMethodCharacterIsNumber(TestCase):
    """
    Testa o método character_is_number do arquivo Tools/String.py.
    """

    def testar_numeros(self):
        for i in range(0, 9):
            self.assertEqual(Tools.String.character_is_number("{}".format(i)), True)

    def testar_letras(self):
        self.assertEqual(Tools.String.character_is_number("a"), False)
        self.assertEqual(Tools.String.character_is_number("I"), False)
        self.assertEqual(Tools.String.character_is_number("G"), False)
        self.assertEqual(Tools.String.character_is_number("o"), False)
        self.assertEqual(Tools.String.character_is_number("W"), False)
        self.assertEqual(Tools.String.character_is_number("Z"), False)
        self.assertEqual(Tools.String.character_is_number("A"), False)
        self.assertEqual(Tools.String.character_is_number("z"), False)

    def testar_outros_caracteres(self):
        self.assertEqual(Tools.String.character_is_number("ç"), False)
        self.assertEqual(Tools.String.character_is_number("¹"), False)
        self.assertEqual(Tools.String.character_is_number("²"), False)
        self.assertEqual(Tools.String.character_is_number("³"), False)
        self.assertEqual(Tools.String.character_is_number("`"), False)
        self.assertEqual(Tools.String.character_is_number("^"), False)
        self.assertEqual(Tools.String.character_is_number("`"), False)
        self.assertEqual(Tools.String.character_is_number("?"), False)
        self.assertEqual(Tools.String.character_is_number("ª"), False)
        self.assertEqual(Tools.String.character_is_number("º"), False)


class TestMethodCharacterIsLetter(TestCase):
    """
    Testa o método character_is_letter do arquivo Tools/String.py.
    """

    def testar_numeros(self):
        for i in range(0, 9):
            self.assertEqual(Tools.String.character_is_letter("{}".format(i)), False)

    def testar_letras(self):
        self.assertEqual(Tools.String.character_is_letter("a"), True)
        self.assertEqual(Tools.String.character_is_letter("I"), True)
        self.assertEqual(Tools.String.character_is_letter("G"), True)
        self.assertEqual(Tools.String.character_is_letter("o"), True)
        self.assertEqual(Tools.String.character_is_letter("W"), True)
        self.assertEqual(Tools.String.character_is_letter("Z"), True)
        self.assertEqual(Tools.String.character_is_letter("A"), True)
        self.assertEqual(Tools.String.character_is_letter("z"), True)

    def testar_outros_caracteres(self):
        self.assertEqual(Tools.String.character_is_letter("¹"), False)
        self.assertEqual(Tools.String.character_is_letter("²"), False)
        self.assertEqual(Tools.String.character_is_letter("³"), False)
        self.assertEqual(Tools.String.character_is_letter("`"), False)
        self.assertEqual(Tools.String.character_is_letter("^"), False)
        self.assertEqual(Tools.String.character_is_letter("`"), False)
        self.assertEqual(Tools.String.character_is_letter("?"), False)
        self.assertEqual(Tools.String.character_is_letter("ª"), False)
        self.assertEqual(Tools.String.character_is_letter("º"), False)


class TestMethodStringIsSingleCharacter(TestCase):
    def testar_um_unico_caractere(self):
        self.assertEqual(Tools.String.string_is_single_character("a"), True)
        self.assertEqual(Tools.String.string_is_single_character("m"), True)
        self.assertEqual(Tools.String.string_is_single_character("z"), True)
        self.assertEqual(Tools.String.string_is_single_character("A"), True)
        self.assertEqual(Tools.String.string_is_single_character("Q"), True)
        self.assertEqual(Tools.String.string_is_single_character("Z"), True)
        self.assertEqual(Tools.String.string_is_single_character("\n"), True)
        self.assertEqual(Tools.String.string_is_single_character("\t"), True)
        self.assertEqual(Tools.String.string_is_single_character("\0"), True)
        self.assertEqual(Tools.String.string_is_single_character("\\"), True)
        self.assertEqual(Tools.String.string_is_single_character("0"), True)
        self.assertEqual(Tools.String.string_is_single_character("5"), True)
        self.assertEqual(Tools.String.string_is_single_character("9"), True)
        self.assertEqual(Tools.String.string_is_single_character("ç"), True)
        self.assertEqual(Tools.String.string_is_single_character("~"), True)
        self.assertEqual(Tools.String.string_is_single_character("\""), True)
        self.assertEqual(Tools.String.string_is_single_character("`"), True)
        self.assertEqual(Tools.String.string_is_single_character("ª"), True)
        self.assertEqual(Tools.String.string_is_single_character("º"), True)
        self.assertEqual(Tools.String.string_is_single_character("&"), True)
        self.assertEqual(Tools.String.string_is_single_character("$"), True)
        self.assertEqual(Tools.String.string_is_single_character("{"), True)
        self.assertEqual(Tools.String.string_is_single_character("}"), True)
        self.assertEqual(Tools.String.string_is_single_character("\r"), True)
        self.assertEqual(Tools.String.string_is_single_character("0"), True)

    def testar_mais_de_um_caractere(self):
        self.assertEqual(Tools.String.string_is_single_character("0a"), False)
        self.assertEqual(Tools.String.string_is_single_character("Zç"), False)
        self.assertEqual(Tools.String.string_is_single_character("q\0"), False)
        self.assertEqual(Tools.String.string_is_single_character("\\\\"), False)
        self.assertEqual(Tools.String.string_is_single_character("=="), False)
        self.assertEqual(Tools.String.string_is_single_character("\n\n"), False)
        self.assertEqual(Tools.String.string_is_single_character("\t\t"), False)
        self.assertEqual(Tools.String.string_is_single_character("\\#"), False)
        self.assertEqual(Tools.String.string_is_single_character("''"), False)
        self.assertEqual(Tools.String.string_is_single_character("\"\""), False)

    def testar_nenhum_caractere(self):
        self.assertEqual(Tools.String.string_is_single_character(""), False)
        self.assertEqual(Tools.String.string_is_single_character(''), False)


class TestMethodStringLastIndexesOfRealNumber(TestCase):
    def test_somente_numero_real(self):
        string = "176.079"
        a, b = Tools.String.string_last_indexes_of_real_number(string)
        string = string[a:(b + 1)]
        self.assertEqual(string, "176.079")

        string = "18349.678"
        a, b = Tools.String.string_last_indexes_of_real_number(string)
        string = string[a:(b + 1)]
        self.assertEqual(string, "18349.678")

    def test_somente_numero_inteiro(self):
        string = "17804"
        a, b = Tools.String.string_last_indexes_of_real_number(string)
        string = string[a:(b + 1)]
        self.assertEqual(string, "17804")

        string = "349834"
        a, b = Tools.String.string_last_indexes_of_real_number(string)
        string = string[a:(b + 1)]
        self.assertEqual(string, "349834")

    def test_numero_real_com_outro_caractere_no_comeco(self):
        string = " 176.079"
        a, b = Tools.String.string_last_indexes_of_real_number(string)
        string = string[a:(b + 1)]
        self.assertEqual(string, "176.079")

        string = "z18349.678"
        a, b = Tools.String.string_last_indexes_of_real_number(string)
        string = string[a:(b + 1)]
        self.assertEqual(string, "18349.678")

    def test_numero_real_com_outro_caractere_no_final(self):
        string = "176.079 "
        a, b = Tools.String.string_last_indexes_of_real_number(string)
        string = string[a:(b + 1)]
        self.assertEqual(string, "176.079")

        string = "7543.6489 "
        a, b = Tools.String.string_last_indexes_of_real_number(string)
        string = string[a:(b + 1)]
        self.assertEqual(string, "7543.6489")

    def test_numero_real_com_outro_caractere_no_comeco_e_no_final(self):
        string = " 176.079 "
        a, b = Tools.String.string_last_indexes_of_real_number(string)
        string = string[a:(b + 1)]
        self.assertEqual(string, "176.079")

        string = "18349.678a"
        a, b = Tools.String.string_last_indexes_of_real_number(string)
        string = string[a:(b + 1)]
        self.assertEqual(string, "18349.678")

    def test_numero_real_com_mais_de_um_ponto(self):
        string = ".176.079"
        a, b = Tools.String.string_last_indexes_of_real_number(string)
        string = string[a:(b + 1)]
        self.assertEqual(string, "176.079")

        string = "176.079."
        a, b = Tools.String.string_last_indexes_of_real_number(string)
        string = string[a:(b + 1)]
        self.assertEqual(string, "079.")

        string = "789.987.176.079"
        a, b = Tools.String.string_last_indexes_of_real_number(string)
        string = string[a:(b + 1)]
        self.assertEqual(string, "176.079")

    def test_numero_real_com_virgula(self):
        string = "100,176.079"
        a, b = Tools.String.string_last_indexes_of_real_number(string)
        string = string[a:(b + 1)]
        self.assertEqual(string, "176.079")

        string = "100.176,079"
        a, b = Tools.String.string_last_indexes_of_real_number(string)
        string = string[a:(b + 1)]
        self.assertEqual(string, "079")

    def test_qualquer_outro_caractere(self):
        string = "rthtrjuyiouyjthiopiuyjhgtfrhjklioolikujh"
        a, b = Tools.String.string_last_indexes_of_real_number(string)
        self.assertEqual(a, None)
        self.assertEqual(b, None)

        string = "qscwdcrfbtgnyhmuj,ikiklo´ç-=\//"
        a, b = Tools.String.string_last_indexes_of_real_number(string)
        self.assertEqual(a, None)
        self.assertEqual(b, None)
