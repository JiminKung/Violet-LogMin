import yaml
import tkinter as tk
import tkinter.ttk as ttk

from utils.logmin import LOGMIN

with open("violet-logmin.yaml", mode='r', encoding="utf-8") as f:
    CONFIG = yaml.load(f, Loader=yaml.FullLoader)

WIDGET_CONFIG = CONFIG["widget"]
MEMBER_LIST_FRAME_CONFIG = WIDGET_CONFIG["member_list_frame"]
MEMBER_LIST_TREEVIEW_CONFIG = WIDGET_CONFIG["member_list_treeview"]
MEMBER_LIST_VERTICAL_SCROLLBAR_CONFIG = WIDGET_CONFIG["member_list_vertical_scrollbar"]
MEMBER_LIST_HORIZONTAL_SCROLLBAR_CONFIG = WIDGET_CONFIG["member_list_horizontal_scrollbar"]
SEND_EMAIL_BUTTON_CONFIG = WIDGET_CONFIG["send_email_button"]


class MemberListFrame(tk.LabelFrame):
    def __init__(self, master, context_box, language):
        self.context_box = context_box
        self.context_box["member_list_frame"] = self
        self.language = language
        super().__init__(master=master,
                         text=MEMBER_LIST_FRAME_CONFIG[language]["text"],
                         labelanchor=MEMBER_LIST_FRAME_CONFIG["labelanchor"],
                         font=(MEMBER_LIST_FRAME_CONFIG["font_family"],
                               MEMBER_LIST_FRAME_CONFIG["font_size"],
                               MEMBER_LIST_FRAME_CONFIG["font_weight"]))
        self.grid(row=MEMBER_LIST_FRAME_CONFIG["row"],
                  column=MEMBER_LIST_FRAME_CONFIG["column"],
                  sticky=MEMBER_LIST_FRAME_CONFIG["sticky"])

        self.member_list_treeview = None
        self.member_list_vertical_scrollbar = None
        self.member_list_horizontal_scrollbar = None
        self.send_email_button = None

        self.setup()

    def setup(self):
        columns = MEMBER_LIST_TREEVIEW_CONFIG["columns"]
        anchors = MEMBER_LIST_TREEVIEW_CONFIG["anchors"]
        widths = MEMBER_LIST_TREEVIEW_CONFIG["widths"]
        headings = MEMBER_LIST_TREEVIEW_CONFIG[self.language]["headings"]

        self.member_list_treeview = ttk.Treeview(self, columns=columns,
                                                 show=MEMBER_LIST_TREEVIEW_CONFIG["show"],
                                                 selectmode=MEMBER_LIST_TREEVIEW_CONFIG["selectmode"],
                                                 height=MEMBER_LIST_TREEVIEW_CONFIG["height"])

        for column, anchor, width, heading in zip(columns, anchors, widths, headings):
            self.member_list_treeview.column(column=column, width=width, anchor=anchor)
            self.member_list_treeview.heading(column=column, text=heading, anchor=anchor)

        for index, member in enumerate(LOGMIN.members):
            if member["register_state"]:
                register_state = MEMBER_LIST_TREEVIEW_CONFIG[self.language]["register_state"][0]
            else:
                register_state = MEMBER_LIST_TREEVIEW_CONFIG[self.language]["register_state"][1]
            self.member_list_treeview.insert("", index, values=(register_state, member["name"],
                                                                member["grade"], member["address"]))

        self.member_list_treeview.bind("<ButtonRelease-1>", self.select_logs)

        self.member_list_vertical_scrollbar = tk.Scrollbar(self,
                                                           orient=MEMBER_LIST_VERTICAL_SCROLLBAR_CONFIG["orient"],
                                                           command=self.member_list_treeview.yview)
        self.member_list_vertical_scrollbar.pack(side=MEMBER_LIST_VERTICAL_SCROLLBAR_CONFIG["side"],
                                                 fill=MEMBER_LIST_VERTICAL_SCROLLBAR_CONFIG["fill"])

        self.member_list_horizontal_scrollbar = tk.Scrollbar(self,
                                                             orient=MEMBER_LIST_HORIZONTAL_SCROLLBAR_CONFIG["orient"],
                                                             command=self.member_list_treeview.xview)
        self.member_list_horizontal_scrollbar.pack(side=MEMBER_LIST_HORIZONTAL_SCROLLBAR_CONFIG["side"],
                                                   fill=MEMBER_LIST_HORIZONTAL_SCROLLBAR_CONFIG["fill"])

        self.member_list_treeview.config(yscrollcommand=self.member_list_vertical_scrollbar.set,
                                         xscrollcommand=self.member_list_horizontal_scrollbar.set)

        self.member_list_treeview.pack(side=MEMBER_LIST_TREEVIEW_CONFIG["side"],
                                       padx=MEMBER_LIST_TREEVIEW_CONFIG["padx"],
                                       pady=MEMBER_LIST_TREEVIEW_CONFIG["pady"])

        self.send_email_button = tk.Button(self, state="disable",
                                           text=SEND_EMAIL_BUTTON_CONFIG[self.language]["text"],
                                           font=(SEND_EMAIL_BUTTON_CONFIG["font_family"],
                                                 SEND_EMAIL_BUTTON_CONFIG["font_size"],
                                                 SEND_EMAIL_BUTTON_CONFIG["font_weight"]),
                                           command=LOGMIN.send_email)
        self.send_email_button.pack(side=SEND_EMAIL_BUTTON_CONFIG["side"],
                                    pady=SEND_EMAIL_BUTTON_CONFIG["pady"])

    def select_logs(self, event=None):
        if len(self.member_list_treeview.selection()) == 0:
            return
        # It's set to select only one item at once.
        item = self.member_list_treeview.selection()[0]
        selected_member = self.member_list_treeview.item(item, "values")
        events = ""
        for member in LOGMIN.members:
            if member["address"] == selected_member[3]:
                events = member["events"]
                break
        self.context_box["log_frame"].event_text.delete("0.0", "end")
        self.context_box["log_frame"].event_text.insert("0.0", events)
