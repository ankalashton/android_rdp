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
from ftplib import FTP
import time

# 📲 Разрешения
request_permissions([
    Permission.ACCESS_FINE_LOCATION,
    Permission.ACCESS_WIFI_STATE
])

# 📡 SSID Wi-Fi
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
        self.subnet = "192.168.130."
        self.login = "anonymous"
        self.password = ""
        self.timeout = 4
        self.devices = []

        self.label = Label(text="📡 Сеть: —", font_size=24, size_hint_y=None, height=50)
        self.status_label = Label(text="🕒 Готов к сканированию FTP", font_size=20, size_hint_y=None, height=40)

        refresh_btn = Button(text="🔄 Обновить сеть", size_hint_y=None, height=50)
        refresh_btn.bind(on_press=self.update_ssid)

        scan_ftp_btn = Button(text="📁 Сканировать FTP", size_hint_y=None, height=50)
        scan_ftp_btn.bind(on_press=self.start_ftp_scan)

        self.device_list = GridLayout(cols=1, size_hint_y=None)
        self.device_list.bind(minimum_height=self.device_list.setter('height'))
        scroll = ScrollView()
        scroll.add_widget(self.device_list)

        self.add_widget(self.label)
        self.add_widget(refresh_btn)
        self.add_widget(scan_ftp_btn)
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

    def start_ftp_scan(self, *args):
        self.device_list.clear_widgets()
        self.devices = []
        self.update_status("📁 Сканирование FTP...")
        threading.Thread(target=self.scan_ftp).start()

    def scan_ftp(self):
        found = 0
        for i in range(1, 255):
            ip = f"{self.subnet}{i}"
            try:
                ftp = FTP()
                ftp.connect(ip, 21, timeout=self.timeout)
                ftp.login(self.login, self.password)
                ftp.quit()
                self.add_device("✅ FTP-сервер", ip)
                found += 1
            except Exception as e:
                self.add_device(f"❌ {e.__class__.__name__}", ip)
            time.sleep(0.05)

            if i % 20 == 0:
                self.update_status(f"🔎 FTP: {ip} | Найдено: {found}")
        self.update_status(f"✅ Сканирование завершено: {found} сервер(ов)")

class WifiApp(App):
    def build(self):
        return WifiScanner()

if __name__ == "__main__":
    WifiApp().run()
