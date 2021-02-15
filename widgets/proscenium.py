import yaml
import tkinter as tk

with open("violet-logmin.yaml", mode='r', encoding="utf-8") as f:
    CONFIG = yaml.load(f, Loader=yaml.FullLoader)

WIDGET_CONFIG = CONFIG["widget"]
PROSCENIUM_FRAME_CONFIG = WIDGET_CONFIG["proscenium_frame"]
PROSCENIUM_TEXT_CONFIG = WIDGET_CONFIG["proscenium_text"]
PROSCENIUM_SCROLLBAR_CONFIG = WIDGET_CONFIG["proscenium_scrollbar"]

DIALOGUE_CONFIG = CONFIG["dialogue"]
LOGMIN_DIALOGUE_CONFIG = DIALOGUE_CONFIG["LogMin"]
VIOLET_DIALOGUE_CONFIG = DIALOGUE_CONFIG["Violet"]
VIOLET_LOGMIN_DIALOGUE_CONFIG = DIALOGUE_CONFIG["Violet-LogMin"]


class ProsceniumFrame(tk.LabelFrame):
    def __init__(self, master, context_box, language):
        self.context_box = context_box
        self.context_box["proscenium_frame"] = self
        self.language = language
        super().__init__(master=master,
                         text=PROSCENIUM_FRAME_CONFIG[language]["text"],
                         labelanchor=PROSCENIUM_FRAME_CONFIG["labelanchor"],
                         font=(PROSCENIUM_FRAME_CONFIG["font_family"],
                               PROSCENIUM_FRAME_CONFIG["font_size"],
                               PROSCENIUM_FRAME_CONFIG["font_weight"]))
        self.pack(side=PROSCENIUM_FRAME_CONFIG["side"],
                  padx=PROSCENIUM_FRAME_CONFIG["padx"],
                  pady=PROSCENIUM_FRAME_CONFIG["pady"],
                  fill="x")

        self.proscenium_text = None
        self.proscenium_scrollbar = None

        self.setup()

    def setup(self):
        self.proscenium_text = tk.Text(self, wrap=PROSCENIUM_TEXT_CONFIG["wrap"],
                                       font=(PROSCENIUM_TEXT_CONFIG["font_family"],
                                       PROSCENIUM_TEXT_CONFIG["font_size"],
                                       PROSCENIUM_TEXT_CONFIG["font_weight"]))
        self.proscenium_scrollbar = tk.Scrollbar(self, orient=PROSCENIUM_SCROLLBAR_CONFIG["orient"])
        self.proscenium_scrollbar.config(command=self.proscenium_text.yview)
        self.proscenium_text.config(yscrollcommand=self.proscenium_scrollbar.set)
        self.proscenium_scrollbar.pack(side=PROSCENIUM_SCROLLBAR_CONFIG["side"],
                                       fill=PROSCENIUM_SCROLLBAR_CONFIG["fill"])
        self.proscenium_text.pack(padx=PROSCENIUM_TEXT_CONFIG["padx"],
                                  pady=PROSCENIUM_TEXT_CONFIG["pady"],
                                  fill=PROSCENIUM_TEXT_CONFIG["fill"])

        self.proscenium_text.see("end")
        self.perform_opening_act()
        self.list_cast()

    def perform_opening_act(self):
        welcome_lines = VIOLET_LOGMIN_DIALOGUE_CONFIG["role"] + \
                        VIOLET_LOGMIN_DIALOGUE_CONFIG[self.language]["welcome"] + "\n\n"
        introduction_lines = VIOLET_LOGMIN_DIALOGUE_CONFIG["role"] + \
                             VIOLET_LOGMIN_DIALOGUE_CONFIG[self.language]["introduction"] + "\n\n"
        website_lines = VIOLET_LOGMIN_DIALOGUE_CONFIG["role"] + \
                        VIOLET_LOGMIN_DIALOGUE_CONFIG[self.language]["website"] + "\n\n"
        self.proscenium_text.insert("end", welcome_lines)
        self.proscenium_text.insert("end", introduction_lines)
        self.proscenium_text.insert("end", website_lines)
        self.proscenium_text.config(state="disabled")

    def list_cast(self):
        self.proscenium_text.config(state="normal")
        violet_introduction_lines = VIOLET_DIALOGUE_CONFIG["role"] + \
                                    VIOLET_DIALOGUE_CONFIG[self.language]["introduction"] + "\n\n"
        logmin_introduction_lines = LOGMIN_DIALOGUE_CONFIG["role"] + \
                                    LOGMIN_DIALOGUE_CONFIG[self.language]["introduction"] + "\n\n"
        tutorial_lines = VIOLET_LOGMIN_DIALOGUE_CONFIG["role"] + \
                         VIOLET_LOGMIN_DIALOGUE_CONFIG[self.language]["tutorial"] + "\n\n"
        self.proscenium_text.insert("end", violet_introduction_lines)
        self.proscenium_text.insert("end", logmin_introduction_lines)
        self.proscenium_text.insert("end", tutorial_lines)
        self.proscenium_text.config(state="disabled")
        # self.proscenium_text.see("end")

    def throw_miss_selecting_exception(self):
        self.proscenium_text.config(state="normal")
        violet_miss_selecting_lines = VIOLET_DIALOGUE_CONFIG["role"] + \
                                      VIOLET_DIALOGUE_CONFIG[self.language]["miss_selecting"] + "\n\n"
        self.proscenium_text.insert("end", violet_miss_selecting_lines)
        self.proscenium_text.config(state="disabled")
        self.proscenium_text.see("end")

    def throw_empty_input_exception(self):
        self.proscenium_text.config(state="normal")
        violet_empty_input_lines = VIOLET_DIALOGUE_CONFIG["role"] + \
                                      VIOLET_DIALOGUE_CONFIG[self.language]["empty_input"] + "\n\n"
        self.proscenium_text.insert("end", violet_empty_input_lines)
        self.proscenium_text.config(state="disabled")
        self.proscenium_text.see("end")

    def throw_log_unchange_exception(self):
        pass

    def display_selected_member(self, member):
        pass

    def display_send_permission(self, send_permission):
        pass

    def display_submitted_log(self, log):
        pass

    def display_sent_logs(self, logs):
        pass

    def display_send_instruction(self):
        pass

    def display_send_state(self):
        pass
