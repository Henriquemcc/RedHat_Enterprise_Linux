from unittest import TestCase

import Tools.Backup


class TestMethodGetDotOldFileName(TestCase):
    """
    Testa o método __get_dot_old_file_name do arquivo Tools/Backup.py.
    """

    def test_one(self):
        nome_arquivo = "sshd_config"
        nome_arquivo_backup = Tools.Backup.get_dot_old_file_name(nome_arquivo)
        self.assertEqual(nome_arquivo_backup, "sshd_config.old")

        nome_arquivo = nome_arquivo_backup
        nome_arquivo_backup = Tools.Backup.get_dot_old_file_name(nome_arquivo)
        self.assertEqual(nome_arquivo_backup, "sshd_config.old1")

        nome_arquivo = nome_arquivo_backup
        nome_arquivo_backup = Tools.Backup.get_dot_old_file_name(nome_arquivo)
        self.assertEqual(nome_arquivo_backup, "sshd_config.old2")

        nome_arquivo = nome_arquivo_backup
        nome_arquivo_backup = Tools.Backup.get_dot_old_file_name(nome_arquivo)
        self.assertEqual(nome_arquivo_backup, "sshd_config.old3")

        nome_arquivo = nome_arquivo_backup
        nome_arquivo_backup = Tools.Backup.get_dot_old_file_name(nome_arquivo)
        self.assertEqual(nome_arquivo_backup, "sshd_config.old4")

        nome_arquivo = nome_arquivo_backup
        nome_arquivo_backup = Tools.Backup.get_dot_old_file_name(nome_arquivo)
        self.assertEqual(nome_arquivo_backup, "sshd_config.old5")
