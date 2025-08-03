from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from smb.SMBConnection import SMBConnection
import threading

# Константы подключения
USERNAME = "afirnd"
PASSWORD = "afifarm5!"
IP_ADDRESS = "192.168.130.39"
SHARE_NAME = "Afimilk"
FOLDER = "Robot"
TARGET_FILE = "RMC.exe"

class SMBChecker(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', **kwargs)

        self.result_label = Label(
            text="🕒 Готов к проверке",
            font_size=20,
            size_hint_y=None,
            height=50
        )

        check_btn = Button(
            text="🔍 Проверить RMC.exe",
            size_hint_y=None,
            height=50
        )
        check_btn.bind(on_press=self.start_check)

        self.add_widget(self.result_label)
        self.add_widget(check_btn)

    def start_check(self, *args):
        self.result_label.text = "⏳ Идёт проверка..."
        threading.Thread(target=self.check_file).start()

    def check_file(self):
        try:
            print("🔗 Пытаемся подключиться к SMB...")
            conn = SMBConnection(
                USERNAME,
                PASSWORD,
                "android_kivy",   # имя клиента
                "smb_host",       # имя хоста
                use_ntlm_v2=True
            )

            connected = conn.connect(IP_ADDRESS, 445, timeout=5)
            if connected:
                print("✅ Успешное подключение к SMB.")
                files = conn.listPath(SHARE_NAME, f"/{FOLDER}")
                print(f"📁 Получено {len(files)} файлов:")
                for f in files:
                    print(" -", f.filename)

                found = any(f.filename.lower() == TARGET_FILE.lower() for f in files)
                if found:
                    self.update_label(f"✅ Файл {TARGET_FILE} найден!")
                else:
                    self.update_label(f"❌ Файл {TARGET_FILE} не найден.")
            else:
                self.update_label("🔌 Не удалось подключиться к SMB.")
            conn.close()

        except Exception as e:
            print("⚠️ Ошибка при подключении к SMB:", str(e))
            self.update_label(f"⚠️ Ошибка: {str(e)}")

    def update_label(self, text):
        # Обновление метки с результатом (в основном потоке)
        self.result_label.text = text

class SMBCheckerApp(App):
    def build(self):
        print("🚀 Приложение запускается!")
        return SMBChecker()

if __name__ == "__main__":
    SMBCheckerApp().run()
