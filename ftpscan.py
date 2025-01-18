from ftplib import FTP, error_perm, error_temp, error_proto
import socket
from concurrent.futures import ThreadPoolExecutor

def ftp_scan(ip, username, password, port=21, timeout=3):
    """
    Проверяет доступность FTP на заданном IP-адресе.
    
    :param ip: IP-адрес для проверки
    :param username: Имя пользователя для FTP
    :param password: Пароль для FTP
    :param port: Порт для FTP (по умолчанию 21)
    :param timeout: Таймаут подключения (в секундах)
    :return: Результат проверки (успешно или нет)
    """
    try:
        ftp = FTP()
        ftp.connect(ip, port, timeout=timeout)
        ftp.login(username, password)
        print(f"[+] FTP доступен: {ip}")
        ftp.quit()
        return ip
    except (socket.error, error_perm, error_temp, error_proto):
        print(f"[-] FTP недоступен: {ip}")
        return None

def scan_ftp_local_network(start_ip, end_ip, username, password):
    """
    Сканирует диапазон IP-адресов на доступность FTP.
    
    :param start_ip: Начальный IP-адрес диапазона
    :param end_ip: Конечный IP-адрес диапазона
    :param username: Имя пользователя для FTP
    :param password: Пароль для FTP
    :return: Список доступных IP-адресов
    """
    from ipaddress import ip_address
    start = ip_address(start_ip)
    end = ip_address(end_ip)
    accessible_ips = []

    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [
            executor.submit(ftp_scan, str(ip_address(ip)), username, password)
            for ip in range(int(start), int(end) + 1)
        ]
        for future in futures:
            result = future.result()
            if result:
                accessible_ips.append(result)
    
    return accessible_ips

if __name__ == "__main__":
    # Задайте диапазон IP, имя пользователя и пароль
    start_ip = "192.168.1.1"
    end_ip = "192.168.1.254"
    username = "anonymous"  # Для публичных FTP можно использовать 'anonymous'
    password = ""           # Пароль для 'anonymous' может быть пустым или адресом электронной почты

    print("Сканирование началось...")
    results = scan_ftp_local_network(start_ip, end_ip, username, password)
    print("Доступные FTP-хосты:")
    print("\n".join(results) if results else "Не найдено доступных хостов.")
