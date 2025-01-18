import socket
import ipaddress

def check_port(ip, port):
    """Проверяет, открыт ли указанный порт на заданном IP-адресе."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(1)  # Устанавливаем таймаут в 1 секунду
    result = sock.connect_ex((ip, port))
    sock.close()
    return result == 0

def scan_network(network, port):
    """Сканирует заданную сеть на наличие открытого порта."""
    for ip in ipaddress.IPv4Network(network):
        if check_port(str(ip), port):
            print(f"Порт {port} открыт на {ip}")
        else:
            print(f"Порт {port} закрыт на {ip}")

if __name__ == "__main__":
    # Задайте диапазон сети и порт для проверки
    network_range = "192.168.1.0/24"  # Пример диапазона
    port_to_check = 9100

    print(f"Сканирование сети {network_range} на порт {port_to_check}...")
    scan_network(network_range, port_to_check)
