import sys
import os
import threading
import time
import tkinter as ttk

from pathlib import Path
from client import ReceiveData
from camera import MyVideoCapture

##########Last##################
# sys.path.append(os.path.join(".", "modules"))
# sys.path.append(os.path.join(".", "models"))
# sys.path.append(os.path.join(".","..", "configs"))
# sys.path.append(os.path.join(".", "constants"))
# sys.path.append(os.path.join(".", "components"))
# sys.path.append(os.path.join(".", "..", "backend"))
###########Last###############################

##################New#######################################
sys.path.append(os.path.join(os.path.dirname(__file__),"..", "modules"))
sys.path.append(os.path.join(os.path.dirname(__file__),"..", "models"))
sys.path.append(os.path.join(os.path.dirname(__file__),".." ,"configs"))
sys.path.append(os.path.join(os.path.dirname(__file__),"..", "constants"))
sys.path.append(os.path.join(os.path.dirname(__file__),"..", "components"))
sys.path.append(os.path.join(os.path.dirname(__file__),"..", "..", "backend"))
######################New###########################################


# print(sys.path)
from configs import APP_DIR, APP_NAME, INFORMATION, load_language
from colors import BACKGROUND_COLOR, BACKGROUND_COLOR_1, MENU_COLOR, TRANSPARENT

from load_page import LoadPage

from titlebar import TitleBar
from menubar import MenuBar
from toolsbar import ToolsBar
from displaysection import DisplaySection
from inspectorsection import InspectorSection
from verticaltoolsbar import VerticalToolsBar

home = str(Path.home())
Path(os.path.join(home, APP_DIR)).mkdir(parents=True, exist_ok=True)  


class MainPage(ttk.Tk):
    def __init__(self) -> None:
        super().__init__(className="toplevel")
        # self.state('zoomed')
        self.screen_width = self.winfo_screenwidth() - 20
        self.screen_height = self.winfo_screenheight() - 80
        self.geometry(f"{self.winfo_screenwidth()}x{self.screen_height}+0+0")
        self.title(APP_NAME)
        self.configure(bg=BACKGROUND_COLOR)


        # self.overrideredirect(True)
        
        
        self.resizable(width=False, height=False)
        tools_bar_width = 140
        inspector_section_width = 240
        display_section_width = self.screen_width - (tools_bar_width + inspector_section_width)
        menu_height = 30
        tools_menu_height = 84
        bottom_sections_height = self.screen_height - (menu_height + tools_menu_height)

        self.language = load_language()

        self.display_section = DisplaySection(
            self, menu_items=[], 
            language="en", 
            width=display_section_width, 
            height=bottom_sections_height - 2, 
            background=BACKGROUND_COLOR_1,
            copyright = "" if INFORMATION == {} else f"Copyright - {INFORMATION['compagny']} & {INFORMATION['owner']} - {INFORMATION['copyright']}" 
        )

        functions = {
            "pause": self.display_section.pause,
            "play": self.display_section.play,
            "stop": self.display_section.stop,
            "close": self.destroy,
            "count_cells": self.display_section.count_cells,
            "select_rectangle": None,
            "select_cursor": None,
            "text_add": self.display_section.add_text_entry,
            "draw_rectangle": self.display_section.draw_rectangle,
            "draw_ellips": self.display_section.draw_ellips,
            "draw_line": self.display_section.draw_line,
            "draw_pencil": self.display_section.free_draw,
            "draw_eraser": None,
            "draw_size": None,
            "zoom_zoom": self.display_section.zoom_zoom,
            "zoom_to_fit": self.display_section.zoom_to_fit,
            "zoom_in": self.display_section.zoom_in,
            "zoom_out": self.display_section.zoom_out,
            "zoom_collapse": self.display_section.zoom_collapse,
            "zoom_expand": self.display_section.zoom_expand,
            "capture_video": self.display_section.capture_video,
            "capture_image": self.display_section.capture_image
        }

        self.title_bar = TitleBar(
            self, 
            menu_items = self.language["menu_bar"], 
            width = self.screen_width+10, 
            height = menu_height, 
            background = MENU_COLOR,
            functions=functions, 
            iconify = lambda event: self.iconify(), 
            maximize = lambda event: self.state('zoomed'), 
            minimize = lambda event: self.state("normal"), 
            close = lambda event: self.destroy()
        )
        self.title_bar.pack_propagate(False)
        self.title_bar.grid(row=0, column=0, columnspan=3, sticky="W")

        
        self.title_bar.set_title("New project")
        
        self.horizontal_tools_bar = ToolsBar(
            self, 
            menu_items=self.language["tools_bar"], 
            width = self.screen_width, 
            height= tools_menu_height, 
            language='en',
            functions = functions
        )

        self.horizontal_tools_bar.pack_propagate(0)
        self.horizontal_tools_bar.grid(sticky='W', row=1, columnspan=3, ipadx=5, ipady=2)

        self.vertical_tools_bar = VerticalToolsBar(
            self, 
            menu_items=self.language["tools"], 
            language="en", 
            functions = functions,
            width=tools_bar_width + 9, 
            height=bottom_sections_height - 2
        )

        self.vertical_tools_bar.pack_propagate(False)
        self.vertical_tools_bar.grid(sticky="W", row = 2, column=0, pady=1, ipady=0, ipadx=0)


        self.display_section.pack_propagate(False)
        self.display_section.grid(sticky="W", row = 2, column=1, pady=1, ipady=0, ipadx=0)


        self.inspector_section = InspectorSection(
            self, menu_items=self.language["inspector"], 
            language="en", 
            width=inspector_section_width, 
            height=bottom_sections_height - 2
        )
        self.inspector_section.pack_propagate(False)
        self.inspector_section.grid(sticky="E", row = 2, column=2, pady=1, ipady=0, ipadx=0)

        self.display_section.set_count_cells_result_function(self.inspector_section.number_of_cells)
        self.display_section.set_add_layer_function(self.inspector_section.add_new_layer)

        self.inspector_section.set_change_visibility_function(self.display_section.change_visibility)
        self.inspector_section.set_remove_funtion(self.display_section.remove_element)
        self.inspector_section.set_add_text_function(self.display_section.add_text)

        self.vid = MyVideoCapture(0)
        self.display_section.draw_image(self.vid)
        # receiver = ReceiveData(self.display_section.draw_image)
        # receiver_thread = threading.Thread(target=receiver.run)
        # receiver_thread.daemon = True
        # receiver_thread.start()

    def open_app(self):
        self.mainloop()
    
    def close_app(self):
        self.destroy()
    
    def init_event(self):
        self.bind("<Control-KeyPress-S>", lambda event: self.affiche("enregistrement") ,add="+")
        self.bind("<Control-KeyPress-N>", lambda event: self.affiche("nouveau projet") ,add="+")
    
    def affiche(self, text):
        print("evenement sur la fenetre principale", text)

def open_main_page(root:ttk.Tk):
    # root.destroy()
    mainPage = MainPage()
    mainPage.open_app()
    

if __name__ == "__main__":
    # root = ttk.Tk()
    # loadPage = LoadPage(root)
    # loadPage.pack()
    # loadPage.start_loading(lambda: open_main_page(root))
    # root.mainloop()
    mainPage = MainPage()
    mainPage.open_app()