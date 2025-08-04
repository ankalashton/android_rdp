from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
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

        self.log_output = TextInput(text='Нажмите кнопку для проверки SMB\n',
                                    readonly=True,
                                    size_hint_y=1,
                                    font_size=16,
                                    background_color=(0.95, 0.95, 0.95, 1),
                                    foreground_color=(0, 0, 0, 1),
                                    multiline=True)

        self.check_btn = Button(text='Проверить SMB', size_hint_y=None, height=50)
        self.check_btn.bind(on_press=self.check_smb)

        self.add_widget(self.check_btn)
        self.add_widget(self.log_output)

    def log(self, message):
        self.log_output.text += f"{message}\n"

    def check_smb(self, instance):
        self.log("▶ Начинаем проверку подключения к SMB...")
        try:
            conn = SMBConnection(USER, PASSWORD, "android_client", SERVER, use_ntlm_v2=True)
            self.log(f"⏳ Создаём соединение с {IP}...")
            connected = conn.connect(IP, 139)

            if connected:
                self.log("✅ Успешно подключено!")
                shares = conn.listShares()
                share_names = [share.name for share in shares if not share.isSpecial and share.name != '']
                if share_names:
                    self.log("📁 Доступные шары:")
                    for name in share_names:
                        self.log(f"   • {name}")
                else:
                    self.log("ℹ️ Нет доступных шар.")
                conn.close()
            else:
                self.log("❌ Не удалось подключиться к SMB серверу.")
        except Exception as e:
            self.log(f"⚠️ Ошибка: {str(e)}")

class SMBApp(App):
    def build(self):
        Window.clearcolor = (1, 1, 1, 1)
        return MainLayout()

if __name__ == '__main__':
    SMBApp().run()
