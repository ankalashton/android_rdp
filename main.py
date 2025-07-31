from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.clock import mainthread
from android.permissions import request_permissions, Permission
from jnius import autoclass
import socket
import threading
from ftplib import FTP, error_perm
import time

# 📲 Разрешения Android
request_permissions([
    Permission.ACCESS_FINE_LOCATION,
    Permission.ACCESS_WIFI_STATE,
    Permission.READ_EXTERNAL_STORAGE,
    Permission.WRITE_EXTERNAL_STORAGE
])

# 📡 Получение SSID сети
def get_current_wifi_ssid():
    Context = autoclass('android.content.Context')
    PythonActivity = autoclass('org.kivy.android.PythonActivity')
    activity = PythonActivity.mActivity
    wifi_service = activity.getSystemService(Context.WIFI_SERVICE)
    info = wifi_service.getConnectionInfo()
    ssid = info.getSSID()
    return ssid[1:-1] if ssid.startswith('"') and ssid.endswith('"') else ssid

class WifiScanner(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', **kwargs)
        self.ip_target = "192.168.130.39"
        self.login = "afirnd"
        self.password = "afifarm5!"
        self.timeout = 5

        self.label = Label(text="📡 Сеть: —", font_size=24, size_hint_y=None, height=50)
        self.status_label = Label(text="🕒 Готов к проверке FTP", font_size=20, size_hint_y=None, height=40)

        refresh_btn = Button(text="🔄 Обновить сеть", size_hint_y=None, height=50)
        refresh_btn.bind(on_press=self.update_ssid)

        check_rmc_btn = Button(text="🔍 Проверить RMC.exe @ .39", size_hint_y=None, height=50)
        check_rmc_btn.bind(on_press=self.find_rmc_prompt)

        self.device_list = GridLayout(cols=1, size_hint_y=None)
        self.device_list.bind(minimum_height=self.device_list.setter('height'))
        scroll = ScrollView()
        scroll.add_widget(self.device_list)

        self.add_widget(self.label)
        self.add_widget(refresh_btn)
        self.add_widget(check_rmc_btn)
        self.add_widget(self.status_label)
        self.add_widget(scroll)

        self.update_ssid()

    def update_ssid(self, *args):
        self.label.text = f"📡 Сеть: {get_current_wifi_ssid()}"

    @mainthread
    def add_device(self, name, ip):
        item = Label(text=f"{name} @ {ip}", size_hint_y=None, height=40)
        self.device_list.add_widget(item)

    @mainthread
    def update_status(self, text):
        self.status_label.text = text

    def find_rmc_prompt(self, *args):
        self.device_list.clear_widgets()
        threading.Thread(target=self.find_rmc_thread).start()

    def find_rmc_thread(self):
        self.update_status("🔍 Проверка 192.168.130.39...")
        ip = self.ip_target
        path_segments = ["Afimilk", "Robot"]
        filename = "RMC.exe"

        try:
            ftp = FTP()
            ftp.connect(ip, 21, timeout=self.timeout)
            ftp.login(self.login, self.password)
            ftp.set_pasv(True)

            for folder in path_segments:
                try:
                    self.add_device(f"📍 Перед cwd('{folder}') → pwd: {ftp.pwd()}", ip)
                    contents = ftp.nlst()
                    self.add_device(f"📄 Содержимое: {contents}", ip)
                    ftp.cwd(folder)
                    self.add_device(f"✅ Перешёл в: {folder}", ip)
                except error_perm as e:
                    self.add_device(f"🚫 error_perm в '{folder}': {e}", ip)
                    ftp.quit()
                    return
                except Exception as e:
                    self.add_device(f"❌ Ошибка перехода: {e}", ip)
                    ftp.quit()
                    return

            try:
                final_pwd = ftp.pwd()
                files = ftp.nlst()
                self.add_device(f"📍 Итоговая папка: {final_pwd}", ip)
                self.add_device(f"📄 Файлы: {files}", ip)
                if filename in files:
                    self.add_device(f"✅ Найден RMC.exe!", ip)
                else:
                    self.add_device(f"❌ RMC.exe не найден", ip)
            except Exception as e:
                self.add_device(f"⚠️ Ошибка чтения: {e}", ip)

            ftp.quit()

        except Exception as e:
            self.add_device(f"💥 FTP ошибка: {e}", ip)

        self.update_status("✅ Проверка завершена")

class WifiApp(App):
    def build(self):
        return WifiScanner()

if __name__ == "__main__":
    WifiApp().run()
