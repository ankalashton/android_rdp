from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
import socket
from datetime import datetime

def log(stage):
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {stage}")

def generate_client_info_pdu(username, password, domain, client_name="RDP-COPILOT", working_dir="C:\\"):
    def to_unicode_bytes(s):
        return s.encode("utf-16le") + b"\x00\x00"

    user_bytes = to_unicode_bytes(username)
    pass_bytes = to_unicode_bytes(password)
    domain_bytes = to_unicode_bytes(domain)
    client_bytes = to_unicode_bytes(client_name)
    dir_bytes = to_unicode_bytes(working_dir)

    pdu = b"\x03\x00\x00\x00"              # TPKT header
    pdu += b"\x02\xf0\x80"
    pdu += b"\x64\x00\x06\x03\xf0\x7f"
    pdu += b"\x00\x00\x00\x00"
    pdu += b"\x01\x00\x00\x00"
    pdu += user_bytes + domain_bytes + pass_bytes + client_bytes + dir_bytes
    length = len(pdu)
    pdu = pdu[:2] + length.to_bytes(2, "big") + pdu[4:]
    return pdu

def generate_security_exchange_pdu():
    return bytes.fromhex("03 00 00 0B 02 F0 80 30 00 02 00")

def generate_confirm_active_pdu():
    header = bytes.fromhex("03 00 01 33 02 F0 80 6F 00 03 00 EB 03 00 00 03 00 00 00")
    dummy_payload = bytes([0x20] * 300)
    return header + dummy_payload

class RDPAutoLogin(BoxLayout):
    def __init__(self, **kwargs):
        super(RDPAutoLogin, self).__init__(orientation="vertical", **kwargs)

        self.status_label = Label(text="🔐 RDP Auto Login", font_size=22)
        connect_btn = Button(text="🔌 Connect to RDP")
        connect_btn.bind(on_press=self.auto_connect)

        self.add_widget(self.status_label)
        self.add_widget(connect_btn)

    def auto_connect(self, instance):
        ip = "192.168.130.39"
        port = 3389
        username = "afirnd"
        password = "afifarm5!"
        domain = ""

        try:
            log("Создание сокета")
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(10)

            log(f"Подключение к {ip}:{port}")
            start_time = datetime.now()
            s.connect((ip, port))
            log("Соединение установлено")

            log("➡️ Отправка X.224 Connection Request")
            x224 = bytes.fromhex("030000130ee000000000000100080003000000")
            s.send(x224)
            resp1 = s.recv(1024)
            log(f"✅ Получен ответ X.224 ({len(resp1)} байт)")

            log("➡️ Отправка Client Info PDU")
            client_info = generate_client_info_pdu(username, password, domain)
            s.send(client_info)
            resp2 = s.recv(2048)
            log(f"✅ Получен ответ Client Info ({len(resp2)} байт)")

            log("➡️ Отправка Security Exchange PDU")
            sec_pdu = generate_security_exchange_pdu()
            s.send(sec_pdu)
            resp3 = s.recv(1024)
            log(f"✅ Получен ответ Security ({len(resp3)} байт)")

            log("➡️ Отправка Client Confirm Active PDU")
            confirm = generate_confirm_active_pdu()
            s.send(confirm)
            response = s.recv(2048)
            log(f"✅ Получен финальный ответ ({len(response)} байт)")

            s.close()
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()

            hex_resp = response.hex().upper()
            preview = "\n".join([hex_resp[i:i+32] for i in range(0, min(len(hex_resp), 128), 32)])
            self.status_label.text = f"📨 Ответ сервера:\n{preview}...\n⏱️ Время подключения: {duration:.2f} сек"
        except Exception as e:
            log(f"❌ Ошибка подключения: {e}")
            self.status_label.text = f"⚠️ Ошибка: {e}"

class RDPAutoLoginApp(App):
    def build(self):
        return RDPAutoLogin()

if __name__ == "__main__":
    RDPAutoLoginApp().run()
