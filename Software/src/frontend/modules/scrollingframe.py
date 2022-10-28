import tkinter as ttk

from titleframe import TitleFrame

from colors import BACKGROUND_COLOR_1, BORDER_COLOR, INSPECTOR_BACKGROUND_COLOR, TEXT_COLOR

class ScrollingFrame(ttk.Frame):
    def __init__(self, master, title:str, width:int, height:int, background_color:str=INSPECTOR_BACKGROUND_COLOR, title_bar_height:int=36, title_bar_color:str = BACKGROUND_COLOR_1, title_bar_text_color:str = TEXT_COLOR, title_bar_border_color:str=BORDER_COLOR):
        ttk.Frame.__init__(self, master, width=width, height=height, background=background_color)

        title_bar = TitleFrame(self, text=title, width=width, height=title_bar_height, font_size=14, text_color=title_bar_text_color, background= title_bar_color, border_color= title_bar_border_color)
        title_bar.pack(side='top')

        self.container = ttk.Frame(self, width = width, height = height - title_bar_height, background=background_color)
        self.container.pack(side ="top")
    
    def get_container(self) -> (ttk.Frame):
        return self.container
