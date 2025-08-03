import uuid
import os
from smbprotocol.connection import Connection
from smbprotocol.session import Session
from smbprotocol.tree import TreeConnect
from smbprotocol.open import Open
from smbprotocol.list import List

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button
from kivy.uix.popup import Popup

# Настройки SMB подключения
SERVER_IP = "192.168.130.39"
USERNAME = "afirnd"
PASSWORD = "afifarm5!"
SHARE_NAME = "Afimilk"

class FileList(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', spacing=10, padding=10, **kwargs)
        self.load_files()

    def show_error(self, msg):
        popup = Popup(title='Ошибка', content=Label(text=msg),
                      size_hint=(None, None), size=(400, 200))
        popup.open()

    def load_files(self):
        try:
            # SMB-подключение
            conn = Connection(uuid.uuid4(), SERVER_IP, 445)
            conn.connect()
            session = Session(conn, USERNAME, PASSWORD)
            session.connect()
            tree = TreeConnect(session, f"\\\\{SERVER_IP}\\{SHARE_NAME}")
            tree.connect()

            listing = List(tree, "")
            listing_result = listing.list()

            scroll = ScrollView()
            files_container = BoxLayout(orientation='vertical', size_hint_y=None)
            files_container.bind(minimum_height=files_container.setter('height'))

            for item in listing_result:
                name = item.file_name
                if not name.startswith("."):  # Пропустить скрытые файлы
                    btn = Button(text=name, size_hint_y=None, height=40)
                    btn.bind(on_release=lambda btn: self.show_error(f"Вы выбрали файл: {btn.text}"))
                    files_container.add_widget(btn)

            scroll.add_widget(files_container)
            self.add_widget(scroll)

        except Exception as e:
            self.show_error(str(e))

class SMBApp(App):
    def build(self):
        return FileList()

if __name__ == "__main__":
    SMBApp().run()
