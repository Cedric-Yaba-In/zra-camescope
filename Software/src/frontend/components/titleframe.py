import tkinter as ttk

from colors import BACKGROUND_COLOR, BACKGROUND_COLOR_1, BORDER_COLOR, TEXT_COLOR

class TitleFrame(ttk.Frame):
    def __init__(self, master, text:str, width:int, height:int, font_size:int = 13, text_color:str=TEXT_COLOR, background:str=BACKGROUND_COLOR_1, border_color:str =BORDER_COLOR):
        ttk.Frame.__init__(
            self, master, width=width, 
            height=height, background=background, 
            bd = 1, highlightthickness=1, 
            highlightbackground=border_color, highlightcolor=border_color
        )
        self.pack_propagate(0)
        ttk.Label(self, text = text, foreground=text_color, background= background, font=("Segeo UI", font_size)).pack()
