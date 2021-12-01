#main.py
"""
NJIT - ECE
Senior Design Project Code
*ThinkPen
-Fall 2021
AUTHORS: Jonathan M., Abe A., Angel K., Dhruv P. 
"""

import threading
import pmw_opticalNav_functions as mouse
import thinkPenDraw as thinkPen
import contactPressure as contact

def getMotion():
    motion_dX_dY_squal_lift = mouse.getDeltas()
    dX = 0
    dY = 0
    if(motion_dX_dY_squal_lift[0]):
        #print('chip lifted? : ', motion_dX_dY_squal_lift[4])
        #print('dX: ', motion_dX_dY_squal_lift[1], '   dY: ', motion_dX_dY_squal_lift[2])
        #print('Surface Qual. (Num. of features): ', motion_dX_dY_squal_lift[3])
        #print('\n\n')
        #time.sleep(0.2)

        dX = motion_dX_dY_squal_lift[1]
        dY = motion_dX_dY_squal_lift[2]

        """
        if(abs(dX) >= 7):
            dX = int(dX/20)
        else:
            dX = int(dX/15)
        if(abs(dY) >= 7):
            dY = int(dY/20)
        else:
            dY = int(dY/15)
        if(thinkPen.contactF):
            dX = int(dX/3)
            dY = int(dY/3)
        """
    
    #delay to limit read rate
    mouse.time.sleep(800/1000000)
    return [dX, dY]


try:
    if(mouse.setUp()):
        mouse.checkSROM()
        print("\n\n\t\t Mouse Sensor READY \n\n")
    else:
        print('WTF')

    
    
    while(True):
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
                print('touching')
            thinkPen.contactF = True

            
            thinkPen.yertle.shapesize(thinkPen.initialSize*contact_penSize[1],thinkPen.initialSize*contact_penSize[1]*3)
            thinkPen.yertle.pensize(thinkPen.initialPenSize*contact_penSize[1])
            print(contact_penSize[1])
        else:
            if(thinkPen.contactF == True):
                print('not touching')
            thinkPen.contactF = False

        if((abs(dX_dY[0]) > 0) | (abs(dX_dY[1]) > 0)):
            curr_xCor = thinkPen.yertle.xcor()
            curr_yCor = thinkPen.yertle.ycor()

            thinkPen.targetX = curr_xCor + dX_dY[0]
            thinkPen.targetY = curr_yCor + dX_dY[1]
            #print(thinkPen.targetX, thinkPen.targetX)

                    

            #print('currentX: ', curr_xCor, 'currentY: ', curr_yCor)
            #print('targetX: ', thinkPen.targetX, 'targetYY: ', thinkPen.targetY)
                    
            thinkPen.movePen(thinkPen.targetX, thinkPen.targetY)

            """

            while((curr_xCor != thinkPen.targetX)|(curr_yCor != thinkPen.targetY)):
                curr_xCor = thinkPen.yertle.xcor()
                curr_yCor = thinkPen.yertle.ycor()
                print('currentX: ', curr_xCor, 'currentY: ', curr_yCor)
                print('targetX: ', thinkPen.targetX, 'targetYY: ', thinkPen.targetY)
            
            """
                    
                
                        
finally:
    mouse.spi.unlock()





