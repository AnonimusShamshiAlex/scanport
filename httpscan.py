import socket
import ipaddress

def scan_http(ip_range):
    for ip in ipaddress.IPv4Network(ip_range):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)  # Устанавливаем таймаут в 1 секунду
        result = sock.connect_ex((str(ip), 80))  # Проверяем порт 80 (HTTP)
        if result == 0:
            print(f'HTTP доступен на {ip}')
        sock.close()

# Пример использования
scan_http('192.168.1.0/24')  # Используйте адрес сети
