import socket
import ipaddress

def scan_telnet(ip_range):
    for ip in ipaddress.IPv4Network(ip_range):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)  # Устанавливаем таймаут в 1 секунду
        result = sock.connect_ex((str(ip), 23))  # Проверяем порт 23 (Telnet)
        if result == 0:
            print(f'Telnet доступен на {ip}')
        sock.close()

# Пример использования
scan_telnet('192.168.1.0/24')
