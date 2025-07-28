from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
import socket

class SocketClient(BoxLayout):
    def __init__(self, **kwargs):
        super(SocketClient, self).__init__(orientation="vertical", **kwargs)

        self.ip_input = TextInput(text="192.168.130.39", multiline=False, hint_text="IP адрес")
        self.port_input = TextInput(text="3389", multiline=False, hint_text="Порт")
        self.output_label = Label(text="Готов к подключению", size_hint_y=0.3)

        # Кнопка подключения
        connect_btn = Button(text="Подключиться")
        connect_btn.bind(on_press=self.connect_to_server)

        # Кнопка проверки доступности
        check_btn = Button(text="Проверить доступность")
        check_btn.bind(on_press=self.check_availability)

        # Добавление виджетов
        self.add_widget(Label(text="Введи IP и порт"))
        self.add_widget(self.ip_input)
        self.add_widget(self.port_input)
        self.add_widget(connect_btn)
        self.add_widget(check_btn)
        self.add_widget(self.output_label)

    def connect_to_server(self, instance):
        ip = self.ip_input.text.strip()
        try:
            port = int(self.port_input.text.strip())
        except ValueError:
            self.output_label.text = "❌ Некорректный порт"
            return

        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(5)
            s.connect((ip, port))
            s.send("Привет, сервер!".encode("utf-8"))
            response = s.recv(1024).decode(errors="ignore")
            self.output_label.text = f"✅ Ответ: {response}"
            s.close()
        except socket.timeout:
            self.output_label.text = "⌛ Сервер не отвечает (таймаут)"
        except ConnectionRefusedError:
            self.output_label.text = "🚫 Подключение отклонено — возможно, требуется авторизация RDP"
        except OSError as e:
            self.output_label.text = f"⚠️ Ошибка сокета: {e}"
        except Exception as e:
            self.output_label.text = f"❌ Неизвестная ошибка: {e}"

    def check_availability(self, instance):
        ip = self.ip_input.text.strip()
        try:
            port = int(self.port_input.text.strip())
        except ValueError:
            self.output_label.text = "❌ Некорректный порт"
            return

        try:
            with socket.create_connection((ip, port), timeout=3):
                self.output_label.text = f"✅ Сервер {ip}:{port} доступен"
        except socket.timeout:
            self.output_label.text = f"⌛ Таймаут: сервер {ip}:{port} не отвечает"
        except Exception as e:
            self.output_label.text = f"❌ Недоступен: {e}"

class SocketApp(App):
    def build(self):
        return SocketClient()

if __name__ == "__main__":
    SocketApp().run()
