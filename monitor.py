import os
import requests

URLS_TO_MONITOR = [
    "https://google.com",
    "https://github.com",
    "https://thisurldoesnotexist123456789.com",
]

DISCORD_WEBHOOK_URL = os.environ.get("DISCORD_WEBHOOK_URL")
TIMEOUT_SECONDS = 10

session = requests.Session()
session.headers.update(
    {"User-Agent": "github-uptime-monitor/1.0"}
)


def send_discord_alert(message):
    if not DISCORD_WEBHOOK_URL:
        print("DISCORD_WEBHOOK_URL is not configured.")
        return

    try:
        response = requests.post(
            DISCORD_WEBHOOK_URL,
            json={"content": message},
            timeout=10,
        )
        response.raise_for_status()
    except requests.RequestException as error:
        print(f"Could not send Discord alert: {error}")


def check_url(url):
    try:
        response = session.get(
            url,
            timeout=TIMEOUT_SECONDS,
            allow_redirects=True,
        )
        response.raise_for_status()
        print(f"UP: {url} ({response.status_code})")
    except requests.RequestException as error:
        message = f"ALERT: `{url}` is unavailable. Error: `{error}`"
        print(message)
        send_discord_alert(message)


def main():
    for url in URLS_TO_MONITOR:
        check_url(url)


if __name__ == "__main__":
    main()
