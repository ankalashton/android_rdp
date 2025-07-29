from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
import socket

class RDPClient(BoxLayout):
    def __init__(self, **kwargs):
        super(RDPClient, self).__init__(orientation="vertical", **kwargs)

        self.ip_input = TextInput(text="192.168.130.39", multiline=False, hint_text="IP адрес")
        self.port_input = TextInput(text="3389", multiline=False, hint_text="Порт")
        self.output_label = Label(text="Готов к проверке", size_hint_y=0.3)

        check_btn = Button(text="Проверить доступность")
        check_btn.bind(on_press=self.check_availability)

        connect_btn = Button(text="Отправить X.224 пакет")
        connect_btn.bind(on_press=self.send_x224)

        self.add_widget(Label(text="Введи IP и порт"))
        self.add_widget(self.ip_input)
        self.add_widget(self.port_input)
        self.add_widget(check_btn)
        self.add_widget(connect_btn)
        self.add_widget(self.output_label)

    def check_availability(self, instance):
        ip = self.ip_input.text.strip()
        try:
            port = int(self.port_input.text.strip())
            with socket.create_connection((ip, port), timeout=3):
                self.output_label.text = f"✅ Сервер {ip}:{port} доступен"
        except socket.timeout:
            self.output_label.text = f"⌛ Таймаут: сервер {ip}:{port} не отвечает"
        except Exception as e:
            self.output_label.text = f"❌ Недоступен: {e}"

    def send_x224(self, instance):
        ip = self.ip_input.text.strip()
        try:
            port = int(self.port_input.text.strip())
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(5)
            s.connect((ip, port))

            # X.224 Connection Request (19 байт)
            pkt = bytes([
                0x03, 0x00, 0x00, 0x13,  # TPKT header
                0x0e, 0xe0, 0x00, 0x00, 0x00, 0x00,
                0x00, 0x01, 0x00, 0x08, 0x00, 0x03,
                0x00, 0x00, 0x00
            ])
            s.send(pkt)
            response = s.recv(1024)
            s.close()

            hex_response = response.hex()
            self.output_label.text = f"📨 Ответ от сервера:\n{hex_response[:64]}..."
        except Exception as e:
            self.output_label.text = f"⚠️ Ошибка при отправке: {e}"

class RDPApp(App):
    def build(self):
        return RDPClient()

if __name__ == "__main__":
    RDPApp().run()
