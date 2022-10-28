import os
from typing import Dict, List
import tkinter as ttk
from PIL import Image, ImageTk

from constants import PATH_TO_IMAGE
from custombutton import CustomButton
from custombuttonmodel import CustomButtonModel
from colors import BORDER_COLOR, HOVER_TEXT_COLOR, TEXT_COLOR, TOOLS_BAR_COLOR

class ToolsBarSection(ttk.Frame):
    def __init__(self, 
        master, 
        items:List[CustomButtonModel] = [], 
        key_name="select", 
        label:str = "Section",
        width:int = 140, 
        height = 40,
        background_color:str = TOOLS_BAR_COLOR
        ) -> (None):

        self.image = Image.open(os.path.join(PATH_TO_IMAGE, f"background_tools_section_{key_name}.png"))
        frame_width = width
        frame_height = self.image.height + 10

        ttk.Frame.__init__(
            self, master=master,
            width = frame_width, 
            height= frame_height,
            bg=background_color
        )

        canvas_width = frame_width - 10
        canvas_height = frame_height - 10

        canvas_ipadx = 0
        canvas_ipady = 0
        if key_name == "color":
            canvas_ipadx = 0
            canvas_ipady = 0
        
        self.image = self.image.resize((canvas_width, canvas_height))
        self.img = ImageTk.PhotoImage(self.image)
        
        ttk.Label(self, 
            text = label.capitalize(), 
            foreground=TEXT_COLOR, 
            background=background_color
            ).grid(row = 0, column=0, sticky="W")

        can = ttk.Canvas(
            self, width=canvas_width,
            height=canvas_height, background=background_color, 
            highlightthickness=0, borderwidth=0, 
            border=0
        )
        can.grid(row=1, column=0, ipadx=canvas_ipadx, ipady=canvas_ipady)
        can.grid_propagate(0)
        can.create_image(canvas_width//2, canvas_height//2, image = self.img)

        if key_name == "color":
            if True:
                padx = 1
                pady = 1

                color_picker = ttk.Frame(
                    can, 
                    width = canvas_width//2 - 8, 
                    height = canvas_height - 26,
                    background = "#00FF00"
                )
                color_picker.grid(row=0, column=0, rowspan=3, padx=6, pady=13)
                
                # front_color_picker = ttk.Frame(
                #     color_picker, 
                #     width = (canvas_width//2 - 8)//2, 
                #     height = canvas_height - 26,
                #     background = "#3D3D3D"
                # )

                # front_color_picker = ttk.Frame(
                #     color_picker, 
                #     width = (canvas_width//2 - 8)//2, 
                #     height = canvas_height - 26,
                #     background = "#3D3D3D"
                # )

    
                font_text = ("Segeo UI", 10)
                entry_font = ("Segeo UI", 8)
                ttk.Label(
                    can, 
                    text="R", 
                    font=font_text, 
                    foreground=TEXT_COLOR, 
                    background="#3D3D3D"
                ).grid(row=0, column=1, padx=padx, pady=pady)
                ttk.Label(
                    can, 
                    text="G", 
                    font=font_text, 
                    foreground=TEXT_COLOR, 
                    background="#3D3D3D"
                ).grid(row=1, column=1, padx=padx, pady=0)
                ttk.Label(
                    can, 
                    text="B", 
                    font=font_text, 
                    foreground=TEXT_COLOR, 
                    background="#3D3D3D"
                ).grid(row=2, column=1, padx=padx, pady=pady)
            
                red_value = ttk.IntVar()
                red_value.set(0)
                green_value = ttk.IntVar()
                green_value.set(255)
                blue_value = ttk.IntVar()
                blue_value.set(0)

                red_entry = ttk.Entry(
                    can, 
                    textvariable = red_value, 
                    font = entry_font, 
                    width = 3,
                    foreground = TEXT_COLOR, 
                    bd = 1,
                    highlightthickness=1,
                    highlightcolor = BORDER_COLOR,
                    highlightbackground = BORDER_COLOR,
                    background = "#3D3D3D",
                    relief="flat"
                )
                red_entry.grid(row=0, column=2, padx=padx, pady=pady, ipadx=3, ipady=0)
                red_entry.bind("<KeyPress-Return>", self.leave)

                green_entry = ttk.Entry(
                    can, 
                    textvariable = green_value, 
                    font = entry_font, 
                    width = 3,
                    foreground = TEXT_COLOR, 
                    bd = 1,
                    highlightthickness=1,
                    highlightcolor = BORDER_COLOR,
                    highlightbackground = BORDER_COLOR,
                    background = "#3D3D3D",
                    relief="flat"
                )
                green_entry.grid(row=1, column=2, padx=padx, pady=pady, ipadx=3, ipady=0)
                green_entry.bind("<KeyPress-Return>", self.leave)

                blue_entry = ttk.Entry(
                    can, 
                    textvariable = blue_value, 
                    font = entry_font, 
                    width = 3,
                    foreground = TEXT_COLOR, 
                    bd = 1,
                    highlightthickness=1,
                    highlightcolor = BORDER_COLOR,
                    highlightbackground = BORDER_COLOR,
                    background = "#3D3D3D",
                    relief="flat"
                )
                blue_entry.bind("<KeyPress-Return>", self.leave)
                blue_entry.grid(row=2, column=2, padx=padx, pady=pady, ipadx=3, ipady=0)

        elif key_name == "text":
            frame_left = ttk.Frame(
                can, 
                width=canvas_width//2, 
                height=canvas_height, 
                background= "#3D3D3D"
            )
            
            frame_left.grid(row=0, column=0, padx=3, pady=4)
            # frame_left.grid_propagate(False)

            color_setion_height = 10
            padx = 4
            pady = 5
            button = CustomButton(
                master = frame_left,
                default_image = items[0].default_image_path,
                active_image = items[0].active_image_path,
                second_image = items[0].second_image_path,
                command= items[0].commad,
                width= canvas_width//2 - 2*padx, 
                height= canvas_height - color_setion_height - 4*pady
            )
            button.grid(row=0, column=0, padx=padx, pady=pady-3)
            
            color = ttk.Frame(
                    master=frame_left,
                    width=canvas_width//2 - 2*padx,
                    height= color_setion_height,
                    background="white"
            )
            color.grid(row=1, column=0, padx=padx, pady=4)

            frame_right = ttk.Frame(
                can, 
                width=canvas_width//2 - 16, 
                height=canvas_height-10, 
                background="#3D3D3D"
            )
            frame_right.grid(row=0, column=1, padx=1, pady=2, ipadx=2, ipady=2)
            frame_right.grid_propagate(False)

            size_value = ttk.IntVar()
            size_value.set(15)

            size_entry = ttk.Entry(
                    frame_right, 
                    textvariable = size_value, 
                    font = ("Segeo UI", 10), 
                    width = 4,
                    foreground = TEXT_COLOR, 
                    bd = 1,
                    highlightthickness=1,
                    highlightcolor = BORDER_COLOR,
                    highlightbackground = BORDER_COLOR,
                    background = "#3D3D3D",
                    relief="flat"
                )
            size_entry.grid(row=0, column=0, columnspan=3, padx=padx, pady=pady, ipadx=3, ipady=0)
            size_entry.bind("<KeyPress-Return>", self.leave)
            
            n = len(items)
            row = 0
            count = 0
            buttons:List[ttk.Label] = [None] * n 
            for n_itr in range(2, n):
                if count == 0:
                    row += 1
                image = Image.open(items[n_itr].default_image_path)
                self.image = ImageTk.PhotoImage(image)
                buttons[n_itr] = ttk.Label(
                    master = frame_right, 
                    image = self.image,
                    background="#3D3D3D"
                )
                buttons[n_itr].grid(row=row, column=count, padx=1, pady=1)
                buttons[n_itr].bind("<Button-1>", lambda event: self.modify_text(buttons[n_itr], items[n_itr].commad))
                count = (count + 1)%3
        else:
            max_items = 3
            if key_name == "zoom":
                max_items = 2
            
            blocks = len(items) // max_items + (1 if len(items)%max_items > 0 else 0) 
            row = -1
            count = 0
            for item in items:
                if count == 0:
                    row += 1
                try:
                    custom_button = CustomButton(
                        master = can, 
                        default_image = item.default_image_path, 
                        active_image = item.active_image_path, 
                        second_image = item.second_image_path,
                        command= item.commad,
                        width= None,
                        height= None,
                        background = "#3D3D3D"
                    )
                    custom_button.grid(row=row, column=count, pady=5, padx=5)
                    count = (count + 1)%max_items
                except Exception as error:
                    print(error)
            # print()

    def leave(self, event):
        self.focus_set()

    def modify_text(self, text_object:ttk.Label, function_to_call):
        background_color = text_object.configure()["background"][-1]
        if background_color.upper() == "#3D3D3D":
            text_object.configure(background="#000000")
        else:
            text_object.configure(background="#3D3D3D")
        try:
            function_to_call()
        except Exception:
            pass
