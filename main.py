from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.clock import Clock, mainthread
from android.permissions import request_permissions, Permission
from jnius import autoclass
import socket, threading

# ⛔ Запрос разрешений
request_permissions([
    Permission.ACCESS_FINE_LOCATION,
    Permission.ACCESS_WIFI_STATE
])

# 📡 Получить SSID
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

        # 📡 Отображение SSID
        self.label = Label(text="📡 Сеть: —", font_size=24, size_hint_y=None, height=50)
        refresh_btn = Button(text="🔄 Обновить сеть", size_hint_y=None, height=50)
        refresh_btn.bind(on_press=self.update_ssid)

        # 🌐 Список устройств
        self.device_list = GridLayout(cols=1, size_hint_y=None)
        self.device_list.bind(minimum_height=self.device_list.setter('height'))
        scroll = ScrollView()
        scroll.add_widget(self.device_list)

        scan_btn = Button(text="📥 Сканировать сеть", size_hint_y=None, height=50)
        scan_btn.bind(on_press=self.start_scan)

        # 📋 Интерфейс
        self.add_widget(self.label)
        self.add_widget(refresh_btn)
        self.add_widget(scan_btn)
        self.add_widget(scroll)

        self.update_ssid()

    def update_ssid(self, *args):
        self.label.text = f"📡 Сеть: {get_current_wifi_ssid()}"

    @mainthread
    def add_device(self, name, ip):
        label = Label(text=f"🔌 {name} @ {ip}", size_hint_y=None, height=40)
        self.device_list.add_widget(label)

    def start_scan(self, *args):
        self.device_list.clear_widgets()
        threading.Thread(target=self.scan_network).start()

    def scan_network(self):
        prefix = "192.168.130."
        for i in range(6, 255):
            ip = f"{prefix}{i}"
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(0.5)
                if s.connect_ex((ip, 445)) == 0:
                    try:
                        name = socket.gethostbyaddr(ip)[0]
                    except:
                        name = "Unknown"
                    self.add_device(name, ip)
                s.close()
            except:
                pass

class WifiApp(App):
    def build(self):
        return WifiScanner()

if __name__ == "__main__":
    WifiApp().run()
