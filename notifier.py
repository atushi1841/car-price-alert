import os
import smtplib
import ssl
from email.mime.text import MIMEText
from email.utils import formatdate

def send_alert(alert, matches):
    smtp_host = os.environ.get("SMTP_HOST")
    smtp_user = os.environ.get("SMTP_USER")
    smtp_pass = os.environ.get("SMTP_PASS")
    smtp_port = int(os.environ.get("SMTP_PORT", "587"))
    notify_from = os.environ.get("NOTIFY_FROM")

    if not (smtp_host and smtp_user and smtp_pass and notify_from):
        print("[notify]", alert.get("model"), "matches:", matches)
        return

    subject = f"[PriceAlert] {alert.get('model')} が希望価格以下で見つかりました"
    body_lines = [f"希望上限価格: {alert.get('max_price')}円", ""]
    for m in matches:
        body_lines.append(f"- {m.get('title')} / {m.get('price')}円 / {m.get('detailUrl')}")
    body = "\n".join(body_lines)

    msg = MIMEText(body, "plain", "utf-8")
    msg["Subject"] = subject
    msg["From"] = notify_from
    msg["To"] = alert.get("email")
    msg["Date"] = formatdate(localtime=True)

    context = ssl.create_default_context()
    with smtplib.SMTP(smtp_host, smtp_port) as server:
        server.starttls(context=context)
        server.login(smtp_user, smtp_pass)
        server.sendmail(notify_from, [alert.get("email")], msg.as_string())
