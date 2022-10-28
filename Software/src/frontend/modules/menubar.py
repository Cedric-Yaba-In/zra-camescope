import tkinter as ttk
from tkinter import font
from typing import Callable, Dict, Union
from xml.dom.expatbuilder import TEXT_NODE

from colors import MENU_ACTIVE_COLOR, MENU_TEXT_COLOR, SUB_MENU_COLOR, TEXT_COLOR
from font import MENU_ITEM_FONT

class MenuBar(ttk.Frame):
    def __init__(self, master, width:int, height:int, menu_items: Dict[str, Union[str, Dict[str, str]]], background:str, functions:Dict[str, Callable]={}):
        ttk.Frame.__init__(self, master = master, width=width, height = height,  borderwidth=2, background=background)

        binders = {}
        for menu_item in menu_items:
            fileMenu = ttk.Menubutton(
                self, text = menu_items[menu_item]["name"].capitalize(), 
                background=background, activebackground=MENU_ACTIVE_COLOR, 
                activeforeground=TEXT_COLOR, foreground=MENU_TEXT_COLOR, borderwidth=0,
                font = MENU_ITEM_FONT, justify="left", direction='below',
                relief="flat", height= 1, bd=0, highlightthickness=0, anchor="w"
            )
            fileMenu.pack(side="left", padx=5)

            menu_obj = ttk.Menu(
                fileMenu,
                bd = 0,
                background=background,
                activebackground= background,
                activeforeground= background,
                font = MENU_ITEM_FONT,
                tearoff=0
                )

            for submenu_item in menu_items[menu_item]["subsections"]:
                menu_obj.add_command(
                    label=menu_items[menu_item]["subsections"][submenu_item].capitalize(), 
                    foreground=TEXT_COLOR, 
                    activeforeground= TEXT_COLOR,
                    background= SUB_MENU_COLOR, 
                    activebackground=MENU_ACTIVE_COLOR,
                    command=functions.get(submenu_item, None)
                    )
                menu_obj.configure(relief='flat', type='menubar')
            fileMenu.configure(menu = menu_obj, bd=0, highlightthickness=0, justify="left")
