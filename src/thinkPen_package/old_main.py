#main.py
"""
NJIT - ECE
Senior Design Project Code
*ThinkPen
-Fall 2021
AUTHORS: Jonathan M., Abe A., Angel K., Dhruv P. 
"""

import pmw_opticalNav_functions as mouse
import thinkPenDraw as thinkPen
import contactPressure as contact
import os
import board
import digitalio
import time

currentDir = os.path.abspath(os.path.curdir) #get python file location

def getMotion():
    motion_dX_dY_squal_lift = mouse.getDeltas()
    dX = 0
    dY = 0
    if(motion_dX_dY_squal_lift[0]):
        dX = motion_dX_dY_squal_lift[1]
        dY = motion_dX_dY_squal_lift[2]
    
    #delay to limit read rate
    mouse.time.sleep(800/1000000)
    return [dX, dY]

def pen_undo():
    while(thinkPen.yertle.undobufferentries()):
        thinkPen.yertle.undo()

def savePenFile():
    gotName = False
    name = '_'
    while(not gotName):
        print('\n\n Please Enter a file name (no spaces please!)')
        name = input()
        if(not (' ' in name)):
            gotName = True

    thinkPen.screen.getcanvas().postscript(file="{}.eps".format(name))
    command = "ps2pdf {0}/{1}.eps {0}/{1}.pdf".format(currentDir, name)
    os.system(command)
    command = "mv {0}/{1}.eps {0}/savedDrawings/".format(currentDir, name)
    os.system(command)
    command = "mv {0}/{1}.pdf {0}/savedDrawings/".format(currentDir, name)
    os.system(command)


try:
    upTime = time.monotonic()
    time.sleep(1.5)
    downTime = time.monotonic()

    undoButton = digitalio.DigitalInOut(board.D17) #pin11
    saveButton = digitalio.DigitalInOut(board.D27) #pin13
    resetButton = digitalio.DigitalInOut(board.D22) #pin15

    undoButton.direction = digitalio.Direction.INPUT
    saveButton.direction = digitalio.Direction.INPUT
    resetButton.direction = digitalio.Direction.INPUT

    undoButton.pull = digitalio.Pull.UP
    saveButton.pull = digitalio.Pull.UP
    resetButton.pull = digitalio.Pull.UP


    if(mouse.setUp()):
        mouse.checkSROM()
        print("\n\n\t\t Mouse Sensor READY \n\n")
    else:
        raise Exception('Error Initializing Mouse Sensor')

    while(True):
        if(not resetButton.value):
            thinkPen.clear_reset()
        elif(not saveButton.value):
            savePenFile()
        elif(not undoButton.value):
            pen_undo()
        else:
            contact_penSize = contact.getContact_getSize()
            dX_dY = getMotion()

            if(abs(dX_dY[0]) >= 7):
                dX_dY[0] = dX_dY[0]/20
            else:
                dX_dY[0] = dX_dY[0]/17
            if(abs(dX_dY[1]) >= 7):
                dX_dY[1] = dX_dY[1]/20
            else:
                dX_dY[1] = dX_dY[1]/17
            if(thinkPen.contactF):
                dX_dY[0] = dX_dY[0]/2
                dX_dY[1] = dX_dY[1]/2

            dX_dY[0] = dX_dY[0]/thinkPen.screen.xscale
            dX_dY[1] = dX_dY[1]/thinkPen.screen.yscale

                
            if(contact_penSize[0]):
                if(thinkPen.contactF == False):
                    downTime = time.monotonic()
                    print('touching')
                    if((downTime - upTime) > 0.4):
                        thinkPen.yertle.setundobuffer(1000)
                thinkPen.contactF = True

            
                thinkPen.yertle.shapesize(thinkPen.initialSize*contact_penSize[1],thinkPen.initialSize*contact_penSize[1]*3)
                thinkPen.yertle.pensize(thinkPen.initialPenSize*contact_penSize[1])
            
                #print(contact_penSize[1])
            else:
                if(thinkPen.contactF == True):
                    upTime = time.monotonic()
                    print('not touching')
                    #pen_undo()
                thinkPen.contactF = False
                thinkPen.yertle.shapesize(thinkPen.initialSize*contact.sFactorIn,thinkPen.initialSize*contact.sFactorIn*3)
                thinkPen.yertle.pensize(thinkPen.initialPenSize*contact.sFactorIn)
            


            if((abs(dX_dY[0]) > 0) | (abs(dX_dY[1]) > 0)):
                curr_xCor = thinkPen.yertle.xcor()
                curr_yCor = thinkPen.yertle.ycor()

                thinkPen.targetX = curr_xCor + dX_dY[0]
                thinkPen.targetY = curr_yCor + dX_dY[1]
                thinkPen.movePen(thinkPen.targetX, thinkPen.targetY)
                    
                        
finally:
    mouse.pmw_shutDown()
    mouse.spi.unlock()
    print('\t closing program')





