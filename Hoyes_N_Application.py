import tkinter as tk
from tkinter import *
from tkinter import colorchooser
import math
import turtle as t

#
# Script made for my first programming assignment.
# Draws Spirographs with user input and save slots
# This will be refactored into the project.
#


def draw(big_r, r_ratio, d_ratio, colour): 
    global stop #Should figure out an interrupt solution that doesn't require globals - Could remove now max iteration is dynamic.
    stop = False 


    r = big_r / r_ratio 
    d = r * d_ratio 
    a = 0 
    max_t = 360 
    if not r_ratio.is_integer():
        max_t = max_t * int(round(r_ratio))
    
    print("Doing {} draw iterations.".format(max_t))

    pen.penup()
    pen.color(colour[0])

    draw_list.append((big_r, r_ratio, d_ratio, colour))
    undo_list.append(max_t)

    for i in range(0, max_t): 
        x = (big_r- r) * math.cos((r/ big_r)* a)+ d* math.cos((1- (r/ big_r))* a) 
        y = (big_r- r) * math.sin((r/ big_r)* a)- d* math.sin((1- (r/ big_r))* a) 
        a = a + 0.2
        pen.goto(x,y)
        pen.pendown()
        screen.update()
        if stop == True:
            break
    pen.penup()
    return

def draw_multiple(vars_list):
    pen.clear()
    print("Drawing {} shapes.".format(len(vars_list)))
    for i in vars_list:
        print(i)
        draw(i[0],i[1],i[2],i[3])
    return

def clear():
    global draw_list
    global undo_list
    pen.clear()
    screen.update()
    draw_list = []
    undo_list = []
    print("Screen cleared")
    return

def undo():
    for i in range(0, undo_list[-1]):
        pen.undo()
    print("{} draw iterations undone.".format(undo_list[-1]))
    undo_list.pop(-1)
    draw_list.pop(-1)
    return

def stop():
    global stop
    stop = True
    print("Stop Mr Bones Wild Ride.", stop)
    return

def choose_colour():
    global colour
    colour = (colorchooser.askcolor(title="Choose Colour"))
    if type(colour) == None: #Repeat prompt if colorchooser dialogue closed before a choice is made.
        colour = (colorchooser.askcolor(title="Choose Colour"))
    print("Colour chosen:{}".format(colour[0]))
    return

def save(slot, draw_list, button_id):
    global saved_draws
    saved_draws[slot] = tuple(draw_list)
    print("Saved in slot:{}".format(saved_draws[slot]))
    btn_name = button_id
    btn_name.configure(state = NORMAL)
    return

def delete(slot, button_id):
    global saved_draws
    saved_draws[slot] = None
    btn_name = button_id
    btn_name.configure(state = DISABLED)
    return

stop = False
colour = ((255,0,0),"#ff0000")
undo_list = []
draw_list = []
saved_draws = [None for i in range(0,9)]

#Example multidraw - Renders the single image required for assessment.
example_save = [(400, 2.9, 5.0, ((255, 0, 0),"#ff0000")), 
                (400, 9.9, 0.2, ((125, 13, 130),"#7d0d82")),
                (350, 9.9, 1.0, ((105, 15, 150),"#690f96")),
                (275, 9.9, 1.4, ((63, 16, 150),"#3f1096")),
                (275, 2.9, 1.0, ((11, 21, 155),"#0b159b")),
                (100, 9.9, 1.0, ((7, 61, 158),"#073d9e")),
                (75, 3.9, 1.0, ((4, 122, 162),"#047aa2")),
                (50, 9.9, 0.6, ((0, 255, 255),"#00ffff")),
                (25, 2.1, 0.6, ((0, 255, 255),"#00ffff"))]


window = tk.Tk()
window.title("Spirograph")

canvas = tk.Canvas(highlightbackground = "black", height = 1000, width = 1000)
screen = t.TurtleScreen(canvas)
screen.tracer(0,0)
screen.bgcolor("black")
canvas.grid(row = 0, column = 1, sticky = "NSEW")

window.columnconfigure(1, weight = 1)
window.rowconfigure(0, weight = 1)

frm_inputs = tk.Frame(window)
frm_inputs.grid(column = 0, row = 0)

frm_controls = tk.Frame(frm_inputs) 
frm_controls.grid(column = 0, columnspan = 2, row = 5)

frm_saves = tk.Frame(frm_inputs)
frm_saves.grid(column = 0, columnspan = 2, row = 6)

pen = t.RawTurtle(screen)
pen.hideturtle()
pen.setundobuffer(750000)
screen.colormode(255)

btn_pen_colour= tk.Button(frm_inputs, text= "Pen Colour", command= choose_colour)
btn_pen_colour.grid(row= 1, column= 0)

lbl_big_r= tk.Label(frm_inputs, text = "Radius of large circle, R")
lbl_big_r.grid(row= 2, column= 0)
s_big_r= tk.Scale(frm_inputs, length= 150, from_= 25,to= 400, orient= "horizontal", resolution= 25)
s_big_r.grid(row= 2, column= 1)

lbl_ratio= tk.Label(frm_inputs, text = "Small circle radius as ratio 1:R")
lbl_ratio.grid(row= 3, column= 0)
s_ratio= tk.Scale(frm_inputs, length= 150, from_= 1.5, to= 10, orient="horizontal", resolution=0.1)
s_ratio.grid(row= 3, column= 1)


lbl_distance= tk.Label(frm_inputs, text = "Pen to small circle center distance 1:d")
lbl_distance.grid(row= 4, column= 0)
s_distance= tk.Scale(frm_inputs, length= 150, from_= 0, to= 10, orient="horizontal", resolution=0.2)
s_distance.grid(row= 4, column= 1)

btn_start= tk.Button(frm_controls, text= "Start", command= lambda: draw(s_big_r.get(), s_ratio.get(),s_distance.get(), colour))
btn_start.grid(row= 0, column=0)

btn_stop= tk.Button(frm_controls, text= "Stop", command= stop)
btn_stop.grid(row= 0, column= 1)

btn_undo= tk.Button(frm_controls, text= "Undo", command= undo)
btn_undo.grid(row= 0, column= 2)

btn_clear= tk.Button(frm_controls, text = "Clear", command = clear)
btn_clear.grid(row= 0, column= 3)

#Feature in progress - See def recenter_screen above
#btn_recenter= tk.Button(frm_controls, text = "Recenter")
#btn_recenter.grid(row= 0, column= 3)
#btn_recenter.bind("<Button-1>", recenter_screen)

lbl_programs= tk.Label(frm_controls, text = "Saved sequences", pady = 10)
lbl_programs.grid(row= 1, column= 0, columnspan= 4)

lbl_active_save = tk.Label(frm_controls, text= "Active Slot:")
lbl_active_save.grid(row= 2, column= 0)

spb_active_save = tk.Spinbox(frm_controls, from_= 0, to= 9)
spb_active_save.grid(row= 2, column= 1)

btn_save = tk.Button(frm_controls, text = "Save", command = lambda: save(int(spb_active_save.get()), draw_list,button_list[int(spb_active_save.get())])) 
btn_save.grid(row= 2, column= 2)

btn_delete = tk.Button(frm_controls, text= "Delete", command= lambda: delete(int(spb_active_save.get()), button_list[int(spb_active_save.get())]))
btn_delete.grid(row= 2, column= 3)

btn_preset = tk.Button(frm_saves, text = "Example", command= lambda: draw_multiple(example_save))
btn_preset.grid(row= 0, column= 0)

button_list = [] 
for i in range(0,9): 
    button = tk.Button(frm_saves, text = str(i), command = lambda i=i: draw_multiple(saved_draws[i]), state = DISABLED)
    button.grid(row = 0, column = i + 1)
    button_list.append(button)

lbl_notes = tk.Label(frm_inputs, anchor = "w",
text= 
"If r:R is a whole number a shape with R points will be drawn in a single rotation\n\
Fractional r:R ratios draw complex shapes which resolve over many iterations\n\
The r:d ratio affects 'sharpness' of points. Inversed affects below 1\n\
") 
lbl_notes.grid(row= 8, column= 0, columnspan= 2)

tk.mainloop()
