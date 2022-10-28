from pydoc import text
from re import L
import tkinter as ttk
from typing import Dict, List, Union

from numpy import pad

from colors import BACKGROUND_COLOR_1, BACKGROUND_COLOR_2, BORDER_COLOR, TEXT_COLOR, TOOLS_BAR_COLOR
from layer_model import LayerModel
from layerinstancemanager import LayerInstanceManager
from scrollingframe import ScrollingFrame
from titleframe import TitleFrame

class InspectorSection(ttk.Frame):
    def __init__(self, master:object, menu_items: Dict[str, Union[str, Dict[str, str]]], language:str, width:int, height:int, background=TOOLS_BAR_COLOR):
        ttk.Frame.__init__(self, master = master, width = width, height = height, background=background, borderwidth=0)
        self.pack_propagate(False)
        self.grid_propagate(False)

        section_title_height = 30
        section_height = (height-section_title_height)//2

        self.change_visibility_function = lambda element, visibility : None
        self.remove_function = lambda element: None
        self.add_text_function = lambda x, y, text, size: None

        properties_section = ScrollingFrame(self, title=menu_items["properties"]["name"], width=width, height = section_height)
        properties_section.pack(side = "top")
        properties_container = properties_section.get_container()
        properties_container.grid_propagate(False)

        number_of_cell_label = ttk.Label(
            properties_container, 
            text="Number of cells :", 
            font=("Segeo UI", 16), 
            foreground=TEXT_COLOR, background=background
        )
        number_of_cell_label.grid(row=0, column=0, padx= 10, columnspan=2, pady=10)

        self.number_of_cells_value = ttk.StringVar()
        self.number_of_cells_value_label = ttk.Label(
            properties_container, 
            text="", 
            font=("Segeo UI", 16), 
            textvariable=self.number_of_cells_value,
            foreground="gold", background=background
        )
        self.number_of_cells_value_label.grid(row=0, column=2, padx= 0, pady=10)

        # ttk.Label(
        #     properties_container, 
        #     text="x, y, text", 
        #     font=("Segeo UI", 13),
        #     foreground=TEXT_COLOR, background=background
        # ).grid(row=1, column=0, padx=10, pady=5, sticky="w")

        # _validate_function = lambda text: str(text).isnumeric()
        # validate_function = self.register(_validate_function)
        # self.x_variable = ttk.IntVar()
        # self.x_variable.set(100)
        # ttk.Entry(
        #     properties_container, 
        #     textvariable=self.x_variable, 
        #     font=("Segeo UI", 14), 
        #     foreground=TEXT_COLOR, 
        #     background="#3D3D3D", 
        #     relief="flat",
        #     width=4,
        #     highlightthickness=1,
        #     highlightcolor=BORDER_COLOR,
        #     highlightbackground=BORDER_COLOR,
        #     validate = "key",
        #     validatecommand= (validate_function, self.x_variable)
        # ).grid(row=1, column=1, padx=0, pady=5, sticky="w")

        # self.y_variable = ttk.IntVar()
        # self.y_variable.set(50)
        # ttk.Entry(
        #     properties_container, 
        #     textvariable=self.y_variable, 
        #     font=("Segeo UI", 14), 
        #     foreground=TEXT_COLOR, 
        #     background="#3D3D3D", 
        #     relief="flat",
        #     width=4,
        #     highlightthickness=1,
        #     highlightcolor=BORDER_COLOR,
        #     highlightbackground=BORDER_COLOR,
        #     validate = "key",
        #     validatecommand= (validate_function, self.y_variable)
        # ).grid(row=1, column=2, padx=0, pady=5, sticky="w")

        # self.text_variable = ttk.StringVar()
        # self.add_text_frame = ttk.Text(
        #     properties_container,
        #     font = ("Segeo UI", 12),
        #     width = 24,
        #     height = 4,
        #     highlightthickness = 1,
        #     highlightbackground = BORDER_COLOR,
        #     highlightcolor = BORDER_COLOR,
        #     relief = "flat",
        #     foreground = TEXT_COLOR,
        #     background = "#3D3D3D",
        # )
        # self.add_text_frame.grid(row=2, column=0, padx=10, pady=2, columnspan=3)

        # ttk.Label(
        #     properties_container, 
        #     text="Font size", 
        #     font=("Segeo UI", 13),
        #     foreground=TEXT_COLOR, background=background
        # ).grid(row=3, column=0, padx=10, pady=15, sticky="w")

        # self.font_size_variable = ttk.IntVar()
        # self.font_size_variable.set(12)
        # ttk.Entry(
        #     properties_container, 
        #     textvariable=self.font_size_variable, 
        #     font=("Segeo UI", 14), 
        #     foreground=TEXT_COLOR, 
        #     background="#3D3D3D", 
        #     relief="flat",
        #     width=5,
        #     highlightthickness=1,
        #     highlightcolor=BORDER_COLOR,
        #     highlightbackground=BORDER_COLOR,
        #     validate = "key",
        #     validatecommand= (validate_function, self.font_size_variable)
        # ).grid(row=3, column=1, padx=0, pady=15, sticky="w")

        # ttk.Button(
        #     properties_container, 
        #     text="Ok", 
        #     font=("Segeo UI", 12),
        #     foreground=TEXT_COLOR, 
        #     background="#3D3D3D",
        #     relief="raised",
        #     bd=1,
        #     highlightthickness=1,
        #     highlightbackground=BORDER_COLOR,
        #     highlightcolor=BORDER_COLOR,
        #     command=self.get_text
        # ).grid(row=3, column=2, padx=5, pady=15, sticky="w")

        layers_section = ScrollingFrame(self, title=menu_items["layers"]["name"], width=width, height = section_height)
        layers_section.pack(side="top")
        layer_container = layers_section.get_container()

        self.canvas_width = width - 12
        canvas_height = section_height-36
        self.canvas_width_x_scroll = self.canvas_width
        self.canvas_width_y_scroll = canvas_height
        
        self.layer = ttk.Canvas(
            layer_container, 
            width = self.canvas_width, 
            height = canvas_height, 
            highlightthickness=0, 
            background=background
        )
        self.layer.grid(row=0, column=0)
        self.layer.pack_propagate(False)
        self.layer.grid_propagate(False)

        schroll = ttk.Scrollbar(layer_container, orient="vertical", width=12, command=self.layer.yview)
        schroll.grid(row=0, column=1, sticky='ns')
        self.layer["yscrollcommand"] = schroll.set
        
        self.layer_id:int = 0
        self.layers_dict:Dict[int, LayerModel] = {}
        self.layer_height = 34

       
        #--default_layer
        # add = LayerInstanceManager(self.layer, "default", "Camera", self.canvas_width, height=self.layer_height)
        # # add.set_remove_function(lambda: add.destroy())
        # add.pack(side='top')    

        section_title = TitleFrame(self, text=menu_items["name"], height=section_title_height, width=width)
        section_title.pack(side="bottom")
    
    def get_text(self, event=None):
        text = self.add_text_frame.get("1.0", "1000.end")
        font = self.font_size_variable.get()
        x = self.x_variable.get()
        y = self.y_variable.get()
        self.add_text_function(x, y, text, font)
    
    def number_of_cells(self, value):
        # self.number_of_cells_value_label.configure(text="   ")
        # self.number_of_cells_value_label.
        self.number_of_cells_value.set(str(value))
    
    def set_change_visibility_function(self, new_function):
        self.change_visibility_function = new_function
    
    def set_remove_funtion(self, new_function):
        self.remove_function = new_function

    def set_add_text_function(self, new_function):
        self.add_text_function = new_function

    def add_new_layer(self, layer:LayerModel):
        add = None
        if layer.layer_type == "geometry":
            graphic_type = layer.graphic.graphic_name
            if layer.graphic.graphic_type == "complex":
                graphic_type = "draw"
            graphic_name = layer.graphic.graphic_name
            add = LayerInstanceManager(self.layer, graphic_type, f"{graphic_name} {self.layer_id}", self.canvas_width, height=self.layer_height)
        elif layer.layer_type == "image":
            add = LayerInstanceManager(self.layer, "default", f"Image {self.layer_id}", self.canvas_width, height=self.layer_height)
        elif layer.layer_type == "text":
            add = LayerInstanceManager(self.layer, "text", f"Text {self.layer_id}", self.canvas_width, height=self.layer_height)
        if add != None:
            layer_id = self.layer_id
            add.set_remove_function(lambda: self.remove_layer(layer_id, add))
            add.set_change_visibility_function(lambda visibility: self.change_visility(layer, visibility))
            add.pack(side='top')  
        
            self.canvas_width_y_scroll += self.layer_height
            self.layer.configure(scrollregion=(0, 0, self.canvas_width_x_scroll, self.canvas_width_y_scroll))
            self.layers_dict[self.layer_id] = layer
            self.layer_id += 1

    def remove_layer(self, layer_id:int, element:LayerInstanceManager):
        self.canvas_width_y_scroll -= self.layer_height
        self.layer.configure(scrollregion=(0, 0, self.canvas_width_x_scroll, self.canvas_width_y_scroll))
        try:
            element_s = self.layers_dict[layer_id]
            response = self.remove_function(element_s)
            if response == True:
                self.layers_dict.pop(layer_id)
                element.destroy()
        except:
            pass
       
    def change_visility(self, element:LayerModel, visibility:bool) -> (bool):
        try:
            response = self.change_visibility_function(element, visibility)
            return response
        except:
            pass
        return False

    def selected_layer(self):
        pass

    def get_layers(self) -> (List[LayerModel]):
        return self.layers_dict