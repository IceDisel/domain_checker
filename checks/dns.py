"""
dns.py

Модуль для проверки DNS-резолвинга домена.

Задача:
- понять, отвечает ли DNS
- получить IP-адрес домена
- отличить DNS-блокировку от других проблем
"""

import socket
from typing import Optional


def resolve_domain(domain: str) -> Optional[str]:
    """
    Пытается получить IP-адрес для домена через системный DNS.

    ВАЖНО:
    Мы используем системный DNS намеренно:
    - именно его чаще всего блокирует провайдер
    - так мы видим реальную картину для пользователя

    :param domain: доменное имя (example.com)
    :return:
        str  — IP-адрес, если резолв успешен
        None — если DNS не ответил или домен заблокирован
    """

    try:
        # gethostbyname:
        # - делает A-запрос (IPv4)
        # - использует системный DNS
        ip_address = socket.gethostbyname(domain)
        return ip_address

    except socket.gaierror:
        # gaierror возникает если:
        # - домен не существует
        # - DNS-сервер не отвечает
        # - провайдер подменяет / блокирует DNS
        return None
