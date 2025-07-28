from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
import socket

class RDPClient(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', **kwargs)
        self.output = Label(text="Нажми для подключения к RDP", size_hint_y=0.8)
        self.add_widget(self.output)

        btn = Button(text="Подключиться", size_hint_y=0.2)
        btn.bind(on_press=self.connect_rdp)
        self.add_widget(btn)

    def connect_rdp(self, instance):
        try:
            ip = "192.168.130.39"  # 💡 Замените на IP вашего RDP-сервера
            port = 3389
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(5)
            s.connect((ip, port))

            pkt = bytes([
                0x03, 0x00, 0x00, 0x13,
                0x0e, 0xe0, 0x00, 0x00, 0x00, 0x00,
                0x00, 0x01, 0x00, 0x08, 0x00, 0x03, 0x00, 0x00, 0x00
            ])
            s.send(pkt)
            response = s.recv(1024)
            s.close()

            self.output.text = f"[RDP] Ответ: {response.hex()}"
        except Exception as e:
            self.output.text = f"[Ошибка] {str(e)}"

class RDPApp(App):
    def build(self):
        return RDPClient()

if __name__ == "__main__":
    RDPApp().run()
