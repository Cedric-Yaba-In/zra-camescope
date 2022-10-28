from typing import List, Union


class Point:
    x:float = None
    y:float = None

    def __init__(self, x:float=None, y:float=None) -> None:
        self.x = x
        self.y = y


class SimpleGraphic:
    start:Point = Point()
    end: Point = Point()
    outline_color:str = ""
    fill_color:str = ""


class ComplexGraphic:
    points:List[Point] = []
    outline_color:str = ""
    fill_color:str = ""


class TextGraphic:
    def __init__(
        self, 
        text:str, 
        coord:Point, 
        font_weight:str="normal",
        style = [],
        foreground:str = None,
        background:str=None,
        outline:str=None,
        outline_width:int = 0
        ):

        self.text = text
        self.coord = coord
        self.foreground = foreground
        self.background = background
        self.outline = outline
        self.outline_width = outline_width


class ImageGraphic:
    def __init__(self, path:str, coord:Point, width:float, height:float):
        self.path = path
        self.coord = coord
        self.width = width
        self.height = height


class Graphic:
    def __init__(self, graphic_object:Union[SimpleGraphic, ComplexGraphic] = None, graphic_type:str = None, graphic_name:str = None) -> None:
        self.graphic_object:Union[SimpleGraphic, ComplexGraphic,None] = graphic_object
        self.graphic_type:str = graphic_type
        self.graphic_name:str = graphic_name

