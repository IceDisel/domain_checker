"""
tls.py

Модуль для проверки HTTPS-доступности сайта
путём прямого подключения к IP-адресу.

Используется для диагностики:
- DNS-блокировок
- SNI-фильтрации
"""
import warnings
from urllib3.exceptions import InsecureRequestWarning

import requests
from typing import Optional

warnings.simplefilter("ignore", InsecureRequestWarning)


def check_https_via_ip(
    ip_address: str,
    domain: str,
    timeout: int = 5
) -> Optional[int | str]:
    """
    Проверяет доступность HTTPS-сайта через IP + Host.

    ВАЖНО:
    - verify=False → мы игнорируем SSL-сертификат
    - Host обязателен → иначе сервер не поймёт, кого обслуживать

    :param ip_address: IP-адрес сайта (например 142.250.74.206)
    :param domain: доменное имя (google.com)
    :param timeout: таймаут запроса
    :return:
        int  — HTTP статус-код
        str  — описание ошибки
        None — непредвиденная ошибка
    """

    url = f"https://{ip_address}"

    headers = {
        # Ключевой момент:
        # мы говорим серверу, какой сайт хотим открыть
        "Host": domain
    }

    try:
        response = requests.get(
            url,
            headers=headers,
            timeout=timeout,
            allow_redirects=True,
            verify=False  # игнорируем несоответствие сертификата
        )

        return response.status_code

    except requests.exceptions.ConnectTimeout:
        return "Timeout"

    except requests.exceptions.SSLError:
        # Даже с verify=False возможны ошибки при жесткой TLS-фильтрации
        return "SSL error"

    except requests.exceptions.ConnectionError:
        return "Connection error"

    except Exception:
        return None
