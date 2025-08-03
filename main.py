import socket
from smb.SMBConnection import SMBConnection

IP_ADDRESS = "192.168.130.39"
PORT = 445
USERNAME = "afirnd"
PASSWORD = "afifarm5!"  # Замени на свой пароль
SERVICE_NAME = "Afimilk"  # Замени на имя общего ресурса


def check_port(ip, port):
    sock = socket.socket()
    sock.settimeout(3)
    try:
        sock.connect((ip, port))
        print(f"✅ Порт {port} на {ip} доступен.")
        return True
    except Exception as e:
        print(f"❌ Порт {port} недоступен: {e}")
        return False

def connect_to_smb():
    print("🔎 Проверка порта...")
    if not check_port(IP_ADDRESS, PORT):
        print("⛔ Соединение невозможно: порт недоступен.")
        return

    print("🔗 Подключение к SMB...")
    conn = SMBConnection(USERNAME, PASSWORD, "client_machine", "server_name", use_ntlm_v2=True)
    try:
        connected = conn.connect(IP_ADDRESS, PORT, timeout=5)
        print(f"📡 Статус подключения: {connected}")
        if connected:
            print("✅ Успешное подключение к SMB!")
            # Можно выполнить действия, например:
            # shares = conn.listShares()
            # for share in shares:
            #     print("📁", share.name)
        else:
            print("❌ Не удалось подключиться к SMB.")
    except ConnectionResetError:
        print("🚫 Сервер сбросил соединение. Проверь настройки SMB или аутентификацию.")
    except Exception as e:
        print(f"⚠️ Ошибка при подключении: {e}")

if __name__ == "__main__":
    connect_to_smb()
