import tkinter

# TOOLS
DRAW, ERASE = list(range(2))
color = (0, 0, 0)
xold, yold = None, None

class Paint:
    def __init__(self, canvas):
        self.canvas = canvas
        self.tool, self.obj = None, None
        self.lastx, self.lasty = None, None
        self.canvas.bind('<Button-1>', self.update_xy)
        self.canvas.bind('<ButtonRelease-1>', self.reset)
        self.canvas.bind('<B1-Motion>', self.draw)

    def draw(self, event):
        if self.tool is None or self.obj is None:
            return

        x, y = self.lastx, self.lasty
        if self.tool in (DRAW, ERASE):
            self.canvas.coords(self.obj, (x, y, event.x, event.y))

    def update_xy(self, event):
        global erasing #why is this necessary lol
        if self.tool is None:
            return
        x, y = event.x, event.y

        if self.tool == DRAW:
            erasing = 0
            self.obj = None
            canvas.unbind('<B1-Motion>')
            canvas.bind('<B1-Motion>', self.draw_point)

        elif self.tool == ERASE:
            erasing = 1
            self.obj = None
            canvas.unbind('<B1-Motion>')
            canvas.bind('<B1-Motion>', self.draw_point)

        self.lastx, self.lasty = x, y

    def draw_point(self, event):
        global xold, yold
        x = event.x
        y = event.y
        if erasing == 1:
            canvas.create_rectangle((x, y, x+4, y+4), fill = 'white', outline = 'white')

        elif erasing == 0:
            if xold is not None and yold is not None:
                canvas.create_line(xold, yold, x, y)
            xold = x
            yold = y
    def reset(self, event):
        global xold, yold
        xold, yold = None, None

    def selecttool(self, tool):
        if tool == 0:
            print("Free draw tool selected")
        elif tool == 1:
            print("Erase tool selected")
        self.tool = tool

class Tool:
    def __init__(self, whiteboard, parent=None):
        self.whiteboard = whiteboard

        frame = tkinter.Frame(parent)
        self.currtool = None

        for i, (text, t) in enumerate((('D', DRAW), ('E', ERASE))):
            lbl = tkinter.Label(frame, text=text, width=2, relief='raised')
            lbl.tool = t
            lbl.bind('<Button-1>', self.updatetool)
            lbl.pack(padx=6, pady=6*(i % 2))

        frame.pack(side='left', fill='y', expand=True, pady=6)

    def updatetool(self, event):
        lbl = event.widget

        if self.currtool:
            self.currtool['relief'] = 'raised'

        lbl['relief'] = 'sunken'
        self.currtool = lbl
        self.whiteboard.selecttool(lbl.tool)


root = tkinter.Tk()
root.wm_title("Paint")
canvas = tkinter.Canvas(highlightbackground='black')
canvas.configure(background = 'white', width = 640, height = 480)
whiteboard = Paint(canvas)
tool = Tool(whiteboard)
canvas.pack(fill='both', expand=True, padx=6, pady=6)

root.mainloop()