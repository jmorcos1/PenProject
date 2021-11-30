import threading
from turtle import Turtle, Screen

targetX = 0
targetY = 0
contactF = False


class App(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.start()
        
    def callback(self):
        self.root.quit()
    
    def run(self):
        self.root = Screen()
        #self.root.protocol("WM_DELETE_WINDOW", self.callback)
        #self.root.title('thinkPen')
        #self.root.geometry("1900x900")
        self.root.setup(500, 500, startx=10, starty=2)
        self.root.screensize(1900, 900)
        self.root.title("thinkPen Drawing")
        self.onmove(self.root, self.move_handler)
        self.root.mainloop()
    
    def move_handler(self, x, y):
        self.checkContact()
        self.onmove(self.root, None)  # avoid overlapping events
        yertle.setheading(yertle.towards(x, y))
        yertle.goto(x, y)
        self.onmove(self.root, self.move_handler)

    def onmove(self, fun, add=None):
        global targetX
        global targetY
        """
        Bind fun to mouse-motion event on screen.

        Arguments:
        self -- the singular screen instance
        fun  -- a function with two arguments, the coordinates
            of the mouse cursor on the canvas.
        """

        if fun is None:
            self.root.cv.unbind('<Motion>')
        else:
            def eventfun(event):
                fun(targetX, targetY)
            self.root.cv.bind('<Motion>', eventfun, add)

    def checkContact():
        global contactF
        if(contactF):
            yertle.pendown()
        else:
            yertle.penup()



"""
screen = Screen()
screen.setup(500, 500, startx=10, starty=2)
screen.screensize(1900, 900)
screen.title("thinkPen Drawing")
"""



yertle = Turtle()
yertle.penup()
yertle.shape('arrow')
yertle.resizemode('user')
yertle.shapesize(0.1, 0.1)
yertle.pensize(10)
yertle.home()
yertle.goto(-50, 50)
yertle.speed('fastest')

app = App()
#app.onmove(app.root, app.move_handler)


# Initially we track the turtle's motion and left button clicks
#onmove(screen, move_handler)  # a la screen.onmove(move_handler)
#yertle.onclick(click_handler)  # a click will turn motion into drag

