class Credencial:
    """
    Classe que armazena uma credencial
    """

    def __init__(self, usuario: str = "", senha: str = ""):
        """
        Método construtor.
        :param usuario: Usuário.
        :param senha: Senha.
        """
        self.usuario = usuario
        self.senha = senha
