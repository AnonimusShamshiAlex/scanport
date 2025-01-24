import socket
import ipaddress
from concurrent.futures import ThreadPoolExecutor

# Функция для проверки VNC-сервера на заданном IP и порту
def check_vnc(ip, port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1)  # Устанавливаем таймаут в 1 секунду
            result = s.connect_ex((str(ip), port))
            if result == 0:
                print(f'VNC сервер найден на {ip}:{port}')
    except Exception as e:
        print(f"Ошибка при проверке {ip}:{port} - {e}")

# Функция для сканирования диапазона IP-адресов
def scan_vnc(ip_range):
    with ThreadPoolExecutor(max_workers=100) as executor:  # Ограничиваем количество потоков
        for ip in ip_range:
            for port in range(5900, 6000):
                executor.submit(check_vnc, ip, port)

if __name__ == "__main__":
    # Задаем диапазон IP-адресов для сканирования
    network = ipaddress.ip_network('192.168.1.0/24')  # Замените на ваш диапазон
    print("Начинаем сканирование VNC-серверов...")
    scan_vnc(network)
    print("Сканирование завершено.")
