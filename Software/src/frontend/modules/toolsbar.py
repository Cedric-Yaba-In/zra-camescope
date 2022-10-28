import os
from typing import Dict, List, Union
import tkinter as ttk

from colors import TOOLS_BAR_COLOR
from constants import PATH_TO_IMAGE
from custombuttonmodel import CustomButtonModel
from menuitemsection import MenuItemSection


class ToolsBar(ttk.Frame):

    def __init__(self, master:object, menu_items: Dict[str, Union[str, Dict[str, str]]], language:str, width:int, height:int, functions:Dict={}):
        ttk.Frame.__init__(self, master = master, width = width, height = height, bg=TOOLS_BAR_COLOR, borderwidth=0)

        join = os.path.join
        sections_items = {
            "project": [
                CustomButtonModel(
                    join(PATH_TO_IMAGE, f"file_n_{language}.png"),
                    join(PATH_TO_IMAGE, f"file_{language}.png"),  
                    command = functions.get("open_file", None)
                    ),
                CustomButtonModel(
                    join(PATH_TO_IMAGE, f"folder_n_{language}.png"), 
                    join(PATH_TO_IMAGE, f"folder_{language}.png"), 
                    command = functions.get("open_folder", None)
                    )
                ],
            "edit": [
                CustomButtonModel(
                    join(PATH_TO_IMAGE, f"undo_n_{language}.png"), 
                    join(PATH_TO_IMAGE, f"undo_{language}.png"), 
                    command = functions.get("undo", None)
                    ),
                CustomButtonModel(
                    join(PATH_TO_IMAGE, f"redo_n_{language}.png"), 
                    join(PATH_TO_IMAGE, f"redo_{language}.png"), 
                    command = functions.get("redo", None)
                    )
                ],
            "actions": [
                CustomButtonModel(
                    join(PATH_TO_IMAGE, f"play_n_{language}.png"), 
                    join(PATH_TO_IMAGE, f"play_{language}.png"), 
                    join(PATH_TO_IMAGE, f"play_disabled_{language}.png"), 
                    command = functions.get("play", None)
                    ),
                CustomButtonModel(
                    join(PATH_TO_IMAGE, f"pause_n_{language}.png"), 
                    join(PATH_TO_IMAGE, f"pause_{language}.png"), 
                    join(PATH_TO_IMAGE, f"pause_disabled_{language}.png"), 
                    command = functions.get("pause", None)
                    ),
                CustomButtonModel(
                    join(PATH_TO_IMAGE, f"stop_n_{language}.png"), 
                    join(PATH_TO_IMAGE, f"stop_{language}.png"), 
                    command = functions.get("stop", None)
                    ),
                CustomButtonModel(
                    join(PATH_TO_IMAGE, f"save_n_{language}.png"), 
                    join(PATH_TO_IMAGE, f"save_{language}.png"), 
                    command = functions.get("save", None)
                    ),
                CustomButtonModel(
                     join(PATH_TO_IMAGE, f"save_as_n_{language}.png"), 
                    join(PATH_TO_IMAGE, f"save_as_{language}.png"), 
                    command = functions.get("save_as", None)
                    ),
                # CustomButtonModel(
                #     join(PATH_TO_IMAGE, f"close_n_{language}.png"), 
                #     join(PATH_TO_IMAGE, f"close_{language}.png"), 
                #     command = functions.get("close", None)
                #     )
                ],
            "capture": [
                CustomButtonModel(
                    join(PATH_TO_IMAGE, f"image_n_{language}.png"), 
                    join(PATH_TO_IMAGE, f"image_{language}.png"), 
                    command = functions.get("capture_image", None)
                    ),
                CustomButtonModel(
                    join(PATH_TO_IMAGE, f"video_n_{language}.png"), 
                    join(PATH_TO_IMAGE, f"video_{language}.png"), 
                    join(PATH_TO_IMAGE, f"video_stop_{language}.png"), 
                    command = functions.get("capture_video", None)
                    )
                ],
            "filters": [
                CustomButtonModel(
                    join(PATH_TO_IMAGE, f"gaussian_n_{language}.png"), 
                    join(PATH_TO_IMAGE, f"gaussian_{language}.png"), 
                    command = functions.get("gaussian_filtrage", None)
                    ),
                CustomButtonModel(
                    join(PATH_TO_IMAGE, f"pepper_n_{language}.png"), 
                    join(PATH_TO_IMAGE, f"pepper_{language}.png"), 
                    command = functions.get("pepper_filtrage", None)
                    ),
                CustomButtonModel(
                    join(PATH_TO_IMAGE, f"laplace_n_{language}.png"), 
                    join(PATH_TO_IMAGE, f"laplace_{language}.png"), 
                    command = functions.get("laplace_filtrage", None)
                    ),
                # CustomButtonModel(
                #     join(PATH_TO_IMAGE, f"low_pass_n_{language}.png"), 
                #     join(PATH_TO_IMAGE, f"low_pass_{language}.png"), 
                #     command = functions.get("low_pass_filtrage", None)
                #     ),
                # CustomButtonModel(
                #     join(PATH_TO_IMAGE, f"high_pass_n_{language}.png"), 
                #     join(PATH_TO_IMAGE, f"high_pass_{language}.png"), 
                #     command = functions.get("high_pass_filtrage", None)
                #     ),
                ],
            "count": [
                CustomButtonModel(
                    join(PATH_TO_IMAGE, f"cells_n_{language}.png"), 
                    join(PATH_TO_IMAGE, f"cells_{language}.png"), 
                    join(PATH_TO_IMAGE, f"cells_{language}.png"), 
                    command = functions.get("count_cells", None)
                    ),
                ],
            "colorization": [
                CustomButtonModel(
                    join(PATH_TO_IMAGE, f"color_n_{language}.png"), 
                    join(PATH_TO_IMAGE, f"color_{language}.png"), 
                    command = functions.get("colorization", None)
                    ),
                ],
        }

        self.menu_item_objects:List[MenuItemSection] = [None] * len(sections_items)
        self.menu_item_objects[0] = MenuItemSection(self, items = sections_items["project"], label = menu_items["project"], background_color=TOOLS_BAR_COLOR)
        self.menu_item_objects[1] = MenuItemSection(self, items = sections_items["edit"], label = menu_items["edit"], background_color=TOOLS_BAR_COLOR)
        self.menu_item_objects[2] = MenuItemSection(self, items = sections_items["actions"], label = menu_items["actions"], background_color=TOOLS_BAR_COLOR)
        self.menu_item_objects[3] = MenuItemSection(self, items = sections_items["capture"], label = menu_items["capture"], background_color=TOOLS_BAR_COLOR)
        self.menu_item_objects[4] = MenuItemSection(self, items = sections_items["filters"], more= lambda a:a,  label = menu_items["filters"], background_color=TOOLS_BAR_COLOR)
        self.menu_item_objects[5] = MenuItemSection(self, items = sections_items["count"], label = menu_items["count"], background_color=TOOLS_BAR_COLOR)
        self.menu_item_objects[6] = MenuItemSection(self, items = sections_items["colorization"], label = menu_items["colorization"], background_color=TOOLS_BAR_COLOR)

        for item in self.menu_item_objects:
            item.pack(side = 'left', padx=8, pady=5)