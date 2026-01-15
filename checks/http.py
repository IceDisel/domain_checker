"""
http.py

Модуль для проверки доступности сайта по HTTP/HTTPS.

Проверка:
- выполняется HTTPS-запрос
- используются реальные таймауты
- аккуратно различаются типы ошибок
"""

import requests
from typing import Optional


def check_https(
    domain: str,
    timeout: int = 5
) -> Optional[int | str]:
    """
    Проверяет доступность сайта по HTTPS.

    :param domain: домен (example.com)
    :param timeout: таймаут запроса в секундах
    :return:
        int  — HTTP статус-код (200, 301, 403, 451, ...)
        str  — описание ошибки (Timeout, SSL error, Connection error)
        None — если произошло что-то совсем неожиданное
    """

    url = f"https://{domain}"

    try:
        response = requests.get(
            url,
            timeout=timeout,
            allow_redirects=True
        )

        # Если запрос дошёл до сервера — возвращаем статус
        return response.status_code

    except requests.exceptions.ConnectTimeout:
        # Сервер не ответил вовремя
        return "Timeout"

    except requests.exceptions.SSLError:
        # Часто бывает при:
        # - SNI-блокировке
        # - подмене сертификатов провайдером
        return "SSL error"

    except requests.exceptions.ConnectionError:
        # Ошибка соединения:
        # - TCP reset
        # - фильтрация провайдером
        return "Connection error"

    except Exception:
        # Любая другая непредвиденная ошибка
        return None
