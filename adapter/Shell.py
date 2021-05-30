import enum
import subprocess


class AcaoQuandoOcorrerErro(enum.Enum):
    """
    Enum das ações a serem executadas caso ocorra algum erro
    """

    # Aborta quando ocorrer erro
    ABORTAR = 0

    # Repete o comando quando ocorrer erro até o numero máximo de repetições. Quando o número máximo de repetições é
    # atingido o programa aborta
    REPETIR_E_ABORTAR = 1

    # Repete o comando quando ocorrer erro até o numero máximo de repetições. Quando o número máximo de repetições é
    # atingido o programa ignora o erro executando o próximo comando.
    REPETIR_E_IGNORAR = 2

    # Ignora o erro, seguindo para o próximo comando.
    IGNORAR = 3


class Shell:
    """
    Classe que realiza a comunicação do código Python com o shell do Linux.
    """

    def __init__(self, acao_quando_ocorrer_erro: AcaoQuandoOcorrerErro = AcaoQuandoOcorrerErro.REPETIR_E_ABORTAR,
                 quantidade_maxima_de_repeticoes_em_caso_de_erro: int = 5):
        """
        Método construtor.
        :param acao_quando_ocorrer_erro: O que deve ser feito caso o comando Shell resulte em erro.
        :param quantidade_maxima_de_repeticoes_em_caso_de_erro: Caso seja para repetir, o número máximo de repetições.
        """
        self.acao_quando_ocorrer_erro = acao_quando_ocorrer_erro
        self.quantidade_maxima_de_repeticoes_em_caso_de_erro = quantidade_maxima_de_repeticoes_em_caso_de_erro

    def executar(self, comando):
        """
        Executa comando(s) shell.
        :param comando: Comando a ser executado.
        """
        if type(comando) is str:
            if self.acao_quando_ocorrer_erro == AcaoQuandoOcorrerErro.ABORTAR:
                subprocess.run(comando, shell=True, check=True)
            elif self.acao_quando_ocorrer_erro == AcaoQuandoOcorrerErro.IGNORAR:
                try:
                    subprocess.run(comando, shell=True, check=True)
                except subprocess.CalledProcessError as erro:
                    print(erro)
            elif self.acao_quando_ocorrer_erro == AcaoQuandoOcorrerErro.REPETIR_E_ABORTAR \
                    or self.acao_quando_ocorrer_erro == AcaoQuandoOcorrerErro.REPETIR_E_IGNORAR:
                for c in range(0, self.quantidade_maxima_de_repeticoes_em_caso_de_erro):
                    try:
                        subprocess.run(comando, shell=True, check=True)
                        break
                    except subprocess.CalledProcessError as erro:
                        print(erro)
                        if self.acao_quando_ocorrer_erro == AcaoQuandoOcorrerErro.REPETIR_E_ABORTAR and c == self.quantidade_maxima_de_repeticoes_em_caso_de_erro - 1:
                            raise erro

        elif type(comando) is list:
            for c in comando:
                self.executar(c)

    def executar_e_obter_saida(self, comando):
        """
        Executa comando(s) shell e obtém a saida.
        :param comando: Comando(s) shell a ser(em) executado(s).
        :return: Saida(s) do(s) comando(s).
        """
        if type(comando) is str:

            if self.acao_quando_ocorrer_erro == AcaoQuandoOcorrerErro.ABORTAR:
                return subprocess.check_output(comando, shell=True)

            elif self.acao_quando_ocorrer_erro == AcaoQuandoOcorrerErro.IGNORAR:
                try:
                    return subprocess.check_output(comando, shell=True)
                except subprocess.CalledProcessError as erro:
                    print(erro)

            elif self.acao_quando_ocorrer_erro == AcaoQuandoOcorrerErro.REPETIR_E_ABORTAR or self.acao_quando_ocorrer_erro == AcaoQuandoOcorrerErro.REPETIR_E_IGNORAR:
                for c in range(0, self.quantidade_maxima_de_repeticoes_em_caso_de_erro):
                    try:
                        return subprocess.check_output(comando, shell=True)
                    except subprocess.CalledProcessError as erro:
                        print(erro)
                        if self.acao_quando_ocorrer_erro == AcaoQuandoOcorrerErro.REPETIR_E_ABORTAR and c == self.quantidade_maxima_de_repeticoes_em_caso_de_erro - 1:
                            raise erro

        elif type(comando) is list:
            string_saida = []
            for c in comando:
                string_saida.append(self.executar_e_obter_saida(c))
            return string_saida
