import yaml


# with open("violet-logmin.yaml", mode='r', encoding="utf-8") as f:
#     CONFIG = yaml.load(f, Loader=yaml.FullLoader)
#
#
# def adjust_logs(logs, receiver):
#     """Put the receiver at the head of log list."""
#     current_full_name = receiver["sur_name"] + receiver["given_name"]
#     current_log = None
#     for i, log in enumerate(logs):
#         if log["member"] == current_full_name:
#             current_log = logs.pop(i)
#             break
#     if current_log is None:
#         return
#     logs.insert(0, current_log)

