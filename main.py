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
        self.port_input = TextInput(text="8080", multiline=False, hint_text="Порт")
        self.output_label = Label(text="Готов к подключению")

        connect_btn = Button(text="Подключиться")
        connect_btn.bind(on_press=self.connect_to_server)

        self.add_widget(Label(text="Введи IP и порт"))
        self.add_widget(self.ip_input)
        self.add_widget(self.port_input)
        self.add_widget(connect_btn)
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
            s.send("Привет, сервер!".encode("utf-8"))  # ✔ теперь корректно
            response = s.recv(1024).decode()
            self.output_label.text = f"✅ Ответ: {response}"
            s.close()
        except PermissionError:
            self.output_label.text = "❌ Android запрещает доступ. Попробуй другой порт."
        except socket.timeout:
            self.output_label.text = "⌛ Таймаут: сервер не отвечает"
        except Exception as e:
            self.output_label.text = f"⚠️ Ошибка: {e}"

class SocketApp(App):
    def build(self):
        return SocketClient()

if __name__ == "__main__":
    SocketApp().run()
