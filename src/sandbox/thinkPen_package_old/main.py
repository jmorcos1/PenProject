#main.py
"""
NJIT - ECE
Senior Design Project Code
*ThinkPen
-Fall 2021
AUTHORS: Jonathan M., Abe A., Angel K., Dhruv P. 
"""

import pmw_opticalNav_functions as mouse
import old_draw as thinkPen
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

        if(abs(dX) >= 10):
            dX = int(dX/2)
        if(abs(dY) >= 10):
            dY = int(dY/2)
    #delay to limit read rate
    mouse.time.sleep(800/1000000)
    return [dX, dY]

try:
    if(mouse.setUp()):
        mouse.checkSROM()
        print("\n\n\t\t Mouse Sensor READY \n\n")
    else:
        print('WTF')
    
    thinkPen.screen.mainloop()

    
    #app = thinkPen.App()
    while(True):
        contact_penSize = contact.getContact_getSize()
        dX_dY = getMotion()
        if(contact_penSize[0]):
            thinkPen.contactF = True
        else:
            thinkPen.contactF = False
        if((abs(dX_dY[0]) > 0) | (abs(dX_dY[1]) > 0)):
            thinkPen.targetX = thinkPen.targetX + dX_dY[0]
            thinkPen.targetX = thinkPen.targetX + dX_dY[1]
        #thinkPen.app.onmove(thinkPen.app.root, thinkPen.app.move_handler)



finally:
  mouse.spi.unlock()

