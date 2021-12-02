from turtle import Turtle, Screen

MOVING, DRAGGING = range(2)  # states

def move_handler(x, y):
    if state != MOVING:  # ignore stray events
        return

    onmove(screen, None)  # avoid overlapping events
    yertle.penup()
    yertle.setheading(yertle.towards(x, y))
    yertle.goto(x, y)
    onmove(screen, move_handler)

def click_handler(x, y):
    global state

    yertle.onclick(None)  # disable until release
    onmove(screen, None)  # disable competing handler

    yertle.onrelease(release_handler)  # watch for release event
    yertle.ondrag(drag_handler)  # motion is now dragging until release

    state = DRAGGING

def release_handler(x, y):
    global state

    yertle.onrelease(None)  # disable until click
    yertle.ondrag(None)  # disable competing handler

    yertle.onclick(click_handler)  # watch for click event
    onmove(screen, move_handler)  # dragging is now motion until click

    state = MOVING

def drag_handler(x, y):
    if state != DRAGGING:  # ignore stray events
        return

    yertle.ondrag(None)  # disable event inside event handler
    yertle.pendown()
    yertle.setheading(yertle.towards(x, y))
    yertle.goto(x, y)
    yertle.ondrag(drag_handler)  # reenable event on event handler exit

def onmove(self, fun, add=None):
    """
    Bind fun to mouse-motion event on screen.

    Arguments:
    self -- the singular screen instance
    fun  -- a function with two arguments, the coordinates
        of the mouse cursor on the canvas.

    Example:

    >>> onmove(turtle.Screen(), lambda x, y: print(x, y))
    >>> # Subsequently moving the cursor on the screen will
    >>> # print the cursor position to the console
    >>> screen.onmove(None)
    """

    if fun is None:
        self.cv.unbind('<Motion>')
    else:
        def eventfun(event):
            fun(self.cv.canvasx(event.x) / self.xscale, -self.cv.canvasy(event.y) / self.yscale)
        self.cv.bind('<Motion>', eventfun, add)

initialPenSize = 2
initialSize = initialPenSize/5

screen = Screen()
screen.setup(400, 300, startx=-10, starty=2)
screen.screensize(500, 500)
screen.title("Mouse Drawing")

yertle = Turtle('arrow')
yertle.speed('fastest')

yertle.resizemode('user')
yertle.shapesize(initialSize*0.2, initialSize*0.2*3)
yertle.pensize(initialPenSize*0.2)

yertle.penup()
yertle.home()
yertle.goto(-50, 50)
yertle.speed('fastest')
yertle.fillcolor('green')

state = MOVING

# Initially we track the turtle's motion and left button clicks
onmove(screen, move_handler)  # a la screen.onmove(move_handler)
yertle.onclick(click_handler)  # a click will turn motion into drag

screen.mainloop()