import yaml
import tkinter as tk

from utils.logmin import LOGMIN

with open("violet-logmin.yaml", mode='r', encoding="utf-8") as f:
    CONFIG = yaml.load(f, Loader=yaml.FullLoader)

WIDGET_CONFIG = CONFIG["widget"]
LOG_FRAME_CONFIG = WIDGET_CONFIG["log_frame"]
EVENT_TEXT_CONFIG = WIDGET_CONFIG["event_text"]
EVENT_BUTTON_FRAME_CONFIG = WIDGET_CONFIG["event_button_frame"]
EVENT_SUBMIT_BUTTON_CONFIG = WIDGET_CONFIG["event_submit_button"]
EVENT_CLEAR_BUTTON_CONFIG = WIDGET_CONFIG["event_clear_button"]
EVENT_VERTICAL_SCROLLBAR_CONFIG = WIDGET_CONFIG["event_vertical_scrollbar"]
EVENT_HORIZONTAL_SCROLLBAR_CONFIG = WIDGET_CONFIG["event_horizontal_scrollbar"]
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

        self.event_text = None
        self.event_vertical_scrollbar = None
        self.event_horizontal_scrollbar = None
        self.event_button_frame = None
        self.event_submit_button = None
        self.event_clear_button = None

        self.setup()

    def setup(self):

        self.event_text = tk.Text(self, wrap=EVENT_TEXT_CONFIG["wrap"],
                                  width=EVENT_TEXT_CONFIG["width"],
                                  height=EVENT_TEXT_CONFIG["height"],
                                  font=(EVENT_TEXT_CONFIG["font_family"],
                                        EVENT_TEXT_CONFIG["font_size"],
                                        EVENT_TEXT_CONFIG["font_weight"]))

        self.event_vertical_scrollbar = tk.Scrollbar(self,
                                                     orient=EVENT_VERTICAL_SCROLLBAR_CONFIG["orient"],
                                                     command=self.event_text.yview)
        self.event_vertical_scrollbar.pack(side=EVENT_VERTICAL_SCROLLBAR_CONFIG["side"],
                                           fill=EVENT_VERTICAL_SCROLLBAR_CONFIG["fill"])

        self.event_horizontal_scrollbar = tk.Scrollbar(self,
                                                       orient=EVENT_HORIZONTAL_SCROLLBAR_CONFIG["orient"],
                                                       command=self.event_text.xview)
        self.event_horizontal_scrollbar.pack(side=EVENT_HORIZONTAL_SCROLLBAR_CONFIG["side"],
                                             fill=EVENT_HORIZONTAL_SCROLLBAR_CONFIG["fill"])

        self.event_text.config(yscrollcommand=self.event_vertical_scrollbar.set,
                               xscrollcommand=self.event_horizontal_scrollbar.set)

        # self.log_content_frame.pack(side=LOG_CONTENT_FRAME_CONFIG["side"])
        self.event_text.pack(side=EVENT_TEXT_CONFIG["side"],
                             padx=EVENT_TEXT_CONFIG["padx"],
                             pady=EVENT_TEXT_CONFIG["pady"])

        self.event_button_frame = tk.Frame(self)
        self.event_button_frame.pack(side=EVENT_BUTTON_FRAME_CONFIG["side"])

        self.event_submit_button = tk.Button(self.event_button_frame,
                                             text=EVENT_SUBMIT_BUTTON_CONFIG[self.language]["text"],
                                             font=(EVENT_SUBMIT_BUTTON_CONFIG["font_family"],
                                                   EVENT_SUBMIT_BUTTON_CONFIG["font_size"],
                                                   EVENT_SUBMIT_BUTTON_CONFIG["font_weight"]),
                                             command=self.submit_event)
        self.event_submit_button.pack(side=EVENT_SUBMIT_BUTTON_CONFIG["side"],
                                      padx=EVENT_SUBMIT_BUTTON_CONFIG["padx"],
                                      pady=EVENT_SUBMIT_BUTTON_CONFIG["pady"])

        self.event_clear_button = tk.Button(self.event_button_frame,
                                            text=EVENT_CLEAR_BUTTON_CONFIG[self.language]["text"],
                                            font=(EVENT_CLEAR_BUTTON_CONFIG["font_family"],
                                                  EVENT_CLEAR_BUTTON_CONFIG["font_size"],
                                                  EVENT_CLEAR_BUTTON_CONFIG["font_weight"]),
                                            command=self.clear_event_text)
        self.event_clear_button.pack(side=EVENT_CLEAR_BUTTON_CONFIG["side"],
                                     padx=EVENT_CLEAR_BUTTON_CONFIG["padx"],
                                     pady=EVENT_CLEAR_BUTTON_CONFIG["pady"])

    def submit_event(self):
        events = self.event_text.get("0.0", "end")
        events = events.replace("\n\n", "\n")
        member_list_treeview = self.context_box["member_list_frame"].member_list_treeview
        if len(member_list_treeview.selection()) == 0:
            return
        selected_item = member_list_treeview.selection()[0]
        selected_member = member_list_treeview.item(selected_item, "values")
        selected_index = member_list_treeview.index(selected_item)
        member_list_treeview.delete(selected_item)
        register_state = MEMBER_LIST_TREEVIEW_CONFIG[self.language]["register_state"][0]
        send_state = True
        for member in LOGMIN.members:
            if member["address"] == selected_member[3]:
                member["register_state"] = True
                member["events"] = events
                member_list_treeview.insert("", selected_index, values=(register_state, member["name"],
                                                                        member["grade"], member["address"]))
            if not member["register_state"]:
                send_state = False

        if send_state:
            self.context_box["member_list_frame"].send_email_button.config(state="normal")

    def clear_event_text(self):
        self.event_text.delete("0.0", "end")
