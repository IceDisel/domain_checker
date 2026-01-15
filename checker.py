"""
checker.py

Точка входа в проект domain_checker.

Этот файл:
- читает список доменов
- запускает все проверки
- анализирует результаты
- выводит человеку понятный диагноз
"""

from checks.ping import check_internet
from checks.dns import resolve_domain
from checks.http import check_https
from checks.tls import check_https_via_ip


def load_domains(path: str = "domains.txt") -> list[str]:
    """
    Загружает список доменов из файла.

    Формат файла:
    - один домен на строку
    - пустые строки игнорируются
    - строки с # считаются комментариями

    :param path: путь к файлу domains.txt
    :return: список доменов
    """

    domains: list[str] = []

    with open(path, "r", encoding="utf-8") as file:
        for line in file:
            domain = line.strip()

            # Пропускаем пустые строки и комментарии
            if not domain or domain.startswith("#"):
                continue

            domains.append(domain)

    return domains


def diagnose_domain(domain: str) -> None:
    """
    Выполняет полный набор проверок для одного домена
    и печатает диагностический результат.
    """

    print(f"\n🔍 Проверка домена: {domain}")

    # 1️⃣ Проверка наличия интернета вообще
    if not check_internet():
        print("❌ Нет интернет-соединения вообще")
        return

    print("✅ Интернет доступен")

    # 2️⃣ DNS-проверка
    ip_address = resolve_domain(domain)

    if not ip_address:
        print("❌ DNS не резолвится (возможна DNS-блокировка)")
        return

    print(f"🌍 DNS OK → {ip_address}")

    # 3️⃣ HTTPS по домену
    https_result = check_https(domain)
    print(f"🌐 HTTPS по домену → {https_result}")

    # 4️⃣ HTTPS напрямую по IP
    if https_result != 200:
        ip_https_result = check_https_via_ip(ip_address, domain)
        print(f"🧪 HTTPS через IP → {ip_https_result}")

    # 5️⃣ Простейшая интерпретация
    print("📊 Диагноз:")

    if https_result == 200:
        print("  ✅ Сайт доступен без ограничений")

    elif https_result in ("Timeout", "Connection error", "SSL error"):
        if isinstance(ip_https_result, int):
            print("  🚫 Похоже на DNS или SNI-блокировку")

        else:
            print("  🚫 Вероятна DPI / фильтрация провайдером")

    elif isinstance(https_result, int):
        print(f"  ⚠️ Сервер отвечает, но статус {https_result}")

    else:
        print("  ❓ Не удалось определить причину")


def main() -> None:
    """
    Основная точка запуска программы.
    """

    domains = load_domains()

    if not domains:
        print("⚠️ Файл domains.txt пуст или не найден")
        return

    for domain in domains:
        diagnose_domain(domain)


if __name__ == "__main__":
    main()


# if __name__ == "__main__":
#     print("Проверка Интернета ping 1.1.1.1:")
#     print("Internet:", check_internet(), "\n")
#
#     print("Проверка домена через системный DNS:")
#     print("google.com →", resolve_domain("google.com"))
#     print("nonexistent-domain-xyz.test →", resolve_domain("nonexistent-domain-xyz.test"), "\n")
#
#     print("Проверка доступности сайта через HTTPS:")
#     print("google.com →", check_https("google.com"))
#     print("example.com →", check_https("example.com"), "\n")
#
#     print("Проверяет доступность HTTPS-сайта через IP + Host:")
#     print(check_https_via_ip("1.1.1.1", "cloudflare.com"))
#