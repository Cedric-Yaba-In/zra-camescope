from typing import List, Union
from geometricgraphicmodels import Graphic, ImageGraphic, TextGraphic

class LayerModel:
    def __init__(self, item_ids:List[int], layer_type:str, visibility:bool, graphic:Union[Graphic, TextGraphic, ImageGraphic]):
        self.item_ids = item_ids
        self.visibility = visibility
        self.layer_type = layer_type
        self.graphic = graphic