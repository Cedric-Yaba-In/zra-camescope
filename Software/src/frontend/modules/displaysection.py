import os
import threading
import time
import tkinter as ttk
from tkinter.tix import WINDOW
from turtle import width
from typing import Callable, Dict, List
from PIL import Image, ImageTk
import cv2
from pathlib import Path
from cells_counter import cells_counter

from colors import BACKGROUND_COLOR_1, BACKGROUND_COLOR_2, BORDER_COLOR, TEXT_COLOR, TOOLS_BAR_COLOR
from configs import APP_DIR, APP_NAME, DIR_IMAGE, DIR_VIDEO
from camera import MyVideoCapture
from geometricgraphicmodels import ComplexGraphic, Graphic, Point, SimpleGraphic, TextGraphic
from graduatebar import GraduateBar
from layer_model import LayerModel

home = str(Path.home())
Path(os.path.join(home, APP_DIR)).mkdir(parents=True, exist_ok=True)  
Path(os.path.join(home, APP_DIR, DIR_IMAGE)).mkdir(parents=True, exist_ok=True)  
Path(os.path.join(home, APP_DIR, DIR_VIDEO)).mkdir(parents=True, exist_ok=True)


class DisplaySection(ttk.Frame):
    ELLIPS = "ellips"
    LINE = "line"
    IMAGE = "image"
    TEXT = "text"
    WINDOW = "window"
    RECTANGLE = "rectangle"
    FREE = "free"
    POLYGON = "polygon"
    GEOMETRY = "geometry"

    def __init__(self, master:object, menu_items: List[object], language:str, width:int, height:int, background:str=TOOLS_BAR_COLOR, copyright:str=""):
        ttk.Frame.__init__(self, master = master, width = width, height = height, background=background, borderwidth=0)
        self.master = master
        footer_height = 30
        frame_width = width
        frame_height = (height - footer_height)

        frame = ttk.Frame(self, width=frame_width, height=frame_height,  background=background)
        frame.pack(side="top")

        schrool_bar_width = 12
        graduatebar_width = 20
        self.canvas_width = frame_width - 2*graduatebar_width
        self.canvas_height = frame_height - 2*graduatebar_width
        self.image_width = self.canvas_width
        self.image_height = self.canvas_height
        
        conner0 = GraduateBar(frame, width=graduatebar_width, height=graduatebar_width, orient="horizontal")
        conner0.grid(row=0, column=0)

        self.x_bar = GraduateBar(frame, width=self.canvas_width, height=graduatebar_width, orient="horizontal")
        self.x_bar.grid(row=0, column=1)

        conner1 = GraduateBar(frame, width=graduatebar_width, height=graduatebar_width, orient="horizontal")
        conner1.grid(row=0, column=2)

        self.y_bar = GraduateBar(frame, width=graduatebar_width, height=self.canvas_height, orient="vertical")
        self.y_bar.grid(row=1, column=0)

        self.canvas = ttk.Canvas(
            frame, width = self.canvas_width, 
            height=self.canvas_height, 
            background=background, 
            highlightthickness=0, 
            bd=0
        )
        self.canvas.grid(row=1, column=1, sticky="nw")
        self.canvas.bind("<Motion>", func = lambda event: self.set_pos(event.x, event.y), add="+")
        self.canvas.bind("<Button-1>", func = self.on_canvas_click, add="+")

        y_schrool = ttk.Scrollbar(frame, bg='black',  orient='vertical', width=schrool_bar_width, command=self.move_y_scroll_bar)
        y_schrool.grid(row=1, column=2, sticky="ns")

        conner2 = GraduateBar(frame, width=graduatebar_width, height=graduatebar_width, orient="horizontal")
        conner2.grid(row=2, column=0)

        x_schrool = ttk.Scrollbar(frame, bg = "black", orient='horizontal', width=schrool_bar_width, command=self.move_x_scroll_bar)
        x_schrool.grid(row=2, column=1, sticky="ew")

        conner3 = GraduateBar(frame, width=graduatebar_width, height=graduatebar_width, orient="horizontal")
        conner3.grid(row=2, column=2)

        self.canvas["xscrollcommand"] = x_schrool.set
        self.canvas["yscrollcommand"] = y_schrool.set

        footer = ttk.Canvas(
            self, width = width, 
            height=footer_height, background=BACKGROUND_COLOR_1, 
            highlightcolor=BORDER_COLOR, highlightbackground=BORDER_COLOR, 
            bd=1, highlightthickness=1
        )
        footer.pack(side="top")


        self.width_coord_frame = 200
        width_copyright_frame = width - self.width_coord_frame
        self.font_size_coord = 9
        font_size_copyright = 11
        dx = 20
        position_copyright = self.width_coord_frame + dx + (width_copyright_frame - len(copyright)*(font_size_copyright - 4))//2 
    

        footer.create_line(self.width_coord_frame, 0, self.width_coord_frame, footer_height, fill=BORDER_COLOR)    
    
        self.text_coord =ttk.Label(footer, text="", font=("Arial", self.font_size_coord), background=BACKGROUND_COLOR_1, foreground=TEXT_COLOR)
        self.text_coord.place(x = width_copyright_frame//2 + 10, y = 5)

        ttk.Label(
            footer, text = copyright, font=("Segeo UI", font_size_copyright), 
            foreground=TEXT_COLOR, background=BACKGROUND_COLOR_1
            ).place(x = position_copyright , y = 2)
        
        self.is_record = False
        self.is_paused = False
        self.is_playing = True
        self.is_stopped = False
        self.image_id = None

        self.x_schroll_factor = 0
        self.y_schroll_factor = 0

        self.str_time = ""

        self.fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        self.FPS = 25

        self.simple_graphic = SimpleGraphic()
        self.complex_graphic = ComplexGraphic()
        self.graphics:List[LayerModel] = []
        #---- event
        self.cursor_is_pressed = False

        self.item_type = ""
        self.geometry_type = ""
        self.start_drawing = False
        self.is_drawing = False
        self.fill_color = ""
        self.outline_color = "gold"
        self.cursor_x = None
        self.cursor_y = None
        self.font_size = 15
        self.font_weight = 'normal'
        
        self.drawing_items_ids = []
        self.crop_rects_ids = []

        self.repere_y_line_id = None
        self.repere_x_line_id = None
        self.text_id = None

        self.allow_count_cells = False
        
        self.drawing_functions = {
            self.IMAGE: self.canvas.create_image,
            self.ELLIPS: self.canvas.create_oval,
            self.LINE: self.canvas.create_line,
            self.RECTANGLE: self.canvas.create_rectangle,
            self.FREE: self.canvas.create_line,
            self.WINDOW: self.canvas.create_window,
            self.TEXT: self.canvas.create_text,
            self.POLYGON: self.canvas.create_polygon
            }
        
        self.display_count_cells_result_function = lambda number_of_cells:None 
        self.add_layer_function = lambda new_layer:None

        # print("number iof processor", cv2.getNumberOfCPUs())
        self.elements_to_display:List[LayerModel] = []
        self.thread_lock = threading.RLock()

        self.add_text_mode = False
        self.text_object = None
        self.text_editor_x = None
        self.text_editor_y = None

    def set_font_size(self, new_size:int):
        self.font_size = new_size
    
    def set_font_weight(self, new_weight:str):
        self.font_weight = new_weight

    def move_x_scroll_bar(self, *args):
        self.canvas.xview(*args)
        self.x_schroll_factor = float(args[1])

        if self.text_id != None:
            self.canvas.delete(self.text_id)
        x = self.canvas_width - 100
        y = 20
        x += self.x_schroll_factor * self.image_width
        y += self.y_schroll_factor * self.image_height
        self.text_id = self.canvas.create_text(x, y, text = f"Recorder  {self.str_time}", font=("Segeo UI", 14, "bold"), fill=TEXT_COLOR)
                        
    def move_y_scroll_bar(self, *args):
        self.canvas.yview(*args)
        self.y_schroll_factor = float(args[1])

        if self.text_id != None:
            self.canvas.delete(self.text_id)
        x = self.canvas_width - 100
        y = 20
        x += self.x_schroll_factor * self.image_width
        y += self.y_schroll_factor * self.image_height
        self.text_id = self.canvas.create_text(x, y, text = f"Recorder  {self.str_time}", font=("Segeo UI", 14, "bold"), fill=TEXT_COLOR)

    def stop(self, event=None):
        self.is_paused = False
        self.is_playing = False
        self.is_stopped = True
        self.is_record = False

        children = self.canvas.find_all()
        for tag_orid in children:
            self.canvas.delete(tag_orid) 
        self.add_text_mode = False
        self.is_drawing = False
        self.start_drawing = False
    
    def play(self, event=None):
        self.is_paused = False
        self.is_playing = True
        self.is_stopped = False
    
    def pause(self, event=None):
        self.is_paused = not self.is_paused

    def draw_image(self, camera:MyVideoCapture):
        if self.is_playing == True and self.is_paused == False:
            ret, self.frame = camera.get_frame()
            frame = cv2.resize(self.frame, (self.image_width, self.image_height))
            if self.image_id != None:
                self.canvas.delete(self.image_id)

            if ret:
                self.photo = ImageTk.PhotoImage(image = Image.fromarray(frame, "RGB"))
                self.image_id = self.canvas.create_image(0, 0, image = self.photo, anchor = ttk.NW)

            children = list(self.canvas.find_all())
            tag_orid = children.pop()
            tag_orids:Dict[int, bool] = {}
            for element in self.graphics:
                if element.visibility == True:
                    for item_id in element.item_ids:
                        tag_orids[item_id] = True

            while children:
                new_tag_orid = children.pop()
                if tag_orids.get(new_tag_orid, "-1") != -1:    
                    self.canvas.tag_raise(new_tag_orid, tag_orid)
                elif new_tag_orid in [self.image_id, self.repere_x_line_id, self.repere_y_line_id, self.text_id]:
                    self.canvas.tag_raise(new_tag_orid, tag_orid)
                tag_orid = new_tag_orid

        self.master.after(10, lambda: self.draw_image(camera))
    
    def capture_image(self, event=None):
        name = APP_NAME + "-" + time.strftime("%d-%m-%Y-%H-%M-%S") + ".jpg"
        path = os.path.join(str(Path.home()), APP_DIR, DIR_IMAGE, name)
        cv2.imwrite(path, cv2.cvtColor(self.frame, cv2.COLOR_RGB2BGR))       
    
    def capture_video(self, event=None):
        name = APP_NAME + "-" + time.strftime("%d-%m-%Y-%H-%M-%S") + ".mp4"
        path = os.path.join(str(Path.home()), APP_DIR, DIR_VIDEO, name)
        
        if self.is_record == False:
            self.is_record = True
            out = cv2.VideoWriter(path, self.fourcc, self.FPS, (640, 480))
            def timer():
                two_digits = lambda n : (("0" if n < 10 else "") + str(n))
                counter = 0
                while self.is_record and self.is_playing == True:
                    if self.is_paused == False:
                        minutes = counter // 60
                        seconds = counter  % 60
                        self.str_time = f"{two_digits(minutes)}:{two_digits(seconds)}"
                        if self.text_id != None:
                            self.canvas.delete(self.text_id)
                        x = self.canvas_width - 100
                        y = 20
                        x += self.x_schroll_factor * self.image_width
                        y += self.y_schroll_factor * self.image_height
                        self.text_id = self.canvas.create_text(x, y, text = f"Recorder  {self.str_time}", font=("Segeo UI", 14, "bold"), fill=TEXT_COLOR)
                        counter += 1
                        time.sleep(1)

            def write_video():
                while self.is_record and self.is_playing == True:
                    frame =  cv2.cvtColor(self.frame, cv2.COLOR_RGB2BGR)
                    out.write(frame)
                    time.sleep(1/self.FPS) 
                out.release()
                    

            thread1 = threading.Thread(target=timer)
            thread2 = threading.Thread(target=write_video)
            
            thread1.daemon = True
            thread2.daemon = True
            
            thread1.start()
            thread2.start()
        else:
            self.is_record = False
            if self.text_id != None:
                self.canvas.delete(self.text_id)
    
    def set_count_cells_result_function(self, new_function:Callable):
        self.display_count_cells_result_function = new_function

    def set_add_layer_function(self, new_function:Callable):
        self.add_layer_function = new_function

    def start_count_cells(self, frame, x, y, width, height):
        with self.thread_lock:
            crop_frame = frame[y:y+height, x:x+width]
            ans = cells_counter(crop_frame)
            try:
                self.display_count_cells_result_function(ans)
            except Exception as error:
                print('An error occured when setting counted celles ', error)

    def count_cells(self, event=None):
        # if self.start_drawing == False:
        #     self.allow_count_cells = True
        #     self.start_drawing = True
        #     self.item_type = self.RECTANGLE
        #     self.geometry_type = "simple"
        # else:
        #     self.allow_count_cells = False
        #     self.start_drawing = False
        #     if self.repere_x_line_id != None:
        #         self.canvas.delete(self.repere_x_line_id)
        #     if self.repere_y_line_id != None:
        #         self.canvas.delete(self.repere_y_line_id)
            
        #     while self.crop_rects_ids:
        #         self.canvas.delete(self.crop_rects_ids.pop())
        # # Do something here
        image = Image.fromarray(self.frame)
        thread = threading.Thread(target=self.start_count_cells, args=(cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB), 0, 0, image.width, image.height))
        thread.daemon = True
        thread.start()
        

    def add_text(self, x, y, text, font, position=None):
        font=int(str(font).strip())
        item_id = self.canvas.create_text(x, y, fill = self.outline_color, font=("Segeo UI", font), text=text)

        self.graphics.append(
            LayerModel(
                item_ids = [item_id], 
                layer_type = self.TEXT,
                visibility = True, 
                graphic = TextGraphic (
                    text = text,
                    coord = Point(x, y),
                    foreground = self.outline_color,
                )
            )
        )

    def add_text_entry(self, position=None):
        if self.start_drawing == False:
            if self.add_text_mode == False:
                self.add_text_mode = True
                self.start_drawing = True
            else:
                self.add_text_mode = False
                if self.text_object != None:
                    text = self.text_object.get("1.0", "1000.end")
                    item_id = self.canvas.create_text(
                        self.text_editor_x, 
                        self.text_editor_y, 
                        fill = self.outline_color, 
                        font=("Segeo UI", self.font_size), 
                        text=text
                    )

                    self.graphics.append(
                        LayerModel(
                                item_ids = [item_id], 
                                layer_type = self.TEXT,
                                visibility = True, 
                                graphic = TextGraphic (
                                    text = text,
                                    coord = Point(self.text_editor_x+5, self.text_editor_y+5),
                                    foreground = self.outline_color,
                                )
                            )
                    )
                    self.add_layer(self.graphics[-1])
                    # Draw text in canvas at the given position

    def draw_line(self, event=None):
        if(self.add_text_mode == False):
            if self.start_drawing == False:
                self.start_drawing = True
                self.item_type = self.LINE
                self.geometry_type = "simple"
            else:
                self.start_drawing = False
                if self.repere_x_line_id != None:
                    self.canvas.delete(self.repere_x_line_id)
                if self.repere_y_line_id != None:
                    self.canvas.delete(self.repere_y_line_id)

    def draw_rectangle(self, event=None,  position=None):
        if(self.add_text_mode == False):
            if self.start_drawing == False:
                self.start_drawing = True
                self.item_type = self.RECTANGLE
                self.geometry_type = "simple"
            else:
                self.start_drawing = False
                if self.repere_x_line_id != None:
                    self.canvas.delete(self.repere_x_line_id)
                if self.repere_y_line_id != None:
                    self.canvas.delete(self.repere_y_line_id)

    def draw_ellips(self, event=None,  position=None):
        if(self.add_text_mode == False):
            if self.start_drawing == False:
                self.start_drawing = True
                self.item_type = self.ELLIPS
                self.geometry_type = "simple"
            else:
                self.start_drawing = False
                if self.repere_x_line_id != None:
                    self.canvas.delete(self.repere_x_line_id)
                if self.repere_y_line_id != None:
                    self.canvas.delete(self.repere_y_line_id)
    
    def free_draw(self, event=None, position=None):
        if(self.add_text_mode == False):
            if self.start_drawing == False:
                self.start_drawing = True
                self.item_type = self.FREE
                self.geometry_type = "complex"
            else:
                self.start_drawing = False
                if self.repere_x_line_id != None:
                    self.canvas.delete(self.repere_x_line_id)
                if self.repere_y_line_id != None:
                    self.canvas.delete(self.repere_y_line_id)
    
    def zoom_in(self, event=None,  increase_value = 100):
        self.image_width += increase_value
        self.image_height += increase_value

        try:
            self.canvas.create_image(0, 0, image = self.photo, anchor = ttk.NW)
            scrollregion = (
                0, 
                0, 
                max(self.canvas_width, self.image_width), 
                max(self.canvas_height, self.image_height)
            )
            self.canvas.configure(scrollregion=scrollregion)
        except Exception:
            pass

    def zoom_out(self, event=None,  reduce_value=100):
        self.image_width -= reduce_value
        self.image_height -=  reduce_value

        try:
            self.canvas.create_image(max(0, (self.canvas_width - self.image_width)//2), max(0, (self.canvas_height - self.image_height)//4), image = self.photo, anchor = ttk.NW)
            scrollregion = (
                0,
                0,
                max(self.canvas_width, self.image_width), 
                max(self.canvas_height, self.image_height)
            )
            self.canvas.configure(scrollregion=scrollregion)
        except Exception:
            pass
    
    def zoom_zoom(self, event=None,  increase_by=100):
        # zoom where the pointer is currently positioned
        self.image_width += increase_by
        self.image_height += increase_by

        try:
            self.canvas.create_image(0, 0, image = self.photo, anchor = ttk.NW)
            scrollregion = (
                0, 
                0, 
                max(self.canvas_width, self.image_width), 
                max(self.canvas_height, self.image_height)
            )
            self.canvas.configure(scrollregion=scrollregion)
        except Exception:
            pass

    def zoom_to_fit(self, event=None):
        #change the cursor to allow user to draw rectangle where we want to zoom and do the same thing as expand
        print('To fit')

    def zoom_expand(self, event=None):
        # get all position of selected item and find the square that contain all those items
        #zoom on this item by indicated the x, y, x + width, y + height
        #with is the max between self.canvas_width and the overlooped square
        #samething for height
        print('Expand')

    def zoom_collapse(self, event=None):
        self.image_width = self.canvas_width
        self.image_height = self.canvas_height

        try:
            self.canvas.create_image(0, 0, image = self.photo, anchor = ttk.NW)
            scrollregion = (
                0, 
                0, 
                max(self.canvas_width, self.image_width), 
                max(self.canvas_height, self.image_height)
            )
            self.canvas.configure(scrollregion=scrollregion)
        except Exception:
            pass

    def set_pos(self, x:int=0, y:int = 0, unit=""):
        self.text_coord.configure(text="                ")
        
        self.text_coord.configure(text=f"x={x} {unit}, y={y}  {unit}")
        self.cursor_x = x
        self.cursor_y = y
        position = self.width_coord_frame - self.font_size_coord * (len(f"x={x} {unit}, y={y}  {unit}") - 4)
        position = position // 2
        self.text_coord.place(x = position)

        if self.start_drawing == True:
            if self.repere_x_line_id != None:
                self.canvas.delete(self.repere_x_line_id)
            if self.repere_y_line_id != None:
                self.canvas.delete(self.repere_y_line_id)

            self.repere_x_line_id = self.canvas.create_line(
                0, self.cursor_y, max(self.canvas_width, self.image_width), self.cursor_y, 
                fill="white", dash=(30, 100, 15, 100), width=1
            )

            self.repere_y_line_id = self.canvas.create_line(
                self.cursor_x, 0, self.cursor_x, max(self.canvas_height, self.image_height), 
                fill="white", dash=(30, 100, 15, 100), width=1
            )
        if self.start_drawing == True:
            pass

    
    def draw_element(self, type:str, x1:float, y1:float, x2:float, y2:float, color:str) -> (int):
        return self.drawing_functions[type](x1, y1, x2, y2, fill=color)
    
    def live_drawing(self):
        while self.cursor_is_pressed and self.is_drawing == True and (self.simple_graphic.start.x != None or self.complex_graphic.points):
            #Remove all current graphic drawed items in canvas
            if self.drawing_items_ids:
                for item_id in self.drawing_items_ids: 
                    self.canvas.delete(item_id)
            if self.geometry_type == "simple":
                try:
                    item = self.drawing_functions[self.item_type](
                            self.simple_graphic.start.x, 
                            self.simple_graphic.start.y, 
                            self.cursor_x, self.cursor_y, 
                            outline=self.simple_graphic.outline_color,
                            fill = self.simple_graphic.fill_color, 
                            width = 2
                        )
                except:
                    item = self.drawing_functions[self.item_type](
                            self.simple_graphic.start.x, 
                            self.simple_graphic.start.y, 
                            self.cursor_x, self.cursor_y,
                            fill = self.simple_graphic.outline_color, 
                            width = 2
                        )
                self.drawing_items_ids.append(item)
            elif self.geometry_type == "complex":
                size = len(self.complex_graphic.points)
                prev_point = self.complex_graphic.points[0]
                for i in range(1, size):
                    current_point = prev_point = self.complex_graphic.points[i]
                    self.drawing_items_ids.append(
                    self.drawing_functions[self.item_type](
                        prev_point.x, prev_point.y, 
                        current_point.x, current_point.y,
                        fill=self.complex_graphic.outline_color,
                        width = 2
                        )
                    )
                    prev_point = current_point

                self.drawing_items_ids.append(
                    self.drawing_functions[self.item_type](
                        prev_point.x, prev_point.y, 
                        self.cursor_x, self.cursor_y,
                        fill=self.complex_graphic.outline_color,
                        width = 2
                        )
                    )
                self.complex_graphic.points.append(Point(self.cursor_x, self.cursor_y))
        
        ids = [item_id for item_id in self.drawing_items_ids]
        self.graphics.append(
            LayerModel(
                item_ids = ids, 
                layer_type = self.GEOMETRY,
                visibility = True, 
                graphic = Graphic(
                    graphic_object=(self.complex_graphic if self.geometry_type == "complex" else self.simple_graphic), 
                    graphic_type=self.geometry_type, 
                    graphic_name=self.item_type
                )
            )
        )

        # if  self.allow_count_cells and self.item_type == self.RECTANGLE:
        #     for item_id in self.drawing_items_ids:
        #         self.crop_rects_ids.append(item_id)
        #     width = abs(self.simple_graphic.start.x - self.simple_graphic.end.x)
        #     height = abs(self.simple_graphic.start.y - self.simple_graphic.end.y)
        #     x = min(self.simple_graphic.start.x, self.simple_graphic.end.x)
        #     y = min(self.simple_graphic.start.y, self.simple_graphic.end.y)
        #     thread = threading.Thread(target=self.start_count_cells, args=(self.frame, x, y, width, height))
        #     thread.daemon = True
        #     thread.start()
        self.add_layer(self.graphics[-1])

        self.simple_graphic.start = Point()
        self.complex_graphic = ComplexGraphic()
        while self.drawing_items_ids:
            self.drawing_items_ids.pop()

    def add_layer(self, layer:LayerModel):
        if not self.allow_count_cells:
            try:
                self.add_layer_function(layer)
            except Exception as error:
                print("An errocured when setting layer to add", error)
                    
    def draw_geometry(self, x, y):     
        if self.start_drawing == True and self.add_text_mode==False:
            if self.geometry_type == "simple":
                if self.simple_graphic.start.x == None:
                    self.simple_graphic.start.x = x
                    self.simple_graphic.start.y = y
                    self.simple_graphic.outline_color = self.outline_color
                    self.simple_graphic.fill_color = self.fill_color
                    self.is_drawing = True
                else:
                    self.simple_graphic.end.x = x
                    self.simple_graphic.end.y = y
                    self.is_drawing = False
            elif self.geometry_type == "complex":
                if len(self.complex_graphic.points) == 0:
                    self.complex_graphic.outline_color = self.outline_color
                    self.complex_graphic.fill_color = self.fill_color
                    self.complex_graphic.points.append(Point(x, y))
                    self.is_drawing = True
                else:
                    self.is_drawing = False
        
            if self.cursor_is_pressed == False:
                self.cursor_is_pressed = True
                draw_thread = threading.Thread(target=self.live_drawing)
                draw_thread.daemon = True
                draw_thread.start()
            else:
                self.cursor_is_pressed = False
                self.drawing_items_ids = []

    def text_editor(self, x, y):
        if self.add_text_mode == True:
            if self.start_drawing == True:
                self.start_drawing = False
            x_pos = x
            y_pox = y
            self.text_editor_x = x
            self.text_editor_y = y
            def draw_editor():
                self.text_object = ttk.Text(
                        self.canvas,
                        font = ("Segeo UI", 12),
                        width = 30,
                        height = 10,
                        highlightthickness = 1,
                        highlightbackground = BORDER_COLOR,
                        highlightcolor = BORDER_COLOR,
                        relief = "flat",
                        foreground = TEXT_COLOR,
                        background = "#3D3D3D",
                )
                self.text_object.place(x = x_pos, y=y_pox)
                while self.add_text_mode == True:   
                    self.text_object.focus_force()
                self.text_object.destroy()
            thread = threading.Thread(target=draw_editor)
            thread.daemon = True
            thread.start()

            if self.repere_x_line_id != None:
                self.canvas.delete(self.repere_x_line_id)
            if self.repere_y_line_id != None:
                self.canvas.delete(self.repere_y_line_id)

    def on_canvas_click(self, event):
        self.draw_geometry(event.x, event.y)
        self.text_editor(event.x, event.y)

    def change_visibility(self, element:LayerModel, visibility:bool=True) -> (bool):
        for in_element in self.graphics:
            if element == in_element:
                in_element.visibility = visibility
                
                if visibility == False:
                    for item_id in element.item_ids:
                        self.canvas.delete(item_id)
                return True
        return False

    def remove_element(self, element:LayerModel) -> (bool):
        try:
            self.graphics.remove(element)
            for item_id in element.item_ids:
                self.canvas.delete(item_id)
            return True
        except:
            return False