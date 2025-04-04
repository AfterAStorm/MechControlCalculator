
import tkinter as tk
import tkinter.font as tkf

from time import time

from calculate import Calculator
from solver import ik2d, LegAngles, findKnee
from math import degrees, sin, cos
from legs import Leg
from expressions import Expression

window = tk.Tk()
window.title('wouldn\'t you like to know!')
window.attributes('-topmost', 'true')

canvas = tk.Canvas(window, width=800, height=800, background='#000000', borderwidth=0, highlightthickness=0)
canvas.pack()

font = tkf.Font(family='Courier New', size=10)

labels = [
    canvas.create_text(10, 10+5, text='a', font=font, fill='#fff', anchor='w'),
    canvas.create_text(10, 30+5, text='b', font=font, fill='#fff', anchor='w'),
    canvas.create_text(10, 50+5, text='c', font=font, fill='#fff', anchor='w'),
]

window.minsize(800, 800)
window.maxsize(800, 800)

#window.mainloop()

calc = Calculator()
lengths = [1, 1]

legs = []
def create_legs(joints):
    legs.clear()
    for i in range(2):
        legs.append(Leg(canvas, joints, (i + 1) / 2))

create_legs(2)

canvas.create_text(50 - 2, 640, text='Joints', font=font, fill='#fff', anchor='ne', justify='right'),
num_legs_var = tk.IntVar(window)
num_legs_var.set(2)
num_legs = tk.Entry(window, width=2, textvariable=num_legs_var)
num_legs.place(x=50, y=640)

length_entry = []

for i in range(2):
    var = tk.DoubleVar(window)
    var.set(1)
    entry = tk.Entry(window, width=4, textvariable=var)
    entry.place(x=90 + i * 30, y=640)
    length_entry.append((entry, var))

expressions = [
    (50, 680, 'X', '-sin(dt*2*pi) * -0.5'),#'-2 + dt * 4'), # sin(dt*2*pi) * -0.5
    (50, 700, 'Y', 'max(cos(dt*2*pi),0) * -0.5 + 1.5'), # max(cos(dt*2*pi),0) * -0.5 + 1.5
    (50, 720, 'Z', '0'), # 0
]

from rtf import RTFText

for i in range(len(expressions)):
    var = tk.StringVar(window)
    canvas.create_text(expressions[i][0] - 2, expressions[i][1], text=expressions[i][2], font=font, fill='#fff', anchor='ne', justify='right'),
    error = canvas.create_text(expressions[i][0] + 310 - 2, expressions[i][1], text='', font=font, fill='#f00', anchor='nw', justify='left'),
    entry = tk.Entry(window, textvariable=var, foreground='#000', background='#ddd', highlightthickness=0, borderwidth=1)
    entry.place(x=expressions[i][0], y=expressions[i][1], width=300, height=20)

    '''rich = RTFText(window, width=50, border=0, bg=None)
    rich.place(x=expressions[i][0] + 10, y=expressions[i][1], width=300, height=20)
    rich.setRTF(expressions[i][3], font=font)

    rich.bind('<Button-1>', lambda e: rich.focus())'''

    expressions[i] = [entry, None, expressions[i][3], var, error] #, rich]
    expressions[i][1] = Expression(expressions[i][2])
    var.set(expressions[i][2])

def nspace(x: float):
    return ' ' if x > 0 else ''

def circle_coords(center, radius):
    return (center[0] - radius, center[1] - radius, center[0] + radius, center[1] + radius)

xy_center = (800 - 60, 60)
canvas.create_oval(*circle_coords(xy_center, 50), fill='#222', outline='#fff')
canvas.create_oval(*circle_coords(xy_center, 25), fill='#000', outline='#ccc')
canvas.create_text(xy_center[0], xy_center[1] + 50, text='XY', font=font, fill='#fff', anchor='n', justify='center'),
xy_line = canvas.create_line(0, 0, 0, 0, fill='#cc0')
xy_dot = canvas.create_oval(0, 0, 0, 0, fill='#ff0')
xy_range = canvas.create_oval(*circle_coords(xy_center, 25), fill='#000', outline='#ccc')

z_center = (800 - 60, 60 + 125)
canvas.create_oval(*circle_coords(z_center, 50), fill='#222', outline='#fff')
canvas.create_oval(*circle_coords(z_center, 25), fill='#000', outline='#ccc')
canvas.create_text(z_center[0], z_center[1] + 50, text='Z', font=font, fill='#fff', anchor='n', justify='center'),
z_line = canvas.create_line(0, 0, 0, 0, fill='#cc0')
z_dot = canvas.create_oval(0, 0, 0, 0, fill='#ff0')
z_range = canvas.create_oval(*circle_coords(z_center, 25), fill='#000', outline='#ccc')

def tryget(x):
    try:
        y = x.get()
        if y == 0:
            y = 1
        return y
    except:
        return 1

time_scale = tk.Scale(window, label='Speed', orient=tk.HORIZONTAL, from_=1.0, to=10.0, digits=2, resolution=0.01)
time_scale.place(x=50, y=580)

time_set = tk.Scale(window, label='Set', orient=tk.HORIZONTAL, from_=0.0, to=1.0, digits=3, resolution=0.001)
time_set.place(x=150, y=580)

funcs = {
    'findKnee': (1, lambda args: findKnee(*lengths[0:2], args[0]))
}

while True:
    window.update_idletasks()
    window.update()
    
    try:
        n = num_legs_var.get()
    except:
        n = 2
    n = max(min(n, 5), 1)
    if len(lengths) != n:
        lengths = [1 for _ in range(n)]
        create_legs(n)
    
    for i in range(min(len(lengths), len(length_entry))):
        lengths[i] = tryget(length_entry[i][1])

    vars = {
        'dt': 0
    }

    for i in range(len(expressions)):
        exp = expressions[i]
        entry = exp[0]
        expression = exp[1]
        current = exp[2]
        var = exp[3]
        if var.get() != current:
            #exp[5].setRTF(current, pad=(0,0), bg='#000', font=font)
            current = var.get()
            expressions[i][2] = current
            try:
                expression = Expression(current)
                expression.evaluate(vars)
                expressions[i][1] = expression
                canvas.itemconfig(exp[4], text='')
            except Exception as e:
                canvas.itemconfig(exp[4], text=str(e))

    for i in range(len(legs)):
        offset = i / len(legs)
        vars = {
            'dt': (time() / (10.01 - time_scale.get()) + offset) % 1 if time_set.get() == 0 else (time_set.get() + offset) % 1
        }
        x = expressions[0][1].evaluate(vars)#xExp.evaluate(vars)
        y = expressions[1][1].evaluate(vars)#yExp.evaluate(vars)
        z = expressions[2][1].evaluate(vars)
        #(x, y, z) = calc.solve(offset)
        angles = legs[i].update(lengths, (x, y, z))

        if i == len(legs) - 1:
            cx = xy_center[0] + x * 25
            cy = xy_center[1] + y * 25
            canvas.coords(xy_dot, cx - 2, cy - 2, cx + 2, cy + 2)
            cx = z_center[0] + z * 25
            cy = z_center[1] + vars['dt'] * 100 - 50
            canvas.coords(z_dot, cx - 2, cy - 2, cx + 2, cy + 2)

            coords = []
            for i in range(200):
                p = i / 199
                vars['dt'] = p
                coords.extend((xy_center[0] + expressions[0][1].evaluate(vars) * 25, xy_center[1] + expressions[1][1].evaluate(vars) * 25))
            canvas.coords(xy_line, coords)
            canvas.tag_raise(xy_line)
            canvas.tag_raise(xy_dot)
            coords.clear()
            for i in range(200):
                p = i / 199
                vars['dt'] = p
                coords.extend((z_center[0] + expressions[2][1].evaluate(vars) * 25, z_center[1] + p * 100 - 50))
            canvas.coords(z_line, coords)
            canvas.tag_raise(z_line)
            canvas.tag_raise(z_dot)

    canvas.itemconfig(labels[0], text=f'Hip : {nspace(angles.hip)}{degrees(angles.hip):.2f}')
    canvas.itemconfig(labels[1], text=f'Knee: {nspace(angles.knee)}{degrees(angles.knee):.2f}')
    canvas.itemconfig(labels[2], text=f'Foot: {nspace(angles.foot)}{degrees(angles.foot):.2f}')