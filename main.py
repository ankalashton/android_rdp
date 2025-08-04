from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.core.window import Window

from smb.SMBConnection import SMBConnection
import socket

# Параметры подключения
USER = 'afirnd'
PASSWORD = 'afifarm5!'
SERVER = 'R0000014'
IP = '192.168.130.39'

class MainLayout(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', spacing=10, padding=20, **kwargs)

        self.check_btn = Button(text='Проверить SMB', size_hint_y=None, height=50)
        self.check_btn.bind(on_press=self.check_smb)
        self.add_widget(self.check_btn)

        self.output = Label(text='Нажмите кнопку для проверки', size_hint_y=1)
        self.add_widget(self.output)

    def check_smb(self, instance):
        try:
            conn = SMBConnection(USER, PASSWORD, "android_client", SERVER, use_ntlm_v2=True)
            connected = conn.connect(IP, 139)  # Порт может быть 445, если 139 не отвечает

            if connected:
                shares = conn.listShares()
                share_names = [share.name for share in shares if not share.isSpecial and share.name != '']
                self.output.text = f"Подключено. Доступные шары:\n" + "\n".join(share_names)
                conn.close()
            else:
                self.output.text = "Не удалось подключиться к SMB серверу."
        except Exception as e:
            self.output.text = f"Ошибка: {str(e)}"

class SMBApp(App):
    def build(self):
        Window.clearcolor = (1, 1, 1, 1)
        return MainLayout()

if __name__ == '__main__':
    SMBApp().run()
