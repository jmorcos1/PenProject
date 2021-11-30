from turtle import Turtle, Screen

targetX = 0
targetY = 0
contactF = False

def movePen(x, y):
    checkContact()
    yertle.setheading(yertle.towards(x, y))
    yertle.goto(x, y)


def checkContact():
    global contactF
    if(contactF):
        yertle.pendown()
    else:
        yertle.penup()


screen = Screen()
screen.setup(500, 500, startx=10, starty=2)
screen.screensize(1900, 900)
screen.title("thinkPen Drawing")

initialSize = 0.1
initialPenSize = 4

yertle = Turtle()
yertle.penup()
yertle.shape('arrow')
yertle.resizemode('user')
yertle.shapesize(initialSize, initialSize)
yertle.pensize(initialPenSize)
yertle.home()
yertle.goto(-50, 50)
yertle.speed('fastest')