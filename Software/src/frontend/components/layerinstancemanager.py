import os
import tkinter as ttk
from typing import Callable

from PIL import Image, ImageTk

from colors import BORDER_COLOR, LAYER_INSTANCE_COLOR, TEXT_COLOR
from constants import PATH_TO_IMAGE

class LayerInstanceManager(ttk.Canvas): 
    def __init__(
        self, 
        master, 
        type:str, 
        name:str, 
        width:int, 
        height:int = 40, 
        background:str=LAYER_INSTANCE_COLOR, 
        text_color:str=TEXT_COLOR
        ):

        ttk.Canvas.__init__(
            self, 
            master, 
            background=background,
            width=width, 
            height=height, 
            highlightbackground=BORDER_COLOR,
            highlightcolor=BORDER_COLOR,
            highlightthickness=1
        )
        self.pack_propagate(False)

        self.visibility_function = lambda: None
        self.remove_function = lambda: None
        
        image_width = height
        image_height = height

        self.layer_image = Image.open(os.path.join(PATH_TO_IMAGE, f"{type}_layer.png"))
        self.layer_image = self.layer_image.resize((height, height))
        self.layer_img = ImageTk.PhotoImage(self.layer_image)

        ttk.Label(
            self, 
            image=self.layer_img, 
            background=background
        ).pack(side="left")

        self.visible_image = Image.open(os.path.join(PATH_TO_IMAGE, "visible.png"))
        self.visible_image = self.visible_image.resize((height-14, height-14))
        self.visible_img = ImageTk.PhotoImage(self.visible_image)

        self.invisible_image = Image.open(os.path.join(PATH_TO_IMAGE, "invisible.png"))
        self.invisible_image = self.invisible_image.resize((height - 14, height - 14))
        self.invisible_img = ImageTk.PhotoImage(self.invisible_image)

        self.is_visible = True
        self.visibility_button = ttk.Label(
            self, 
            image=self.visible_img,
            background=background
        )
        self.visibility_button.pack(side="left", padx=2, pady=2) 
        self.visibility_button.bind("<Button-1>", self._on_click_visibility, add="+")       

        self.label_name_controller = ttk.StringVar()
        self.layer_name = ttk.Entry(
            self, 
            background=background, 
            highlightthickness=0, 
            highlightcolor="black", 
            highlightbackground="black",
            textvariable= self.label_name_controller,
            foreground=text_color,
            width=16,
            justify='center',
            relief='flat'
        )
        self.layer_name.insert("end", name)
        self.layer_name.bind("<FocusIn>", self._on_focus, add="+")
        self.layer_name.bind("<FocusOut>", self._on_blur, add="+")
        self.layer_name.bind("<KeyPress-Return>", self._on_blur, add="+")

        self.layer_name.pack(side="left")

        self.trash_default_image = Image.open(os.path.join(PATH_TO_IMAGE, "trash.png"))
        self.trash_default_image = self.trash_default_image.resize((height - 14, height - 14))
        self.trash_default_img = ImageTk.PhotoImage(self.trash_default_image)

        self.trash_activate_image = Image.open(os.path.join(PATH_TO_IMAGE, "trash_n.png"))
        self.trash_activate_image = self.trash_activate_image.resize((height - 14, height - 14))
        self.trash_activate_img = ImageTk.PhotoImage(self.trash_activate_image)

        self.remove_button = ttk.Label(
            self, 
            image=self.trash_default_img,
            background=background
        )
        self.remove_button.pack(side="right", padx = 20) 
        
        self.remove_button.bind("<Button-1>", self._remove, add="+")
        self.remove_button.bind("<Enter>", self._on_enter_delete, add="+")
        self.remove_button.bind("<Leave>", self._on_leave_delete, add="+")

    def set_remove_function(self, new_function:Callable):
        self.remove_function = new_function

    def set_change_visibility_function(self, new_function:Callable):
        self.visibility_function = new_function

    def _remove(self, event=None):
        try:
            self.remove_function()
        except Exception as error:
            print(error)

    def _on_enter_delete(self, event):
        self.remove_button.configure(image=self.trash_activate_img)
    
    def _on_leave_delete(self, event):
        self.remove_button.configure(image=self.trash_default_img)

    def _on_click_visibility(self, event):
        try:
            response = self.visibility_function(not self.is_visible)
            if response == True:
                if self.is_visible:
                    self.visibility_button.configure(image=self.invisible_img)
                else:
                    self.visibility_button.configure(image=self.visible_img)
                self.is_visible = not self.is_visible
        except Exception as error:
            print(error)

    def _on_focus(self, event):
        self.layer_name.configure(highlightthickness=1)
    
    def _on_blur(self, event):
        self.layer_name.configure(highlightthickness=0)
        self.focus_set()
    
    def get_label_name(self)->(str):
        print("text:", self.label_name_controller.get())
        return self.label_name_controller.get()