
from tkinter import Canvas
from solver import ik2d, LegAngles
from math import sin, cos, pi

LINE_LENGTH = 100
LINE_WIDTH = 3

COLORS = [
    '#f00',
    '#0f0',
    '#00f',
    '#ff0',
    '#0ff',
    '#f0f',
    '#fff'
]

def pad(x, c, i):
    while len(x) < i:
        x += c
    return x

def color(i, shade):
    hexa = COLORS[i].replace('f', 'ff').replace('0', '00')
    stra = pad(hex(int(int(hexa[1:3], 16) * shade))[2:], '0', 2) \
        + pad(hex(int(int(hexa[3:5], 16) * shade))[2:], '0', 2) \
        + pad(hex(int(int(hexa[5:7], 16) * shade))[2:], '0', 2)
    return '#' + stra

class SolveTree:
    def __init__(self, start: tuple[int, int]):
        self.position = start
        #self.depth = 0
        self.rotation = 0
    
    def update(self, rotation: int, length):
        self.rotation += rotation
        last = self.position
        nextPos = (
            self.position[0] + LINE_LENGTH * length * sin(self.rotation),
            self.position[1] + LINE_LENGTH * length * cos(self.rotation)
        )
        self.position = nextPos
        return last, self.position

class Leg:
    def __init__(self, canvas: Canvas, joints=2, shade=1) -> None:
        self.canvas = canvas
        self.joints = joints
        self.shade = shade
        self.lines = []
        self.create()

    def __del__(self):
        self.destroy()
    
    def create(self):
        if len(self.lines) > 0:
            self.destroy()
        for i in range(self.joints + 1):
            self.lines.append(self.canvas.create_line(
                0, 0, 0, 0, fill=color(i, self.shade), width=LINE_WIDTH))

    def destroy(self):
        if len(self.lines) > 0:
            self.canvas.delete(*self.lines)
            self.lines.clear()
    
    def update(self, lengths: list[int], coords: list[int]):
        if len(lengths) != self.joints:
            raise ValueError('lengths must be the same length as the number of joints!')
        if len(lengths) != 2:
            return LegAngles()
        tree = SolveTree((400, 400))

        try:
            angles: LegAngles = ik2d(*lengths[0:2], coords[0], coords[1])
        except:
            angles = LegAngles()

        for i in range(self.joints):
            last, now = tree.update(angles[i], lengths[i])
            self.canvas.coords(self.lines[i], *last, *now)
        
        LINE_LENGTH2 = LINE_LENGTH
        footPos0 = (
            tree.position[0] - 50 * cos(tree.rotation + angles.foot),
            tree.position[1] - 50 * sin(tree.rotation + angles.foot)
        )
        footPos1 = (
            tree.position[0] + 50 * cos(tree.rotation + angles.foot),
            tree.position[1] + 50 * sin(tree.rotation + angles.foot)
        )
        self.canvas.coords(self.lines[-1], *footPos0, *footPos1)
        
        return angles