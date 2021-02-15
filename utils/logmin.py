import copy
import yaml
import smtplib
from email.header import Header
from email.mime.text import MIMEText

from utils.generate_email_content import joint_email_content

with open("violet-logmin.yaml", mode='r', encoding="utf-8") as f:
    CONFIG = yaml.load(f, Loader=yaml.FullLoader)

SENDER_CONFIG = CONFIG["sender"]


def organize_html_email(logs, receiver):
    email_header, email_body = joint_email_content(logs, receiver)
    email = MIMEText(email_body, "html", "utf-8")
    email["From"] = CONFIG["sender"]["address"]
    email["To"] = receiver["address"]
    email["Subject"] = Header(email_header, "utf-8").encode()
    return email


def adjust_logs(logs, receiver):
    """Put the receiver at the head of log list."""
    copied_logs = copy.deepcopy(logs)
    current_full_name = receiver["sur_name"] + receiver["given_name"]
    current_log = None
    for i, log in enumerate(copied_logs):
        if log["name"] == current_full_name:
            current_log = copied_logs.pop(i)
            break
    if current_log is None:
        return
    copied_logs.insert(0, current_log)
    return copied_logs

def member_filter(receivers):
    members = []
    for receiver in receivers:
        if receiver["degree"] == "Prof.":
            continue
        full_name = receiver["sur_name"] + receiver["given_name"]
        grade = receiver["grade"]
        address = receiver["address"]
        member = {"name": full_name,
                  "grade": grade,
                  "address": address,
                  "register_state": False,
                  "events": "1. ...\n2. ...\n3. ..."}
        members.append(member)

    members = sorted(members, key=lambda i: i["grade"])

    return members


class LogMin:
    def __init__(self):
        self.receivers = CONFIG["receivers"]
        self.members = member_filter(self.receivers)
        self.server = smtplib.SMTP_SSL(SENDER_CONFIG["smtp_server"], 465, timeout=3)

    def send_email(self):
        self.server.set_debuglevel(2)
        self.server.login(SENDER_CONFIG["address"], SENDER_CONFIG["authorization_code"])
        for receiver in self.receivers:
            adjusted_members = adjust_logs(self.members, receiver)
            email = organize_html_email(adjusted_members, receiver)
            self.server.sendmail(SENDER_CONFIG["address"], receiver["address"], email.as_string())
        self.server.quit()

LOGMIN = LogMin()

if __name__ == "__main__":
    logs = [
        {
            "member": "张三",
            "events": ["Coding", "Reading paper"]
        },
        {
            "member": "王二",
            "events": ["上课", "阅读论文"]
        },
        {
            "member": "李四",
            "events": ["干饭", "睡大觉"]
        }
    ]
    receivers = CONFIG["receivers"]
    members = member_filter(receivers)
