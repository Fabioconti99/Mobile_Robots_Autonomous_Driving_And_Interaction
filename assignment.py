from __future__ import print_function

import time
from sr.robot import *


R = Robot()
###########################################
"""
    DRIVE
    Function for setting a linear velocity
        
    Args:
    speed (int): the speed of the wheels
    seconds (int): the time interval
"""
def drive(speed, seconds):

    R.motors[0].m0.power = speed
    R.motors[0].m1.power = speed
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0

###########################################
"""
    TURN
    Function for setting an angular velocity
    
    Args:
    speed (int): the speed of the wheels
    seconds (int): the time interval
"""
def turn(speed, seconds):

    R.motors[0].m0.power = speed
    R.motors[0].m1.power = -speed
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0

###########################################
"""
    FIND_SILVER_TOKEN
    Function to find the closest silver token within a 2 units radius in front of the robot

    Returns:
    dist (float): distance of the closest silver token (-1 if no silver token is detected in a 2 units radius in front of it)
    rot_y (float): angle between the robot and the closest silver token (-1 if no silver token is detected in a 2 units radius in front of it)
"""
def find_silver_token():

    dist = 2
    for token in R.see():
    
        if token.dist < dist and token.info.marker_type is MARKER_TOKEN_SILVER and -45 <token.rot_y< 45:
            dist=token.dist
            rot_y=token.rot_y
    if dist == 2:
        return -1, -1
    else:
           return dist, rot_y

###########################################
"""
    FIND_GOLDEN_TOKEN
    Function to find the closest silver token within a 2 units radius in front of the robot

    Returns:
    dist (float): distance of the closest gold token (-1 if no silver token is detected in a 2 units radius in front of it)
    rot_y (float): angle between the robot and the closest gold token (-1 if no silver token is detected in a 2 units radius in front of it)
"""
def find_golden_token():

    dist=2
    for token in R.see():
        if token.dist < dist and token.info.marker_type is MARKER_TOKEN_GOLD and -60 < token.rot_y < 60:
            dist=token.dist
        rot_y=token.rot_y
    if dist==2:
        return -1, -1
    else:
           return dist, rot_y

###########################################
"""
    GOLD_TOKEN_LIST
    Function to check if there's a golden token in the way of a silver one

    Args:
    d_s (float): distance of the closest silver token (-1 if no silver token is detected in a 2 units radius in front of it)
    rot_s (float): relative angle between the closest silver token and the robot (-1 if no silver token is detected in a 2 units radius in front of it)
            
    Returns:
    True: if no silver is found in a 2 units angle in front of the robot or a gold token is closer to the robot than a silver is
    False: if the silver token is closer to the robot than any of the golden ones
"""
def gold_token_list(d_s,rot_s):
    if ( d_s==-1):
        #print("no silver")
        return True
    else:
        dist=2
        for token in R.see():
            if token.dist < dist and token.info.marker_type is MARKER_TOKEN_GOLD and rot_s-30 < token.rot_y < rot_s+30:
                   dist=token.dist
            rot_y=token.rot_y
        if dist==2:
            #print("no gold")
            return False
        elif (d_s>dist):
            #print("gold closer than silver")
            return True
        elif (d_s<=dist):
            #print("silver closer than gold")
            return False

###########################################
"""
    TURNS
    Function to make the robot turn away from a wall
    
    info:
    if the the closest wall is on the left/right of the robot,
    the robot will change tragectory takeing a turn to the right/left moveing away from the wall.
    
"""
def turns():


    dist=100
    for token in R.see():
        if token.dist < dist and token.info.marker_type is MARKER_TOKEN_GOLD and (-105 < token.rot_y < -75 or 75<token.rot_y<105):
            dist=token.dist
            rot_y=token.rot_y
    if dist==100:
        print("err")
    if rot_y>=0:
        turn(-25,0.1)
    else:
        turn(25,0.1)
        
#########################################
"""
    GRAB_ROUTINE
    Function to make the robot grab the silver token
    
    info:
    the robot will take the silver token and place it behind itself
    
"""
def grab_routine():

    R.grab()
    turn(40,1.90)
    R.release()
    drive(-25,1)
    turn(-40,1.90)

###########################################
"""
    SILVER_ROUTINE
    Function to make the robot approach the silver token
    
    info:
    the robot will adjust the angle to the angle of the token and drive to it until it will reach the distance thrashold in order to grab it
    
"""
def silver_routine(rot_y_silver,a_th=2):

    if rot_y_silver < -a_th:
        print ("turn neg")
        turn(-15, 0.1)
                        
    if rot_y_silver > a_th:
        print ("turn pos")
        turn(+15, 0.1)
        
    if(-a_th<rot_y_silver<a_th ):
        print ("straight")
        drive(80,0.15)


###########################################


def main():

    d_th_silver = 0.4
    #Threshold to grab the silver token
    
    drive(100,3)
    #Moveing the robot straight towards the first token in order to spped up the proces of finding the first token

    while (1):
    
        d_silver , rot_y_silver = find_silver_token()
        d_gold, rot_y_gold= find_golden_token()
        gold = gold_token_list(d_silver, rot_y_silver)
        #Periodic call of all the functions needed to get the info on the surroundings of the robot
        
        if(gold):
            
            if (d_gold!=-1 and d_gold<0.8):
             #If the robot gets close to a gold
                 print("turns")
                 turns()
                 #Routine to get way of the wall
            
            else:
             #If the robot doesen't see neither the silver nor the gold token
             
                drive(100,0.2)
                
        
        else:
         #If the robot sees a silver token

            print (rot_y_silver)
            silver_routine(rot_y_silver)
            #Aproach to the siver token

                
            if d_silver < d_th_silver:
            #The robot is within the treashold and it will operate the grab routine

                print ("grab")
                grab_routine()
                #Grabbing routine of the silver token
###########################################
                    
main()
