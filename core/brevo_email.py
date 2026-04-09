import requests
from django.conf import settings


def send_brevo_email(subject, body, to_email='leelafoundation323@gmail.com'):
    """
    Send a transactional email via Brevo's REST API (HTTPS / port 443).
    This works on PythonAnywhere free accounts because SMTP ports (587/465)
    are blocked there but HTTPS (443) is always open.
    """
    api_key = getattr(settings, 'BREVO_API_KEY', None)

    if not api_key:
        print("[Brevo] ERROR: BREVO_API_KEY is not set in settings.")
        return False

    url = "https://api.brevo.com/v3/smtp/email"

    headers = {
        "accept": "application/json",
        "api-key": api_key,
        "content-type": "application/json",
    }

    payload = {
        "sender": {
            "name": "Leela Foundation",
            "email": "leelafoundation323@gmail.com",
        },
        "to": [{"email": to_email}],
        "subject": subject,
        "textContent": body,
    }

    try:
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        if response.status_code == 201:
            print(f"[Brevo] ✅ Email sent successfully → {to_email}")
            return True
        else:
            print(f"[Brevo] ❌ Failed. Status: {response.status_code} | Response: {response.text}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"[Brevo] ❌ Exception while sending email: {e}")
        return False
