import yaml
import tkinter as tk

from widgets.utils import centered_display
from widgets.proscenium import ProsceniumFrame

from widgets.log import LogFrame
from widgets.daily_quote import DailyQuoteFrame
from widgets.member_list import MemberListFrame


with open("violet-logmin.yaml", mode='r', encoding="utf-8") as f:
    WIDGET_CONFIG = yaml.load(f, Loader=yaml.FullLoader)["widget"]

VIOLET_CONFIG = WIDGET_CONFIG["violet"]
THEATER_WINDOW_CONFIG = WIDGET_CONFIG["theater_window"]
CLAPBOARD_WINDOW_CONFIG = WIDGET_CONFIG["clapboard_window"]


class Voilet(tk.Toplevel):
    def __init__(self, context_box, language):
        super().__init__()

        self.context_box = context_box
        self.context_box["violet"] = self
        self.language = language
        self.title(VIOLET_CONFIG[language]["title"])
        self.iconbitmap(default=VIOLET_CONFIG["icon"])
        self.window_width = VIOLET_CONFIG["window_width"]
        self.window_height = VIOLET_CONFIG["window_height"]
        if not VIOLET_CONFIG["resizeable"]:
            self.resizable(0, 0)

        self.theater_window = None
        self.clapboard_window = None
        self.daily_quote_frame = None
        self.member_list_frame = None
        self.log_frame = None
        self.proscenium_frame = None

        self.setup()
        centered_display(self)

    def setup(self):
        self.protocol("WM_DELETE_WINDOW", self.exit)

        self.theater_window = tk.PanedWindow(self, orient=THEATER_WINDOW_CONFIG["orient"],
                                             showhandle=THEATER_WINDOW_CONFIG["showhandle"],
                                             sashrelief=THEATER_WINDOW_CONFIG["sashrelief"])
        self.theater_window.pack()

        self.clapboard_window = tk.PanedWindow(self.theater_window,
                                               orient=CLAPBOARD_WINDOW_CONFIG["orient"],
                                               showhandle=CLAPBOARD_WINDOW_CONFIG["showhandle"],
                                               sashrelief=CLAPBOARD_WINDOW_CONFIG["sashrelief"])
        self.clapboard_window.pack()
        self.daily_quote_frame = DailyQuoteFrame(self.clapboard_window, self.context_box, self.language)
        self.member_list_frame = MemberListFrame(self.clapboard_window, self.context_box, self.language)
        self.log_frame = LogFrame(self.clapboard_window, self.context_box, self.language)
        self.clapboard_window.add(self.daily_quote_frame)
        self.clapboard_window.add(self.member_list_frame)
        self.clapboard_window.add(self.log_frame)

        self.proscenium_frame = ProsceniumFrame(self.theater_window, self.context_box, self.language)

        self.theater_window.add(self.clapboard_window)
        self.theater_window.add(self.proscenium_frame)

    def exit(self):
        self.context_box["boot_page"].exit()
