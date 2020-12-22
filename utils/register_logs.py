import yaml


with open("LogMin.yaml", mode='r', encoding="utf-8") as f:
    CONFIG = yaml.load(f, Loader=yaml.FullLoader)


def adjust_logs(logs, receiver):
    current_full_name = receiver["sur_name"] + receiver["given_name"]
    current_log = None
    for i, log in enumerate(logs):
        if log["member"] == current_full_name:
            current_log = logs.pop(i)
            break
    if current_log is None:
        return
    logs.insert(0, current_log)


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
    receiver = CONFIG["receivers"][0]
    adjust_logs(logs, receiver)