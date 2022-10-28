import os
import tkinter as ttk
from PIL import Image, ImageTk
from typing import Dict, List, Union

from matplotlib import image

from colors import TOOLS_BAR_COLOR
from configs import LOGO_2
from constants import PATH_TO_IMAGE
from custombuttonmodel import CustomButtonModel
from toolsbarsection import ToolsBarSection

class VerticalToolsBar(ttk.Frame):
    def __init__(self, master:object, menu_items: Dict[str, Union[str, Dict[str, str]]], language:str, width:int, height:int, functions={}, background=TOOLS_BAR_COLOR):
        ttk.Frame.__init__(self, master = master, width = width, height = height, background=background, borderwidth=2)

        join = os.path.join
        sections_items_function = {}
        n = len(menu_items)
        for key in menu_items:
            items = []
            for element in menu_items[key]["subsections"]:
                key_item = f"{key}_{element}"
                _function = functions.get(key_item, None) 
                sections_items_function[f"{key}_{element}"] = _function
                items.append(CustomButtonModel(
                                                join(PATH_TO_IMAGE, f"{key}_{element}_{language}.png"), 
                                                join(PATH_TO_IMAGE, f"{key}_{element}_n_{language}.png"), 
                                                join(PATH_TO_IMAGE, f"{key}_{element}_selected_{language}.png"), 
                                                command=sections_items_function[f"{key}_{element}"]
                                            )
                )

            tools_item_section = ToolsBarSection(self, items = items, width = width - 10, height= (height - 10)// n, label = menu_items[key]["name"], key_name=key, background_color=TOOLS_BAR_COLOR)
            tools_item_section.pack(side = 'top', padx=5, pady=5)
        logo = Image.open(join(PATH_TO_IMAGE, LOGO_2))
        # logo = logo.resize((width - 30, width - 30))
        self.logo = ImageTk.PhotoImage(logo)
        ttk.Label(self, image=self.logo, background=background).pack(side="bottom", padx = 15, pady=10)