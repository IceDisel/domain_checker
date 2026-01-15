"""
ping.py

Модуль для проверки наличия интернет-соединения.

Идея:
Мы не используем ICMP ping, потому что:
- на Windows он может быть заблокирован
- провайдеры могут фильтровать ICMP

Вместо этого:
- открываем TCP-соединение к известному публичному DNS-серверу
- если соединение установилось — интернет есть
"""

import socket


def check_internet(
    host: str = "1.1.1.1",
    port: int = 53,
    timeout: int = 3
) -> bool:
    """
    Проверяет, есть ли доступ в интернет.

    Пытаемся установить TCP-соединение с DNS-сервером Cloudflare (1.1.1.1:53)

    :param host: IP-адрес для проверки (по умолчанию 1.1.1.1)
    :param port: Порт (53 — DNS)
    :param timeout: Таймаут в секундах
    :return: True — интернет есть, False — нет
    """

    try:
        # create_connection:
        # - пытается открыть TCP-сокет
        # - автоматически выбирает IPv4/IPv6
        # - выбрасывает исключение при ошибке
        with socket.create_connection((host, port), timeout=timeout):
            return True

    except (OSError, socket.timeout):
        # Любая ошибка здесь означает:
        # - нет маршрута
        # - сеть отключена
        # - провайдер полностью отрубил интернет
        return False
