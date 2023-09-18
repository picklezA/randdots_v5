# version: 0.1.5
# author: picklez

import numpy
import random
import math
import time
import tkinter
from PIL import Image,ImageTk
import os
import psutil
import threading

# default settings:
height = 900
width = 1600
dots_defined = 500
cwd = os.getcwd()
start_time = time.time()

class admin_check: # this class allows us to escalate a python program to realtime if it is run in a admin terminal
    def has_admin():
        if os.name == 'nt':
            try:
                # only windows users with admin privileges can read the C:\windows\temp
                temp = os.listdir(os.sep.join([os.environ.get('SystemRoot','C:\\windows'),'temp']))
            except:
                return (os.environ['USERNAME'],False)
            else:
                return (os.environ['USERNAME'],True)
        else:
            if 'SUDO_USER' in os.environ and os.geteuid() == 0:
                return (os.environ['SUDO_USER'],True)
            else:
                return (os.environ['USERNAME'],False)
            
    def has_admin_simply():
        hold = admin_check.has_admin()
        return hold[1]
        
    def this_process_esc():
        if admin_check.has_admin_simply() == True:
            pid = os.getpid()
            process = next((proc for proc in psutil.process_iter() if proc.pid == pid),None)
            process.nice(psutil.REALTIME_PRIORITY_CLASS)

# call this upon run to make sure we are running everything as fast as possible
admin_check.this_process_esc()

class Gen: # short for "Generator"
    def create_random_dots():
        dot_dict = {}
        for i in range(dots_defined):
            dot_dict[i] = Gen.create_random_dot()
        return dot_dict
    
    def create_random_dot():
        new_dot = []
        new_dot.append(random.randrange(1,height-1))
        new_dot.append(random.randrange(1,width-1))
        return new_dot
    
    def next_step(direction_value):
        if direction_value == 0:
            return -1, -1
        if direction_value == 1:
            return -1, 0
        if direction_value == 2:
            return -1, 1
        if direction_value == 3:
            return 0, -1
        if direction_value == 4:
            return 0, 1
        if direction_value == 5:
            return 1, -1
        if direction_value == 6:
            return 1, 0
        if direction_value == 7:
            return 1, 1
    
    def get_random_movement():
        return random.randrange(0,8)
    
    def get_random_dot_movement_dict(dot_dict):
        direction_dict = {}
        for i in range(dots_defined):
            direction_dict[i] = Gen.get_random_movement()
        return direction_dict
    
    def apply_just_dots(img_array, dot_dict):
        for key in dot_dict:
            img_array[dot_dict[key][0]][dot_dict[key][1]][0] = 255
            img_array[dot_dict[key][0]][dot_dict[key][1]][1] = 255
            img_array[dot_dict[key][0]][dot_dict[key][1]][2] = 255
        return img_array
        
    def find_distance(dot1, dot2):
        d_x = abs(dot2[0]) - abs(dot1[0])
        d_y = abs(dot2[1]) - abs(dot1[1])
        distance = math.sqrt((d_x*d_x)+(d_y*d_y))
        return round(distance, 2)
        
    def get_nearest_dots(dot_dict):
        nearest = {}
        for key in dot_dict:
            sub_nearest = {}
            sub_dot_array = dot_dict.copy()
            sub_dot_array.pop(key)
            for key2 in sub_dot_array:
                distance = Gen.find_distance(dot_dict[key], sub_dot_array[key2])
                sub_nearest[distance] = key2
            to_add = []
            count = 0
            for key3 in sorted(sub_nearest):
                to_add.append(sub_nearest[key3])
                count += 1
                if count == 9:
                    break
            nearest[key] = to_add
        return nearest
        
    def draw_lines(new_image, random_dots_dict, nearest):
        for key in nearest:
            for point in nearest[key]:
                r_or_b = random.randrange(0,2)
                line_array = Gen.line(random_dots_dict[key], random_dots_dict[point])
                for point2 in line_array:
                    if r_or_b == 0:
                        new_image[point2[0]][point2[1]][0] = 255
                        new_image[point2[0]][point2[1]][1] = 0
                        new_image[point2[0]][point2[1]][2] = 0
                    if r_or_b == 1:
                        new_image[point2[0]][point2[1]][0] = 0
                        new_image[point2[0]][point2[1]][1] = 0
                        new_image[point2[0]][point2[1]][2] = 255
        return new_image
        
    def line(point1, point2):
        all_points_between = []
        dtop = point2[0] - point1[0]
        dbot = point2[1] - point1[1]
        m = dtop / (dbot + 0.0000000000000001)
        b = point1[0] - (m * point1[1])
        if point1[1] < point2[1]:
            for i in range(point1[1], point2[1]):
                hy = (m*i)+b
                hy = round(hy, 2)
                hy = math.trunc(hy)
                hold = [int(hy), int(i)]
                all_points_between.append(hold)
            if point1[0] < point2[0]:
                for j in range(point1[0], point2[0]):
                    hx = (j-b)/m
                    hx = round(hx, 2)
                    hx = math.trunc(hx)
                    hold = [int(j), int(hx)]
                    all_points_between.append(hold)
            if point1[0] > point2[0]:
                for j in range(point2[0], point1[0]):
                    hx = (j-b)/m
                    hx = round(hx, 2)
                    hx = math.trunc(hx)
                    hold = [int(j), int(hx)]
                    all_points_between.append(hold)
        if point1[1] > point2[1]:
            for i in range(point2[1],point1[1]):
                hy = (m*i)+b
                hy = math.trunc(hy)
                hold = [int(hy), int(i)]
                all_points_between.append(hold)
            if point1[0] < point2[0]:
                for j in range(point1[0], point2[0]):
                    hx = (j-b)/m
                    hx = round(hx, 2)
                    hx = math.trunc(hx)
                    hold = [int(j), int(hx)]
                    all_points_between.append(hold)
            if point1[0] > point2[0]:
                for j in range(point2[0], point1[0]):
                    hx = (j-b)/m
                    hx = round(hx, 2)
                    hx = math.trunc(hx)
                    hold = [int(j), int(hx)]
                    all_points_between.append(hold)
        return all_points_between

def next_step_new_array(dot_array, direction_dict):
    to_remove = []
    for key in dot_array:
        direction = direction_dict[key]
        current_dot = dot_array[key]
        next_move = Gen.next_step(direction)
        if current_dot[0]+1 != 0 and current_dot[0]+1 != height and current_dot[1]+1 != 0 and current_dot[1]+1 != width:
            current_dot[0] = current_dot[0] + next_move[0]
            current_dot[1] = current_dot[1] + next_move[1]
            dot_array[key] = current_dot
        elif current_dot[0]+1 == 0 or current_dot[0]+1 == height or current_dot[1]+1 == 0 or current_dot[1]+1 == width:
            to_remove.append(key)
    for i in to_remove:
        dot_array[i] = Gen.create_random_dot()
        direction_dict[i] = Gen.get_random_movement()
    return dot_array

def create_image(ni):
    da = Gen.create_random_dots()
    ndm = Gen.get_nearest_dots(da)
    ni = Gen.draw_lines(ni, da, ndm)
    ni = Gen.apply_just_dots(ni, da)
    dd = Gen.get_random_dot_movement_dict(da)
    dans = next_step_new_array(da, dd)
    return ni, dd, dans

def move_image(bi, da, dd):
    bi = Gen.apply_just_dots(bi, da)
    ndm = Gen.get_nearest_dots(da)
    bi = Gen.draw_lines(bi, da, ndm)
    dans = next_step_new_array(da, dd)
    return bi, dd, dans
    
def window_on_run(imgs):
    window = tkinter.Tk()
    window.title("Python GUI APP")
    window.configure(width=width,height=height)
    window.configure(bg='black')
    winWidth = window.winfo_reqwidth()
    winHeight = window.winfo_reqheight()
    posRight = int(window.winfo_screenwidth() / 2 - winWidth /2)
    posDown = int(window.winfo_screenheight() / 2 - winHeight / 2)
    window.geometry("+{}+{}".format(posRight, posDown))
    
    canvas = tkinter.Canvas(window)
    canvas = tkinter.Canvas(window, width=width, height=height)
    canvas.pack()
    
    while True:
        for i in range(len(imgs)):
            img2 = ImageTk.PhotoImage(image=Image.fromarray((imgs[i].copy()).astype(numpy.uint8)))
            canvas.create_image(0, 0, anchor=tkinter.NW, image=img2)
            canvas.update()
            time.sleep(.1)
    
    window.mainloop()

class dual:
    all_images = []
    new_image = numpy.empty((height,width,3))
    blank_image = new_image.copy()
    new_image, direction_dict, dot_array_next_step = create_image(new_image)
    
    def window_on_run():
        admin_check.this_process_esc()
        window = tkinter.Tk()
        window.title("Python GUI APP")
        window.configure(width=width,height=height)
        window.configure(bg='black')
        winWidth = window.winfo_reqwidth()
        winHeight = window.winfo_reqheight()
        posRight = int(window.winfo_screenwidth() / 2 - winWidth /2)
        posDown = int(window.winfo_screenheight() / 2 - winHeight / 2)
        window.geometry("+{}+{}".format(posRight, posDown))
        
        canvas = tkinter.Canvas(window)
        canvas = tkinter.Canvas(window, width=width, height=height)
        canvas.pack()
        
        while True:
            print(len(dual.all_images))
            for i in range(len(dual.all_images)):
                img2 = ImageTk.PhotoImage(image=Image.fromarray((dual.all_images[i].copy()).astype(numpy.uint8)))
                canvas.create_image(0, 0, anchor=tkinter.NW, image=img2)
                canvas.update()
        
        window.mainloop()
        
    def generate_more():
        admin_check.this_process_esc()
        while len(dual.all_images) < 5001:
            dual.new_image_2, dual.direction_dict, dual.dot_array_next_step = move_image(dual.blank_image.copy(), dual.dot_array_next_step, dual.direction_dict)
            dual.all_images.append(dual.new_image_2.copy().astype(numpy.uint8))
            
    def spawn_threads():
        thread1 = threading.Thread(target=dual.window_on_run,args=())
        thread1.start()
        
        thread2 = threading.Thread(target=dual.generate_more,args=())
        thread2.start()
        
        thread1.join()
        thread2.join()

dual.spawn_threads()