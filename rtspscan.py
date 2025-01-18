import socket
import ipaddress

def scan_rtsp_ports(network):
    # Преобразуем сеть в список IP-адресов
    net = ipaddress.ip_network(network, strict=False)  # Установите strict=False
    rtsp_ports = []

    for ip in net.hosts():
        # Проверяем доступность порта 554
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1)  # Устанавливаем таймаут
            result = s.connect_ex((str(ip), 554))
            if result == 0:
                rtsp_ports.append(str(ip))

    return rtsp_ports

# Пример использования
network = '192.168.1.1/24'  # Замените на вашу локальную сеть
found_rtsp_ports = scan_rtsp_ports(network)

print("Найденные RTSP порты:")
for ip in found_rtsp_ports:
    print(f"RTSP доступен на: rtsp://{ip}:554")
