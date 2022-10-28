from typing import Callable

class CustomButtonModel:
    def __init__(self, default_image_path:str, active_image_path:str, second_image_path:str=None, command:Callable=None) -> None:
        self.default_image_path = default_image_path
        self.active_image_path = active_image_path
        self.second_image_path = second_image_path
        self.commad = command