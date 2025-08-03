from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label

import uuid
from smbprotocol.connection import Connection
from smbprotocol.session import Session
from smbprotocol.tree import TreeConnect
from smbprotocol.open import Open

USERNAME = "YourUsername"     # ← Укажи логин
PASSWORD = "YourPassword"     # ← Укажи пароль
ROBOT_IP = "192.168.130.39"   # ← Укажи IP робота

class SMBCheckApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical', padding=20, spacing=20)

        self.status_label = Label(text="Нажми кнопку для проверки RMC.exe", font_size=18)
        check_button = Button(text="Проверить файл", size_hint=(1, 0.3), font_size=20)
        check_button.bind(on_press=self.check_robot)

        layout.add_widget(self.status_label)
        layout.add_widget(check_button)

        return layout

    def check_robot(self, instance):
        self.status_label.text = "🔄 Проверка файла..."
        if self._check_robot_file():
            self.status_label.text = "✅ Файл RMC.exe найден!"
        else:
            self.status_label.text = "❌ Файл не найден или недоступен."

    def _check_robot_file(self):
        try:
            conn_id = uuid.uuid4()
            conn = Connection(conn_id, ROBOT_IP, 445)
            conn.connect()

            session = Session(conn, USERNAME, PASSWORD)
            session.connect()

            tree = TreeConnect(session, fr"\\{ROBOT_IP}\Afimilk")
            tree.connect()

            file = Open(tree, r"Robot\RMC.exe")
            file.open()
            file.close()

            conn.disconnect()
            return True
        except Exception as e:
            print("[Ошибка подключения SMB]:", e)
            return False

if __name__ == "__main__":
    SMBCheckApp().run()
