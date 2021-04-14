import yaml
import requests
import datetime
import random

with open("violet-logmin.yaml", mode='r', encoding="utf-8") as f:
    CONFIG = yaml.load(f, Loader=yaml.FullLoader)

DAILY_QUOTE = requests.get(CONFIG["shanbay"]["url"]).json()


def generate_email_header(language):
    today = datetime.date.today()
    if language == "Chinese":
        header = "{}日志 {}".format(CONFIG["group"]["name"], today)
    elif language == "English":
        header = "Logs of {} {}".format(CONFIG["group"]["name"], today)
    else:
        raise Exception("No such language: {}".format(language))
    
    return header


def generate_email_salutation(degree, sur_name, language):
    if language == "Chinese":
        if degree == "Prof." or degree == "Dr.":
            salutation = "<p>&ensp;&ensp;尊敬的 {} {}</p>".format(degree, sur_name)
        else:
            salutation = "<p>&ensp;&ensp;亲爱的 {} {}</p>".format(degree, sur_name)
    elif language == "English":
        salutation = "<p>&ensp;&ensp;Dear {} {}</p>".format(degree, sur_name)
    else:
        raise Exception("No such language: {}".format(language))
    
    return salutation


def generate_email_opener(language):
    url = CONFIG["project"]["github"]
    opener = random.choice(CONFIG["email"][language]["opener"])
    if language == "Chinese":
        return "<p>&ensp;&ensp;这里是 <a href='{}'>LogMin</a>，一个日志自动分发系统。 {}</p>".format(url, opener)
    elif language == "English":
        return "<p>&ensp;&ensp;This is <a href='{}'>LogMin</a>, an auto-mail logs robot. {}</p>".format(url, opener)
    else:
        raise Exception("No such language: {}".format(language))


def generate_log_table(members, language):
    if language == "Chinese":
        table_header = "<tr><th>{}</th><th>{}</th></tr>".format("姓名", "日志")
    elif language == "English":
        table_header = "<tr><th>{}</th><th>{}</th></tr>".format("Name", "Log")
    else: 
        raise Exception("No such language: {}".format(language))
    member_log = ""
    for member in members:
        # events = ""
        # for event in log["events"]:
        #     events += (event + "<br>")
        # events = events[:-4]
        log = member["log"].replace("\n\n", "\n")
        log = log.replace("\n", "<br>")
        member_log += "<tr><td>{}</td><td>{}</td></tr>".format(member["name"], log)
    log_table = "<table border='1' style='border-collapse: collapse; " \
                "margin-left: 2em'>{}{}</table>".format(table_header, member_log)
    return log_table


def generate_daily_quote(language):
    if language == "Chinese":
        return "<p>&ensp;&ensp;每日一句：<br>&ensp;&ensp;" \
           "{}<br>&ensp;&ensp;{}</p>".format(DAILY_QUOTE["content"], DAILY_QUOTE["translation"])
    elif language == "English":
        return "<p>&ensp;&ensp;Daily quote:<br>&ensp;&ensp;" \
           "{}<br>&ensp;&ensp;{}</p>".format(DAILY_QUOTE["content"], DAILY_QUOTE["translation"])
    else:
        raise Exception("No such language: {}".format(language))


def generate_email_regards(language):
    regard = random.choice(CONFIG["email"][language]["regards"])
    return "&ensp;&ensp;{}".format(regard)


def generate_email_inscriber(degree, language):
    if language == "Chinese":
        if degree == "Prof." or degree == "Dr.":
            inscriber = random.choice(CONFIG["email"][language]["inscriber"][:2])
        else:
            inscriber = random.choice(CONFIG["email"][language]["inscriber"][2:])
        return "<p>&ensp;&ensp;{}<br>&ensp;&ensp;{}</p>".format(CONFIG["email"]["sender_name"], inscriber)
    elif language == "English":
        inscriber = random.choice(CONFIG["email"][language]["inscriber"])
        return "<p>&ensp;&ensp;{},<br>&ensp;&ensp;{}</p>".format(inscriber, CONFIG["email"]["sender_name"])
    else:
        raise Exception("No such language: {}".format(language))


def joint_email_content(members, receiver, language):
    email_header = generate_email_header(language)
    email_salutation = generate_email_salutation(receiver["degree"], receiver["sur_name"], language)
    email_opener = generate_email_opener(language)
    log_table = generate_log_table(members, language)
    daily_quote = generate_daily_quote(language)
    email_regards = generate_email_regards(language)
    email_inscriber = generate_email_inscriber(receiver["degree"], language)
    email_body = email_salutation + email_opener + log_table + daily_quote + email_regards + email_inscriber
    return email_header, email_body

