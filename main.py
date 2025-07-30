from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from android.permissions import request_permissions, Permission
from jnius import autoclass

# Запрос необходимых разрешений при старте
request_permissions([
    Permission.ACCESS_FINE_LOCATION,
    Permission.ACCESS_WIFI_STATE
])

def get_current_wifi_ssid():
    Context = autoclass('android.content.Context')
    PythonActivity = autoclass('org.kivy.android.PythonActivity')
    activity = PythonActivity.mActivity
    wifi_service = activity.getSystemService(Context.WIFI_SERVICE)
    info = wifi_service.getConnectionInfo()
    ssid = info.getSSID()

    # Убираем лишние кавычки вокруг SSID
    if ssid.startswith('"') and ssid.endswith('"'):
        ssid = ssid[1:-1]
    return ssid

class WifiDisplay(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', **kwargs)
        self.label = Label(text="📡 Сеть: —", font_size=24)
        refresh_btn = Button(text="🔄 Обновить сеть", size_hint_y=None, height=50)
        refresh_btn.bind(on_press=self.update_ssid)

        self.add_widget(self.label)
        self.add_widget(refresh_btn)

        # Первичное обновление
        self.update_ssid()

    def update_ssid(self, *args):
        ssid = get_current_wifi_ssid()
        self.label.text = f"📡 Сеть: {ssid}"

class WifiApp(App):
    def build(self):
        return WifiDisplay()

if __name__ == "__main__":
    WifiApp().run()
