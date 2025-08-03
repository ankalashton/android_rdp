from kivy.app import App
from kivy.uix.label import Label
from smb.SMBConnection import SMBConnection

USERNAME = "afirnd"
PASSWORD = "afifarm5!"
IP_ADDRESS = "192.168.130.39"
SHARE_NAME = "Afimilk"
FOLDER = "Robot"
TARGET_FILE = "RMC.exe"

class SMBCheckerApp(App):
    def build(self):
        self.label = Label(text="Проверка файла...")
        self.check_file()
        return self.label

    def check_file(self):
        try:
            conn = SMBConnection(USERNAME, PASSWORD, "android_kivy", "smb_host", use_ntlm_v2=True)
            connected = conn.connect(IP_ADDRESS, 445, timeout=3)

            if connected:
                files = conn.listPath(SHARE_NAME, f"/{FOLDER}")
                found = any(f.filename.lower() == TARGET_FILE.lower() for f in files)
                if found:
                    self.label.text = f"✅ Файл {TARGET_FILE} найден!"
                else:
                    self.label.text = f"❌ Файл {TARGET_FILE} не найден."
            else:
                self.label.text = "🔌 Не удалось подключиться к SMB."

        except Exception as e:
            self.label.text = f"⚠️ Ошибка: {str(e)}"

