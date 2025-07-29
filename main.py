from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from jnius import autoclass

def get_current_wifi_ssid():
    Context = autoclass('android.content.Context')
    PythonActivity = autoclass('org.kivy.android.PythonActivity')
    activity = PythonActivity.mActivity
    wifi_service = activity.getSystemService(Context.WIFI_SERVICE)
    info = wifi_service.getConnectionInfo()
    ssid = info.getSSID()

    if ssid.startswith('"') and ssid.endswith('"'):
        ssid = ssid[1:-1]  # убираем лишние кавычки
    return ssid

class WifiDisplay(BoxLayout):
    def __init__(self, **kwargs):
        super(WifiDisplay, self).__init__(orientation='vertical', **kwargs)
        ssid = get_current_wifi_ssid()
        self.label = Label(text=f"📡 Сеть: {ssid}", font_size=24)
        self.add_widget(self.label)

class WifiApp(App):
    def build(self):
        return WifiDisplay()

if __name__ == "__main__":
    WifiApp().run()
