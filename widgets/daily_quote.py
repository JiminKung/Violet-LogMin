import yaml
import datetime
import tkinter as tk

from utils.utils import format_date
from utils.generate_email_content import DAILY_QUOTE

with open("violet-logmin.yaml", mode='r', encoding="utf-8") as f:
    WIDGET_CONFIG = yaml.load(f, Loader=yaml.FullLoader)["widget"]

DAILY_QUOTE_FRAME_CONFIG = WIDGET_CONFIG["daily_quote_frame"]
TODAY_LABEL_CONFIG = WIDGET_CONFIG["today_label"]
QUOTE_LABEL_CONFIG = WIDGET_CONFIG["quote_label"]


class DailyQuoteFrame(tk.LabelFrame):
    def __init__(self, master, context_box, language):
        self.context_box = context_box
        self.context_box["daily_quote_frame"] = self
        self.language = language
        self.daily_quote = DAILY_QUOTE
        super().__init__(master=master,
                         text=DAILY_QUOTE_FRAME_CONFIG[language]["text"],
                         labelanchor=DAILY_QUOTE_FRAME_CONFIG["labelanchor"],
                         font=(DAILY_QUOTE_FRAME_CONFIG["font_family"],
                               DAILY_QUOTE_FRAME_CONFIG["font_size"],
                               DAILY_QUOTE_FRAME_CONFIG["font_weight"]))
        self.grid(row=DAILY_QUOTE_FRAME_CONFIG["row"],
                  column=DAILY_QUOTE_FRAME_CONFIG["column"],
                  sticky=DAILY_QUOTE_FRAME_CONFIG["sticky"])

        self.today = None
        self.today_label = None
        self.quote_label = None

        self.setup()

    def setup(self):
        self.today = datetime.datetime.today()
        self.today_label = tk.Label(self, text="\n" + format_date(self.today),
                                    font=(TODAY_LABEL_CONFIG["font_family"],
                                          TODAY_LABEL_CONFIG["font_size"],
                                          TODAY_LABEL_CONFIG["font_weight"],
                                          TODAY_LABEL_CONFIG["underline"]))
        self.today_label.pack()

        if self.language == "Chinese":
            quote = self.daily_quote["content"] + "\n\n" + self.daily_quote["translation"]
        else:
            quote = self.daily_quote["content"]

        self.quote_label = tk.Label(self, text=quote,
                                    justify=QUOTE_LABEL_CONFIG["justify"],
                                    wraplength=QUOTE_LABEL_CONFIG["wraplength"])
        self.quote_label.config(font=(QUOTE_LABEL_CONFIG["font_family"],
                                      QUOTE_LABEL_CONFIG["font_size"],
                                      QUOTE_LABEL_CONFIG["font_weight"]))
        self.quote_label.pack(padx=QUOTE_LABEL_CONFIG["padx"],
                              pady=QUOTE_LABEL_CONFIG["pady"])
