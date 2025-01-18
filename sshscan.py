import paramiko
import socket
from concurrent.futures import ThreadPoolExecutor

def ssh_scan(ip, username, password, port=22, timeout=3):
    """
    Проверяет доступность SSH на заданном IP-адресе.
    
    :param ip: IP-адрес для проверки
    :param username: Имя пользователя для SSH
    :param password: Пароль для SSH
    :param port: Порт для SSH (по умолчанию 22)
    :param timeout: Таймаут подключения (в секундах)
    :return: Результат проверки (успешно или нет)
    """
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(ip, port=port, username=username, password=password, timeout=timeout)
        print(f"[+] SSH доступен: {ip}")
        client.close()
        return ip
    except (socket.error, paramiko.AuthenticationException, paramiko.SSHException):
        print(f"[-] SSH недоступен: {ip}")
        return None
def scan_local_network(start_ip, end_ip, username, password):
    """
    Сканирует диапазон IP-адресов на доступность SSH.
    
    :param start_ip: Начальный IP-адрес диапазона
    :param end_ip: Конечный IP-адрес диапазона
    :param username: Имя пользователя для SSH
    :param password: Пароль для SSH
    :return: Список доступных IP-адресов
    """
    from ipaddress import ip_address
    start = ip_address(start_ip)
    end = ip_address(end_ip)
    accessible_ips = []

    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [
            executor.submit(ssh_scan, str(ip_address(ip)), username, password)
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
    username = "root"  # Замените на нужное имя пользователя
    password = "root"  # Замените на правильный пароль

    print("Сканирование началось...")
    results = scan_local_network(start_ip, end_ip, username, password)
    print("Доступные SSH-хосты:")
    print("\n".join(results) if results else "Не найдено доступных хостов.")

