import os
import copy
import json
import yaml
import smtplib
import datetime
from email.header import Header
from email.mime.text import MIMEText

from utils.utils import format_date
from utils.generate_email_content import joint_email_content

with open("violet-logmin.yaml", mode='r', encoding="utf-8") as f:
    CONFIG = yaml.load(f, Loader=yaml.FullLoader)

SENDER_CONFIG = CONFIG["sender"]


def organize_html_email(members, receiver):
    email_header, email_body = joint_email_content(members, receiver)
    email = MIMEText(email_body, "html", "utf-8")
    email["From"] = CONFIG["sender"]["address"]
    email["To"] = receiver["address"]
    email["Subject"] = Header(email_header, "utf-8").encode()
    return email


def adjust_logs(members, receiver):
    """Put the receiver at the head of log list."""
    copied_members = copy.deepcopy(members)
    current_full_name = receiver["sur_name"] + receiver["given_name"]
    current_member = None
    for i, log in enumerate(copied_members):
        if log["name"] == current_full_name:
            current_member = copied_members.pop(i)
            break
    if current_member is None:
        return copied_members
    copied_members.insert(0, current_member)
    return copied_members


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
                  "log": "1. ...\n\n2. ...\n\n3. ..."}
        members.append(member)
    members = sorted(members, key=lambda i: i["grade"])

    return members


class LogMin:
    def __init__(self):
        self.logs_file = CONFIG["logs_file"]
        self.receivers = CONFIG["receivers"]
        self.sender_address = SENDER_CONFIG["address"]
        self.members = member_filter(self.receivers)
        self.server = smtplib.SMTP_SSL(SENDER_CONFIG["smtp_server"], 465, timeout=3)

    def build_mail_server(self):
        self.server.set_debuglevel(0)
        self.server.login(SENDER_CONFIG["address"], SENDER_CONFIG["authorization_code"])

    def store_logs(self):
        if not os.path.exists(self.logs_file):
            stored_logs = []
        else:
            with open(self.logs_file, mode='r', encoding="utf-8") as f:
                stored_logs = json.load(f)
        today = format_date(datetime.datetime.today())
        today_logs = {"date": today,
                       "logs": []}
        for member in self.members:
            item = {"name": member["name"],
                    "log": member["log"]}
            today_logs["logs"].append(item)
        stored_logs.append(today_logs)
        with open(self.logs_file, mode='w', encoding="utf-8") as f:
            json.dump(stored_logs, f, ensure_ascii=False)

LOGMIN = LogMin()

