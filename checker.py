from checks.dns import resolve_domain
from checks.ping import check_internet

if __name__ == "__main__":
    print("Internet:", check_internet())
    print("google.com →", resolve_domain("google.com"))
    print("nonexistent-domain-xyz.test →", resolve_domain("nonexistent-domain-xyz.test"))
