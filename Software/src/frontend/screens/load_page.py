import sys
import os
import threading
import time
import tkinter as ttk
from typing import List, Union

sys.path.append(os.path.join(".", "configs"))
sys.path.append(os.path.join(".", "constants"))

from colors import BACKGROUND_COLOR, LOAD_TEXT_COLOR, LOADING_RECT_FIRST_COLOR, LOADING_RECT_OUTLINE_COLOR, LOADING_RECT_SECOND_COLOR, TEXT_COLOR
from font import LOAD_TEXT_FONT, LOGO_FONT
from text import APP_NAME
from constants import LOAD_WAITING_TIME_INTERVAL

class LoadPage(ttk.Canvas):
    def __init__(self, root:ttk.Tk, width = 500, height = 300) -> None:
        x_pos = (root.winfo_screenwidth() - width) // 2
        y_pos = (root.winfo_screenheight() - height - 100) //2  
        root.geometry(f"{width}x{height}+{x_pos}+{y_pos}")
        root.resizable(width=False, height=False)

        ttk.Canvas.__init__(self, master=root, background=BACKGROUND_COLOR, width=width, height=height)
        self.pack()
        logo = ttk.Label(self, fg = TEXT_COLOR, background=BACKGROUND_COLOR, text=APP_NAME, font= LOGO_FONT)
        logo.place(x = 125, y = 100)
        self.width = width
    
    def start_loading(self, callback=None):
        self.loading_text = ttk.Label(self, fg = LOAD_TEXT_COLOR, background=BACKGROUND_COLOR, text="", font=LOAD_TEXT_FONT)
        self.loading_text.place(x = 50, y = 250)
        item_ids = self.build_display_loader(8, (self.width - (8 * 4 + 30 * 3))//2, 200, 30)
        self.is_loading = True
        self.callback = callback
        thread1 = threading.Thread(target = self.load, args = ([item_ids]))
        thread2 = threading.Thread(target = self.loading_data)
        
        thread1.daemon = True
        thread2.daemon = True
        
        thread1.start()
        thread2.start()


    def loading_data(self):
        """Load data here and display loading mesages"""
        messages  = [
            "load configurations files",
            "load application variables",
            "setting interface",
            "load assets\images",
            "load assets\data", 
            "a", 
            "b", 
            "c"
        ]
        messages.extend([i for i in "abcdefghijklmnopqrstuvwxyz0123456789" ])
        for message in messages:
            self.loading_text.config(text = " "*50)
            self.loading_text.config(text = message)
            time.sleep(.1)
        self.is_loading = False

    def load(self, item_ids):
        counter = 0
        while self.is_loading:
            self.itemconfig(item_ids[counter], fill=LOADING_RECT_SECOND_COLOR)
            time.sleep(LOAD_WAITING_TIME_INTERVAL) 
            counter = counter + 1
            if counter == len(item_ids):
                counter = 0
                for id in item_ids:
                    self.itemconfig(id, fill = LOADING_RECT_FIRST_COLOR)
                time.sleep(LOAD_WAITING_TIME_INTERVAL) 
        
        if self.callback != None:
            self.callback()

    def build_display_loader(self, side:int, default_x:int, default_y:int, interval:int):
        squares: List[Union[str, int]] = []
        width = height = side
        x = default_x
        y = default_y
        y1 = y + height
        for i in range(4):
            x1 = x + width
            squares.append(self.create_rectangle(x, y, x1, y1, fill=LOADING_RECT_FIRST_COLOR, outline=LOADING_RECT_OUTLINE_COLOR))
            x += width + interval
        return squares
