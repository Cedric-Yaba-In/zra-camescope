import tkinter as ttk
from typing import Callable
from PIL import Image, ImageTk

from colors import BUTTON_BACKGROUND_COLOR

class CustomButton(ttk.Canvas):
    def __init__(self, master, default_image:str, active_image:str, second_image=None, command = None, width:int = 52, height:int = 52, background:str=BUTTON_BACKGROUND_COLOR):
        self.image_d = Image.open(default_image)
        self.image_a = Image.open(active_image)

        if width == None:
            width = self.image_d.width
        if height == None:
            height = self.image_d.height

        self.image_d = self.image_d.resize((width, height))
        self.image_a = self.image_a.resize((width, height))

        self.default_image = ImageTk.PhotoImage(self.image_d)
        self.active_image = ImageTk.PhotoImage(self.image_a)

        self.second_image = None
        if second_image != None:
            self.image_s = Image.open(second_image)
            self.image_s = self.image_s.resize((width, height))
            self.second_image = ImageTk.PhotoImage(self.image_s)

        self.current_image = self.default_image
        self.command = command

        ttk.Canvas.__init__(self, master=master, width=width, height=height, background=background, bd=0, highlightthickness=0)
        self.pack_propagate(False)

        self.button = ttk.Button(self, image=self.current_image, relief='flat', bd=0, highlightthickness=0, background=background)#, command=self.command
        self.button.pack()
        self.button.bind("<Button-1>", func=self.pressed, add="+")
        self.button.bind("<Enter>", func=self.enter_event, add="+")
        self.button.bind("<Leave>", func=self.leave_event, add="+")
    
    def change(self, default_image:str, active_image:str, command = None):
        self.default_image = default_image
        self.active_image = active_image
        self.command = command
    
    def pressed(self, event):
        if self.second_image != None:    
            if self.current_image == self.default_image:
                self.current_image = self.second_image
            else:
                self.current_image = self.default_image
            self.button.configure(image=self.current_image)
        try:
            self.command(event)
        except Exception as error:
            pass
    
    def set_click_function(self, function:Callable):
        try:
            function()
        except Exception as error:
            print(error)

    def enter_event(self, event:ttk.Event):
        self.button.configure(image=self.active_image)
    
    def leave_event(self, event:ttk.Event):
        self.button.configure(image=self.current_image)