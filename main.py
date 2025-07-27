from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button


class RDPConnectScreen(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', **kwargs)

        # 📋 Label для логов
        self.log_label = Label(
            text="⏳ Журнал подключений будет здесь",
            halign="left",
            valign="top",
            size_hint_y=None,
            height=500
        )
        self.log_label.bind(
            texture_size=lambda instance, value: setattr(instance, 'height', value[1])
        )

        # 🧭 ScrollView c логом
        scroll = ScrollView(
            size_hint=(1, 0.6),
            do_scroll_x=False,
            do_scroll_y=True
        )
        scroll.add_widget(self.log_label)
        self.add_widget(scroll)

        # 🔘 Кнопка "Подключиться"
        connect_button = Button(
            text="🔌 Подключиться",
            size_hint=(1, 0.2)
        )
        connect_button.bind(on_press=self.on_connect)
        self.add_widget(connect_button)

        # 🔘 Кнопка "Очистить лог"
        clear_button = Button(
            text="🧹 Очистить лог",
            size_hint=(1, 0.2)
        )
        clear_button.bind(on_press=self.clear_log)
        self.add_widget(clear_button)

    def on_connect(self, instance):
        # ⚠️ Здесь будет логика подключения
        self.log_label.text += "\n✅ Попытка подключения..."

    def clear_log(self, instance):
        self.log_label.text = "🧾 Лог очищен."


class RDPApp(App):
    def build(self):
        return RDPConnectScreen()


if __name__ == "__main__":
    RDPApp().run()
