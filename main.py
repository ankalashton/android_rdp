from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.button import Button
import subprocess

class RDPClient(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', **kwargs)

        # Поля ввода
        self.ip_input = TextInput(hint_text="🖥️ IP-адрес", multiline=False, size_hint=(1, 0.1))
        self.port_input = TextInput(hint_text="🔌 Порт", multiline=False, size_hint=(1, 0.1))
        self.user_input = TextInput(hint_text="👤 Логин", multiline=False, size_hint=(1, 0.1))
        self.pass_input = TextInput(hint_text="🔒 Пароль", multiline=False, password=True, size_hint=(1, 0.1))

        # Лог
        self.log_label = Label(text="📜 Лог:\n", size_hint=(1, 0.4), valign='top')
        self.log_label.bind(size=self._update_log)

        # Кнопки
        connect_btn = Button(text="🔗 Подключиться", size_hint=(1, 0.1))
        connect_btn.bind(on_press=self.on_connect)

        clear_btn = Button(text="🧹 Очистить лог", size_hint=(1, 0.1))
        clear_btn.bind(on_press=self.on_clear)

        # Добавление виджетов
        self.add_widget(self.ip_input)
        self.add_widget(self.port_input)
        self.add_widget(self.user_input)
        self.add_widget(self.pass_input)
        self.add_widget(self.log_label)
        self.add_widget(connect_btn)
        self.add_widget(clear_btn)

    def _update_log(self, instance, value):
        self.log_label.text_size = (self.log_label.width, None)

    def on_connect(self, instance):
        ip = self.ip_input.text.strip()
        port = self.port_input.text.strip()
        user = self.user_input.text.strip()
        password = self.pass_input.text.strip()

        if not ip or not port or not user or not password:
            self.log_label.text += "\n⚠️ Укажите все поля!"
            return

        self.log_label.text += f"\n📡 Подключение к {ip}:{port} как {user}..."

        try:
            cmd = [
                "xfreerdp",
                f"/v:{ip}:{port}",
                f"/u:{user}",
                f"/p:{password}",
                "/cert-ignore"
            ]
            subprocess.Popen(cmd)
            self.log_label.text += "\n✅ Команда xfreerdp запущена!"
        except Exception as e:
            self.log_label.text += f"\n❌ Ошибка запуска: {e}"

    def on_clear(self, instance):
        self.log_label.text = "📜 Лог:\n"

class RDPApp(App):
    def build(self):
        return RDPClient()

if __name__ == "__main__":
    RDPApp().run()
