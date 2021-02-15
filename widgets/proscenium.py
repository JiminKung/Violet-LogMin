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

        for _ in range(1):
            self.proscenium_text.insert("insert", VIOLET_LOGMIN_DIALOGUE_CONFIG[self.language]["welcome"] + "\n")
        self.proscenium_text.config(state=tk.DISABLED)
