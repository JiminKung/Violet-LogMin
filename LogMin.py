import yaml
import smtplib
from email.header import Header
from email.mime.text import MIMEText

from utils.generate_email_content import joint_email_content

with open("LogMin.yaml", mode='r', encoding="utf-8") as f:
    CONFIG = yaml.load(f, Loader=yaml.FullLoader)

def organize_html_email(logs, receiver):
    email_header, email_content = joint_email_content(logs, receiver)
    email = MIMEText(email_content, "html", "utf-8")
    email["From"] = CONFIG["sender"]["address"]
    email["To"] = receiver["address"]
    email["Subject"] = Header(email_header, "utf-8").encode()
    return email

def send_email(logs):
    server = smtplib.SMTP_SSL(CONFIG["sender"]["smtp_server"], 465, timeout=3)
    server.set_debuglevel(2)
    server.login(CONFIG["sender"]["address"], CONFIG["sender"]["authorization_code"])
    for receiver in CONFIG["receivers"]:
        email = organize_html_email(logs, receiver)
        server.sendmail(CONFIG["sender"]["address"], receiver["address"], email.as_string())
    server.quit()

if __name__ == "__main__":
    logs = [
        {
            "member": "张三",
            "events": ["Coding", "Reading paper"]
        },
        {
            "member": "王二",
            "events": ["上课", "阅读论文"]
        }
    ]
    send_email(logs)
