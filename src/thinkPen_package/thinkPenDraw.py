from turtle import Turtle, Screen

targetX = 0
targetY = 0
contactF = False

def movePen(x, y):
    checkContact()
    x = min(xMax, max(xMin, x))
    y = min(yMax, max(yMin, y))
    yertle.setheading(yertle.towards(x, y))
    yertle.goto(x, y)


def checkContact():
    global contactF
    if(contactF):
        yertle.pendown()
        print(yertle.position())
    else:
        yertle.penup()


screen = Screen()
screen.setup(400, 300, startx=-10, starty=2)
screenSX = 500
xMin = -screenSX/2
xMax = screenSX/2
screenSY = 500
yMin = -screenSY/2
yMax = screenSY/2
screen.screensize(500, 500)
screen.title("thinkPen Drawing")

initialPenSize = 2
initialSize = initialPenSize/5


yertle = Turtle()
yertle.penup()
yertle.shape('arrow')
yertle.resizemode('user')
yertle.shapesize(initialSize, initialSize)
yertle.pensize(initialPenSize)
yertle.home()
yertle.goto(-50, 50)
yertle.speed('fastest')
yertle.fillcolor('green')
#yertle.pencolor('black')

print(screen.xscale)