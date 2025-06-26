import requests


def send(service_name: str, status: int, url: str, webhook_url: str):
    payload = {
        "content": f":rotating_light: Service *{service_name}* ({url} return code `{status}`)"
    }
    try:
        response = requests.post(webhook_url, json=payload)
        response.raise_for_status()
    except Exception as e:
        print(f"[{service_name}] Error while sending webhook:", e)
        print(f"[{service_name}] Webhook response {response.status_code}: {response.text}")
