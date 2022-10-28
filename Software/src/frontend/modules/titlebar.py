import os
import tkinter as ttk
from typing import Callable, Dict, Union

from PIL import Image, ImageTk

from colors import TEXT_COLOR
from constants import PATH_TO_IMAGE
from custombutton import CustomButton
from menubar import MenuBar

class TitleBar(ttk.Frame):
    def __init__(self, master:object, width:int, height:int, background:str, menu_items:Dict[str, Union[str, Dict[str, str]]], functions={}, close:Callable = None, iconify:Callable = None, maximize:Callable = None, minimize:Callable = None):
        ttk.Frame.__init__(self, master = master, width=width, height=height, background=background)

        ttk.Label(
            self, text="CACHO", 
            foreground=TEXT_COLOR, font=("Segeo UI", 17, "bold"), 
            background=background, justify="left"
        ).pack(side="left", padx=5)
        
        self.is_maximized = False
        

        menu = MenuBar(self, width = width, height=height, menu_items= menu_items, background=background, functions=functions)
        # menu.pack_propagate(False)
        menu.pack(side='left')
        
        self.title = ttk.Label(self, text="New project", justify='center', foreground=TEXT_COLOR, background=background, font=("Segeo UI", 10))
        self.title.pack(side="left", padx=50 + 180 - 10*3)

        window_action_frame = ttk.Frame(self, width = 90, height=height, background=background)
        window_action_frame.pack(side="right", padx=0)
        # window_action_frame.pack_propagate(0)
        
        # join = os.path.join
        # CustomButton(window_action_frame, join(PATH_TO_IMAGE, "iconify.png"), join(PATH_TO_IMAGE, "iconify_n.png"), command=iconify, background=background, width=None, height=None).pack(side="left")
        # button = CustomButton(window_action_frame, join(PATH_TO_IMAGE, "maximize.png"), join(PATH_TO_IMAGE, "maximize_n.png"), command=maximize, background=background, width=None, height=None).pack(side="left")
        # CustomButton(window_action_frame, join(PATH_TO_IMAGE, "close.png"), join(PATH_TO_IMAGE, "close_n.png"), command=close, background=background, width=None, height=None).pack(side="left")

    def set_menu(self, menu:MenuBar):
        menu.grid(row=0, column=1, sticky="W")

    def set_title(self, title:str):
        n = len(title)
        new_title = title
        if n > 50:
            new_title = title[:47] + "..."
        self.title.configure(text=" "*20)
        self.title.configure(text = new_title)
        self.title.pack(padx=50 + (180 - 10*n))