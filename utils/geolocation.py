import requests


def get_client_ip(request):
    """Extract the client's real IP address."""
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0]
    else:
        ip = request.META.get("REMOTE_ADDR")
    return ip


def get_city_from_ip(request):
    """Get city name from IP address using ipinfo.io"""
    ip = get_client_ip(request)
    if ip in ["127.0.0.1", "localhost"]:  # Handle local development
        return "Localhost"

    try:
        response = requests.get(f"https://ipinfo.io/{ip}/json")
        data = response.json()
        return data.get("city")
    except requests.RequestException:
        return None
