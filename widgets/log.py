import yaml
import tkinter as tk

from utils.logmin import LOGMIN

with open("violet-logmin.yaml", mode='r', encoding="utf-8") as f:
    CONFIG = yaml.load(f, Loader=yaml.FullLoader)

WIDGET_CONFIG = CONFIG["widget"]
LOG_FRAME_CONFIG = WIDGET_CONFIG["log_frame"]
LOG_TEXT_CONFIG = WIDGET_CONFIG["log_text"]
LOG_BUTTON_FRAME_CONFIG = WIDGET_CONFIG["log_button_frame"]
LOG_SUBMIT_BUTTON_CONFIG = WIDGET_CONFIG["log_submit_button"]
LOG_CLEAR_BUTTON_CONFIG = WIDGET_CONFIG["log_clear_button"]
LOG_VERTICAL_SCROLLBAR_CONFIG = WIDGET_CONFIG["log_vertical_scrollbar"]
LOG_HORIZONTAL_SCROLLBAR_CONFIG = WIDGET_CONFIG["log_horizontal_scrollbar"]
MEMBER_LIST_TREEVIEW_CONFIG = WIDGET_CONFIG["member_list_treeview"]



class LogFrame(tk.LabelFrame):
    def __init__(self, master, context_box, language):
        self.context_box = context_box
        self.context_box["log_frame"] = self
        self.language = language
        super().__init__(master=master,
                         text=LOG_FRAME_CONFIG[language]["text"],
                         labelanchor=LOG_FRAME_CONFIG["labelanchor"],
                         font=(LOG_FRAME_CONFIG["font_family"],
                               LOG_FRAME_CONFIG["font_size"],
                               LOG_FRAME_CONFIG["font_weight"]))
        self.grid(row=LOG_FRAME_CONFIG["row"],
                  column=LOG_FRAME_CONFIG["column"],
                  sticky=LOG_FRAME_CONFIG["sticky"])

        self.log_text = None
        self.log_vertical_scrollbar = None
        self.log_horizontal_scrollbar = None
        self.log_button_frame = None
        self.log_submit_button = None
        self.log_clear_button = None

        self.setup()

    def setup(self):

        self.log_text = tk.Text(self, wrap=LOG_TEXT_CONFIG["wrap"],
                                width=LOG_TEXT_CONFIG["width"],
                                height=LOG_TEXT_CONFIG["height"],
                                font=(LOG_TEXT_CONFIG["font_family"],
                                      LOG_TEXT_CONFIG["font_size"],
                                      LOG_TEXT_CONFIG["font_weight"]))

        self.log_vertical_scrollbar = tk.Scrollbar(self,
                                                   orient=LOG_VERTICAL_SCROLLBAR_CONFIG["orient"],
                                                   command=self.log_text.yview)
        self.log_vertical_scrollbar.pack(side=LOG_VERTICAL_SCROLLBAR_CONFIG["side"],
                                         fill=LOG_VERTICAL_SCROLLBAR_CONFIG["fill"])

        self.log_horizontal_scrollbar = tk.Scrollbar(self,
                                                     orient=LOG_HORIZONTAL_SCROLLBAR_CONFIG["orient"],
                                                     command=self.log_text.xview)
        self.log_horizontal_scrollbar.pack(side=LOG_HORIZONTAL_SCROLLBAR_CONFIG["side"],
                                           fill=LOG_HORIZONTAL_SCROLLBAR_CONFIG["fill"])

        self.log_text.config(yscrollcommand=self.log_vertical_scrollbar.set,
                             xscrollcommand=self.log_horizontal_scrollbar.set)

        self.log_text.pack(side=LOG_TEXT_CONFIG["side"],
                           padx=LOG_TEXT_CONFIG["padx"],
                           pady=LOG_TEXT_CONFIG["pady"])

        self.log_button_frame = tk.Frame(self)
        self.log_button_frame.pack(side=LOG_BUTTON_FRAME_CONFIG["side"])

        self.log_submit_button = tk.Button(self.log_button_frame,
                                           text=LOG_SUBMIT_BUTTON_CONFIG[self.language]["text"],
                                           font=(LOG_SUBMIT_BUTTON_CONFIG["font_family"],
                                                 LOG_SUBMIT_BUTTON_CONFIG["font_size"],
                                                 LOG_SUBMIT_BUTTON_CONFIG["font_weight"]),
                                           command=self.submit_event)
        self.log_submit_button.pack(side=LOG_SUBMIT_BUTTON_CONFIG["side"],
                                    padx=LOG_SUBMIT_BUTTON_CONFIG["padx"],
                                    pady=LOG_SUBMIT_BUTTON_CONFIG["pady"])

        self.log_clear_button = tk.Button(self.log_button_frame,
                                          text=LOG_CLEAR_BUTTON_CONFIG[self.language]["text"],
                                          font=(LOG_CLEAR_BUTTON_CONFIG["font_family"],
                                                LOG_CLEAR_BUTTON_CONFIG["font_size"],
                                                LOG_CLEAR_BUTTON_CONFIG["font_weight"]),
                                          command=self.clear_log_text)
        self.log_clear_button.pack(side=LOG_CLEAR_BUTTON_CONFIG["side"],
                                   padx=LOG_CLEAR_BUTTON_CONFIG["padx"],
                                   pady=LOG_CLEAR_BUTTON_CONFIG["pady"])

    def submit_event(self):
        member_list_treeview = self.context_box["member_list_frame"].member_list_treeview
        if len(member_list_treeview.selection()) == 0:
            self.context_box["proscenium_frame"].throw_miss_selecting_exception()
            return
        selected_item = member_list_treeview.selection()[0]
        selected_member = member_list_treeview.item(selected_item, "values")
        selected_index = member_list_treeview.index(selected_item)
        log = self.log_text.get("0.0", "end")[:-1]
        if log == "" or log.strip() == "":
            self.context_box["proscenium_frame"].throw_empty_input_exception()
            return
        register_state = MEMBER_LIST_TREEVIEW_CONFIG[self.language]["register_state"][0]
        send_permission = True
        for member in LOGMIN.members:
            if member["address"] == selected_member[3]:
                if member["log"] == log:
                    self.context_box["proscenium_frame"].throw_log_unchange_exception()
                    return
                member["register_state"] = True
                member["log"] = log
                member_list_treeview.delete(selected_item)
                member_list_treeview.insert("", selected_index, values=(register_state, member["name"],
                                                                        member["grade"], member["address"]))
            if not member["register_state"]:
                send_permission = False

        if send_permission:
            self.context_box["member_list_frame"].send_email_button.config(state="normal")
            self.context_box["proscenium_frame"].display_send_permission()

    def clear_log_text(self):
        self.log_text.delete("0.0", "end")
