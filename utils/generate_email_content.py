import yaml
import requests
import datetime
import random

with open("Violet-LogMin.yaml", mode='r', encoding="utf-8") as f:
    CONFIG = yaml.load(f, Loader=yaml.FullLoader)

RESULT = requests.get(CONFIG["shanbay"]["url"]).json()


def generate_email_header():
    today = datetime.date.today()
    return "Log of {} {}".format(CONFIG["group"]["name"], today)


def generate_email_salutation(degree, sur_name):
    return "<p>&ensp;&ensp;Dear {} {}</p>".format(degree, sur_name)


def generate_email_opener():
    url = CONFIG["project"]["github"]
    opener = random.choice(CONFIG["email"]["opener"])
    return "<p>&ensp;&ensp;This is <a href='{}'>LogMin</a>, an auto-log robot. {}</p>".format(url, opener)


def generate_log_table(logs):
    table_header = "<tr><th>{}</th><th>{}</th></tr>".format("Member", "Events")
    member_events = ""
    for log in logs:
        events = ""
        for event in log["events"]:
            events += (event + "<br>")
        events = events[:-4]
        member_events += "<tr><td>{}</td><td>{}</td></tr>".format(log["member"], events)
    log_table = "<table border='1' style='border-collapse: collapse; " \
                "margin-left: 2em'>{}{}</table>".format(table_header, member_events)
    return log_table


def generate_daily_quote():
    return "<p>&ensp;&ensp;Daily quote:<br>&ensp;&ensp;" \
           "{}<br>&ensp;&ensp;{}</p>".format(RESULT["content"], RESULT["translation"])


def generate_email_regards():
    regard = random.choice(CONFIG["email"]["regards"])
    return "&ensp;&ensp;{}".format(regard)


def generate_email_inscriber():
    inscriber = random.choice(CONFIG["email"]["inscriber"])
    return "<p>&ensp;&ensp;{},<br>&ensp;&ensp;{}</p>".format(inscriber, CONFIG["project"]["name"])


def joint_email_content(logs, receiver):
    email_header = generate_email_header()
    email_salutation = generate_email_salutation(receiver["degree"], receiver["sur_name"])
    email_opener = generate_email_opener()
    log_table = generate_log_table(logs)
    daily_quote = generate_daily_quote()
    email_regards = generate_email_regards()
    email_inscriber = generate_email_inscriber()
    email_body = email_salutation + email_opener + log_table + daily_quote + email_regards + email_inscriber
    return email_header, email_body


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
    email_header, email_body = joint_email_content(logs, CONFIG["receivers"][0])
