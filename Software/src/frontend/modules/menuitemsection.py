import os
from typing import List

import tkinter as ttk

from PIL import Image, ImageTk
from custombutton import CustomButton

from custombuttonmodel import CustomButtonModel
from colors import HOVER_TEXT_COLOR, TEXT_COLOR, TOOLS_BAR_COLOR
from constants import PATH_TO_IMAGE

class MenuItemSection(ttk.Frame):
    def __init__(self, 
        master, items:List[CustomButtonModel] = [], 
        label:str = "Section", more = None, 
        background_color:str = TOOLS_BAR_COLOR
        ) -> (None):

        n = len(items)
        frame_width = 75 * n
        frame_height = 70

        ttk.Frame.__init__(
            self, master=master,
            width = frame_width, 
            height = frame_height, 
            bg=background_color
        )

        canvas_width = frame_width
        canvas_height = frame_height - 10
        canvas_ipadx = 5
        canvas_ipady = 5

        can = ttk.Canvas(
            self, width=canvas_width,
            height=canvas_height, background=background_color, 
            highlightthickness=0, borderwidth=0, 
            border=0
        )

        can.grid(row=0, column=0, columnspan=2, ipadx=canvas_ipadx, ipady=canvas_ipady)

        ttk.Label(self, 
            text = label.capitalize(), 
            foreground=TEXT_COLOR, 
            background=background_color
            ).grid(row = 1, column=0, sticky="W")
        
        
        if more != None:
            more_label = ttk.Label(self, 
            text="more >> ", 
            activeforeground=HOVER_TEXT_COLOR, 
            foreground=TEXT_COLOR, background=background_color
            )

            more_label.grid(row = 1, sticky='E', column=1)
            more_label.bind("<Button-1>", lambda t : self.click("click on more"))

        self.image = Image.open(os.path.join(PATH_TO_IMAGE, f"menu_item_background_x{n}.png"))
        self.image = self.image.resize((canvas_width, canvas_height))
        self.img = ImageTk.PhotoImage(self.image)
        can.create_image(canvas_width//2, canvas_height//2, image = self.img)

        for item in items:
            #print((canvas_width, canvas_height), ((canvas_width - 10) // n - 10, canvas_height - 10))
            custom_button = CustomButton(
                master = can, 
                default_image = item.default_image_path, 
                active_image = item.active_image_path,
                second_image = item.second_image_path, 
                command=item.commad,
                width= (canvas_width - 10) // n - 16,
                height= canvas_height - 10
            )
            custom_button.pack(side='left', padx=9)
        # print()

    def click(self, text):
        print(text)
