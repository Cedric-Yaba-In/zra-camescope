import tkinter as ttk

from colors import BORDER_COLOR, GRADUATE_BAR_COLOR, TEXT_COLOR

class GraduateBar(ttk.Frame):
    def __init__(self, master, width:int, height:int, orient:str="vertical", font_size:int = 13, text_color:str=TEXT_COLOR, background:str=GRADUATE_BAR_COLOR, border_color:str =BORDER_COLOR):
        ttk.Frame.__init__(
            self, master, width=width, 
            height=height, background=background, 
            bd = 1, highlightthickness=1, 
            highlightbackground=border_color, highlightcolor=border_color
        )
        self.pack_propagate(0)
        # self.grid_propagate(0)
        self.orient=orient
