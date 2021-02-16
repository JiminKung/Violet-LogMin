import yaml
import requests
import datetime
import random

with open("violet-logmin.yaml", mode='r', encoding="utf-8") as f:
    CONFIG = yaml.load(f, Loader=yaml.FullLoader)

DAILY_QUOTE = requests.get(CONFIG["shanbay"]["url"]).json()


def generate_email_header():
    today = datetime.date.today()
    return "Logs of {} {}".format(CONFIG["group"]["name"], today)


def generate_email_salutation(degree, sur_name):
    return "<p>&ensp;&ensp;Dear {} {}</p>".format(degree, sur_name)


def generate_email_opener():
    url = CONFIG["project"]["github"]
    opener = random.choice(CONFIG["email"]["opener"])
    return "<p>&ensp;&ensp;This is <a href='{}'>LogMin</a>, an auto-mail logs robot. {}</p>".format(url, opener)


def generate_log_table(members):
    table_header = "<tr><th>{}</th><th>{}</th></tr>".format("Name", "Log")
    member_log = ""
    for member in members:
        # events = ""
        # for event in log["events"]:
        #     events += (event + "<br>")
        # events = events[:-4]
        log = member["log"].replace("\n", "<br>")
        member_log += "<tr><td>{}</td><td>{}</td></tr>".format(member["name"], log)
    log_table = "<table border='1' style='border-collapse: collapse; " \
                "margin-left: 2em'>{}{}</table>".format(table_header, member_log)
    return log_table


def generate_daily_quote():
    return "<p>&ensp;&ensp;Daily quote:<br>&ensp;&ensp;" \
           "{}<br>&ensp;&ensp;{}</p>".format(DAILY_QUOTE["content"], DAILY_QUOTE["translation"])


def generate_email_regards():
    regard = random.choice(CONFIG["email"]["regards"])
    return "&ensp;&ensp;{}".format(regard)


def generate_email_inscriber():
    inscriber = random.choice(CONFIG["email"]["inscriber"])
    return "<p>&ensp;&ensp;{},<br>&ensp;&ensp;{}</p>".format(inscriber, CONFIG["email"]["sender_name"])


def joint_email_content(members, receiver):
    email_header = generate_email_header()
    email_salutation = generate_email_salutation(receiver["degree"], receiver["sur_name"])
    email_opener = generate_email_opener()
    log_table = generate_log_table(members)
    daily_quote = generate_daily_quote()
    email_regards = generate_email_regards()
    email_inscriber = generate_email_inscriber()
    email_body = email_salutation + email_opener + log_table + daily_quote + email_regards + email_inscriber
    return email_header, email_body

