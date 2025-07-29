from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
import socket

def generate_client_info_pdu(username, password, domain, client_name="RDP-COPILOT", working_dir="C:\\"):
    def to_unicode_bytes(s):
        return s.encode("utf-16le") + b"\x00\x00"

    user_bytes = to_unicode_bytes(username)
    pass_bytes = to_unicode_bytes(password)
    domain_bytes = to_unicode_bytes(domain)
    client_bytes = to_unicode_bytes(client_name)
    dir_bytes = to_unicode_bytes(working_dir)

    pdu = b""
    pdu += b"\x03\x00"              # TPKT Header
    pdu += b"\x00\x00"              # Placeholder for length
    pdu += b"\x02\xf0\x80"          # X.224 Header
    pdu += b"\x64\x00\x06\x03\xf0\x7f"  # MCS Header (simplified)

    pdu += b"\x00\x00\x00\x00"      # CodePage = Unicode
    pdu += b"\x01\x00\x00\x00"      # Flags

    pdu += user_bytes
    pdu += domain_bytes
    pdu += pass_bytes
    pdu += client_bytes
    pdu += dir_bytes

    total_length = len(pdu)
    pdu = pdu[:2] + total_length.to_bytes(2, "big") + pdu[4:]
    return pdu

class RDPAutoLogin(BoxLayout):
    def __init__(self, **kwargs):
        super(RDPAutoLogin, self).__init__(orientation="vertical", **kwargs)

        self.status_label = Label(text="🔐 RDP Login Panel", font_size=22)
        connect_btn = Button(text="Connect as afirnd")
        connect_btn.bind(on_press=self.auto_connect)

        self.add_widget(self.status_label)
        self.add_widget(connect_btn)

    def auto_connect(self, instance):
        ip = "192.168.130.39"
        port = 3389

        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(5)
            s.connect((ip, port))

            # Отправка X.224
            x224 = bytes([
                0x03, 0x00, 0x00, 0x13,
                0x0e, 0xe0, 0x00, 0x00,
                0x00, 0x00, 0x00, 0x01,
                0x00, 0x08, 0x00, 0x03,
                0x00, 0x00, 0x00
            ])
            s.send(x224)
            s.recv(1024)

            # Генерация и отправка Client Info PDU
            pdu = generate_client_info_pdu("afirnd", "afifarm5!", "")
            s.send(pdu)
            response = s.recv(2048)
            s.close()

            hex_resp = response.hex()[:64]
            self.status_label.text = f"📨 Server Response:\n{hex_resp}..."
        except Exception as e:
            self.status_label.text = f"⚠️ Connection failed: {e}"

class RDPAutoLoginApp(App):
    def build(self):
        return RDPAutoLogin()

if __name__ == "__main__":
    RDPAutoLoginApp().run()
