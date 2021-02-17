import yaml
import tkinter as tk

from utils.utils import centered_display
from widgets.violet import Voilet

with open("violet-logmin.yaml", mode='r', encoding="utf-8") as f:
    WIDGET_CONFIG = yaml.load(f, Loader=yaml.FullLoader)["widget"]

BOOT_PAGE_CONFIG = WIDGET_CONFIG["boot_page"]
WELCOME_LABEL_FRAME_CONFIG = WIDGET_CONFIG["welcome_label_frame"]
WELCOME_LABEL_CONFIG = WIDGET_CONFIG["welcome_label"]
CHOICE_FRAME_CONFIG = WIDGET_CONFIG["choice_frame"]
ENGLISH_BUTTON_CONFIG = WIDGET_CONFIG["english_button"]
CHINESE_BUTTON_CONFIG = WIDGET_CONFIG["chinese_button"]

class BootPage(tk.Tk):
    def __init__(self):
        super().__init__()

        self.language = ""
        self.context_box = {"boot_page": self}
        self.title(BOOT_PAGE_CONFIG["title"])
        self.iconbitmap(default=BOOT_PAGE_CONFIG["icon"])
        self.window_width = BOOT_PAGE_CONFIG["window_width"]
        self.window_height = BOOT_PAGE_CONFIG["window_height"]
        if not BOOT_PAGE_CONFIG["resizeable"]:
            self.resizable(0, 0)

        self.welcome_label_frame = None
        self.welcome_label = None
        self.choice_frame = None
        self.english_button = None
        self.chinese_button = None

        self.setup()
        centered_display(self)

    def setup(self):
        self.welcome_label_frame = tk.LabelFrame(self, text=WELCOME_LABEL_FRAME_CONFIG["text"],
                                                 labelanchor=WELCOME_LABEL_FRAME_CONFIG["labelanchor"],
                                                 font=(WELCOME_LABEL_FRAME_CONFIG["font_family"],
                                                       WELCOME_LABEL_FRAME_CONFIG["font_size"],
                                                       WELCOME_LABEL_FRAME_CONFIG["font_weight"]))
        self.welcome_label_frame.pack(pady=WELCOME_LABEL_FRAME_CONFIG["pady"])

        self.welcome_label = tk.Label(self.welcome_label_frame, text=WELCOME_LABEL_CONFIG["text"],
                                      wraplength=WELCOME_LABEL_CONFIG["wraplength"],
                                      justify=WELCOME_LABEL_CONFIG["justify"],
                                      font=(WELCOME_LABEL_CONFIG["font_family"],
                                            WELCOME_LABEL_CONFIG["font_size"],
                                            WELCOME_LABEL_CONFIG["font_weight"]))
        self.welcome_label.pack(side=WELCOME_LABEL_CONFIG["side"],
                                padx=WELCOME_LABEL_CONFIG["padx"],
                                pady=WELCOME_LABEL_CONFIG["pady"])

        self.choice_frame = tk.Frame(self)
        self.choice_frame.pack(padx=CHOICE_FRAME_CONFIG["padx"],
                               pady=CHOICE_FRAME_CONFIG["pady"])

        self.english_button = tk.Button(self.choice_frame, text=ENGLISH_BUTTON_CONFIG["text"],
                                        font=(ENGLISH_BUTTON_CONFIG["font_family"],
                                              ENGLISH_BUTTON_CONFIG["font_size"],
                                              ENGLISH_BUTTON_CONFIG["font_weight"]),
                                        command=self.choose_english)
        self.english_button.pack(side=ENGLISH_BUTTON_CONFIG["side"],
                                 padx=ENGLISH_BUTTON_CONFIG["padx"])

        self.chinese_button = tk.Button(self.choice_frame, text=CHINESE_BUTTON_CONFIG["text"],
                                        font=(CHINESE_BUTTON_CONFIG["font_family"],
                                              CHINESE_BUTTON_CONFIG["font_size"],
                                              CHINESE_BUTTON_CONFIG["font_weight"]),
                                        command=self.choose_chinese)
        self.chinese_button.pack(side=CHINESE_BUTTON_CONFIG["side"],
                                 padx=CHINESE_BUTTON_CONFIG["padx"])

    def choose_english(self):
        self.language = "English"
        self.boot_violet()

    def choose_chinese(self):
        self.language = "Chinese"
        self.boot_violet()

    def boot_violet(self):
        violet = Voilet(self.context_box, self.language)
        self.withdraw()
        violet.mainloop()

    def exit(self):
        self.destroy()