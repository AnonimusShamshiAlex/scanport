import socket
from concurrent.futures import ThreadPoolExecutor

def rdp_scan(ip, port=3389, timeout=3):
    """
    Проверяет доступность RDP на заданном IP-адресе.
    
    :param ip: IP-адрес для проверки
    :param port: Порт для RDP (по умолчанию 3389)
    :param timeout: Таймаут подключения (в секундах)
    :return: Результат проверки (успешно или нет)
    """
    try:
        with socket.create_connection((ip, port), timeout=timeout) as conn:
            print(f"[+] RDP доступен: {ip}")
            return ip
    except (socket.timeout, socket.error):
        print(f"[-] RDP недоступен: {ip}")
        return None

def scan_rdp_local_network(start_ip, end_ip):
    """
    Сканирует диапазон IP-адресов на доступность RDP.
    
    :param start_ip: Начальный IP-адрес диапазона
    :param end_ip: Конечный IP-адрес диапазона
    :return: Список доступных IP-адресов
    """
    from ipaddress import ip_address
    start = ip_address(start_ip)
    end = ip_address(end_ip)
    accessible_ips = []

    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [
            executor.submit(rdp_scan, str(ip_address(ip)))
            for ip in range(int(start), int(end) + 1)
        ]
        for future in futures:
            result = future.result()
            if result:
                accessible_ips.append(result)
    
    return accessible_ips

if __name__ == "__main__":
    # Задайте диапазон IP
    start_ip = "192.168.1.1"
    end_ip = "192.168.1.254"

    print("Сканирование началось...")
    results = scan_rdp_local_network(start_ip, end_ip)
    print("Доступные RDP-хосты:")
    print("\n".join(results) if results else "Не найдено доступных хостов.")
