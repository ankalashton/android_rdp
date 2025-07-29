import socket
import logging
from datetime import datetime
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.logger import Logger

# === 🔧 Файл-логгер ===
def setup_file_logging():
    log_file = "/sdcard/nfs-log.txt"  # проверь путь, если на Android
    file_handler = logging.FileHandler(log_file, encoding="utf-8")
    formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')
    file_handler.setFormatter(formatter)
    logging.getLogger().addHandler(file_handler)
    Logger.info("📁 Логгер настроен: %s", log_file)

def log(stage):
    msg = f"[{datetime.now().strftime('%H:%M:%S')}] {stage}"
    print(msg)
    Logger.info(msg)

# === 🔍 Проверка сети ===
def is_host_reachable(ip, port, timeout=3):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(timeout)
            return sock.connect_ex((ip, port)) == 0
    except Exception as e:
        log(f"⚠️ Сетевая проверка: {e}")
        return False

# === ✏️ Генераторы PDU ===
def generate_client_info_pdu(username, password, domain, client_name="RDP-COPILOT", working_dir="C:\\"):
    def to_unicode_bytes(s): return s.encode("utf-16le") + b"\x00\x00"
    fields = [to_unicode_bytes(username), to_unicode_bytes(domain), to_unicode_bytes(password),
              to_unicode_bytes(client_name), to_unicode_bytes(working_dir)]
    pdu = b"\x03\x00\x00\x00\x02\xf0\x80\x64\x00\x06\x03\xf0\x7f" + b"\x00\x00\x00\x00\x01\x00\x00\x00" + b"".join(fields)
    length = len(pdu)
    return pdu[:2] + length.to_bytes(2, "big") + pdu[4:]

def generate_security_exchange_pdu():
    return bytes.fromhex("03 00 00 0B 02 F0 80 30 00 02 00")

def generate_confirm_active_pdu():
    return bytes.fromhex("03 00 01 33 02 F0 80 6F 00 03 00 EB 03 00 00 03 00 00 00") + bytes([0x20] * 300)

# === 📡 Основной виджет ===
class RDPAutoLogin(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation="vertical", **kwargs)
        setup_file_logging()
        self.status_label = Label(text="🔐 RDP Auto Login", font_size=22)
        connect_btn = Button(text="🔌 Connect to RDP")
        connect_btn.bind(on_press=self.auto_connect)
        self.add_widget(self.status_label)
        self.add_widget(connect_btn)

    def auto_connect(self, instance):
        ip = "192.168.130.39"
        port = 3389
        username, password, domain = "afirnd", "afifarm5!", ""

        if not is_host_reachable(ip, port):
            log("❌ Хост недоступен — отмена подключения")
            self.status_label.text = f"🚫 Хост недоступен: {ip}:{port}"
            return

        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(10)
            log(f"🔗 Подключение к {ip}:{port}")
            start_time = datetime.now()
            s.connect((ip, port))
            log("✅ Соединение установлено")

            def timed_send_recv(label, payload, recv_len=1024):
                log(f"➡️ {label}")
                t1 = datetime.now()
                s.send(payload)
                resp = s.recv(recv_len)
                t2 = datetime.now()
                log(f"📥 Ответ ({len(resp)} байт) за {(t2 - t1).total_seconds():.2f} сек")
                return resp

            x224 = bytes.fromhex("030000130ee000000000000100080003000000")
            timed_send_recv("X.224", x224)

            client_info = generate_client_info_pdu(username, password, domain)
            timed_send_recv("Client Info PDU", client_info, 2048)

            sec_pdu = generate_security_exchange_pdu()
            timed_send_recv("Security Exchange", sec_pdu)

            confirm = generate_confirm_active_pdu()
            response = timed_send_recv("Confirm Active", confirm, 2048)

            s.close()
            duration = (datetime.now() - start_time).total_seconds()
            hex_resp = response.hex().upper()
            preview = "\n".join([hex_resp[i:i+32] for i in range(0, min(len(hex_resp), 128), 32)])
            self.status_label.text = f"📨 Ответ сервера:\n{preview}...\n⏱️ Время подключения: {duration:.2f} сек"
        except Exception as e:
            log(f"❌ Ошибка: {e}")
            self.status_label.text = f"⚠️ Ошибка: {e}"

class RDPAutoLoginApp(App):
    def build(self):
        return RDPAutoLogin()

if __name__ == "__main__":
    RDPAutoLoginApp().run()
