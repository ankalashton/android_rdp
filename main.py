import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QTextEdit
from smb.SMBConnection import SMBConnection
from smb.base import NotConnectedError

USER = 'afirnd'
PASSWORD = 'afifarm5!'
SERVER = 'R0000014'
IP = '192.168.130.39'


class FileChecker(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.conn = None

    def initUI(self):
        self.setWindowTitle('SMB File Checker')
        self.resize(400, 300)

        layout = QVBoxLayout()

        self.result = QTextEdit()
        self.result.setReadOnly(True)
        layout.addWidget(self.result)

        btn_connect = QPushButton('🔌 Подключиться и проверить файл')
        btn_connect.clicked.connect(self.check_file)
        layout.addWidget(btn_connect)

        self.setLayout(layout)

    def check_file(self):
        self.result.clear()

        try:
            self.conn = SMBConnection(USER, PASSWORD, 'android-client', SERVER, use_ntlm_v2=True)
            connected = self.conn.connect(IP, 445)
            if not connected:
                self.result.setText('❌ Не удалось подключиться к серверу.')
                return

            shares = self.conn.listShares()
            if not any(share.name == 'Afimilk' for share in shares):
                self.result.setText('❌ Шара Afimilk не найдена.')
                return

            files = self.conn.listPath('Afimilk', '/Robot/')
            filenames = [f.filename for f in files if not f.isDirectory]
            if 'RMC.exe' in filenames:
                self.result.setText('✅ Файл RMC.exe найден!\n\nСписок файлов:\n' + '\n'.join(filenames))
            else:
                self.result.setText('❌ Файл RMC.exe не найден.\n\nСписок файлов:\n' + '\n'.join(filenames))

        except NotConnectedError:
            self.result.setText('❌ Ошибка: нет подключения к SMB.')
        except Exception as e:
            self.result.setText(f'⚠️ Произошла ошибка:\n{str(e)}')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = FileChecker()
    window.show()
    sys.exit(app.exec_())
