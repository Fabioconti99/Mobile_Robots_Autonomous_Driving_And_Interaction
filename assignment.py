from __future__ import print_function

import time
from sr.robot import *


R = Robot()
###########################################
"""
    DRIVE
    Function for setting a linear velocity.
        
    Args:
    speed (int): the speed of the wheels.
    seconds (float): the time interval.
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
    Function for setting an angular velocity.
    
    Args:
    speed (int): the speed of the wheels.
    seconds (float): the time interval.
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
	Function to find the closest silver token within a defined area infront of the robot. The shape of the detecting area is a fraction of a circle 140 degrees wide and 1.2 distance units deep.
	Returns:
	dist (float): distance of the closest silver token detected within the area (-1 if no silver token is detected).
	rot_y (float): angle between the robot and the closest silver token detected within the area (-1 if no silver token is detected).
	
"""

def find_silver_token():

    dist = 1.2
    for token in R.see():
    
        if token.dist < dist and token.info.marker_type is MARKER_TOKEN_SILVER and -70 <token.rot_y< 70:
            dist=token.dist
            rot_y=token.rot_y
    if dist == 1.2:
        return -1, -1
    else:
           return dist, rot_y

###########################################
"""
	FIND_GOLDEN_TOKEN
	Function to find the closest gold token within a defined area infront of the robot. 
	The shape of the detecting area is a fraction of a circle 140 degrees wide and 1.2 distance units deep.
	
	Returns:
	dist (float): distance of the closest gold token detected within the area (-1 if no silver token is detected).
	rot_y (float): angle between the robot and the closest gold token detected within the area (-1 if no silver token is detected).
"""
def find_golden_token():

    dist=1.2
    for token in R.see():
        if token.dist < dist and token.info.marker_type is MARKER_TOKEN_GOLD and -45 < token.rot_y < 45:
            dist=token.dist
        rot_y=token.rot_y
    if dist==1.2:
        return -1, -1
    else:
           return dist, rot_y

###########################################
"""
	GOLD_TOKEN_LIST
	Function that checks if there's a golden token between the robot and the detected silver one inside of a 60 degrees window centered around the detected silver token. 
	
	Args:
	d_s (float): distance of the closest silver token (-1 if no silver token is detected).
	rot_s (float): relative angle between the closest silver token and the robot (-1 if no silver token is detected).
	
	Returns:
	True: if either no silver is found by the find_silver_token() function or a gold token is closer to the robot than a silver one is.
	False: if the detected silver token is closer to the robot than any of the golden ones are.
	
"""
def gold_token_list(d_s,rot_s):
    if ( d_s==-1):
        #print("no silver")
        return True
    else:
        dist=1.2
        for token in R.see():
            if token.dist < dist and token.info.marker_type is MARKER_TOKEN_GOLD and rot_s-30 < token.rot_y < rot_s+30:
                   dist=token.dist
            rot_y=token.rot_y
        if dist==1.2:
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
    If the the robot detects a gold token throught the function find_gold_token(). The function turns() will check to the between the right and the left of the robot where the closest wall is.
    according to this detection, the robot will decide to turn either to the left or to the right to get away of the wall.
    
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
        return True
    else:
        turn(25,0.1)
        return False
        
#########################################
"""
	GRAB_ROUTINE
	Function to make the robot grab the approached silver token and preventing it to hit gold tokens while doing so.
    
    info:
    the robot will take the silver token and place it behind itself.
    
"""
def grab_routine(r_l):
    
    R.grab()
    if (not r_l):
        turn(30,2.5)
        R.release()
        drive(-25,1)
        turn(-30,2.5)
    else:
        turn(-30,2.5)
        R.release()
        drive(-25,1)
        turn(30,2.5)

###########################################
"""
	SILVER_ROUTINE
	Function to make the robot approach the silver token getting as close as possible to it. 
    
    info:
    the robot will adjust the angle to the angle of the token and drive to it until it will reach the assigned distance thrashold to grab it.
    
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
    #Distance Threshold to grab the silver token
    
    drive(100,3) 
    #(optional)
    #Moveing the robot straight towards the first token in order to speed up the proces of finding the first token.

    while (1):
    
        d_silver , rot_y_silver = find_silver_token()
        d_gold, rot_y_gold= find_golden_token()
        gold = gold_token_list(d_silver, rot_y_silver)
        #Periodic call of all the detectiong functions needed to get the info on the surroundings of the robot
        
        if(gold):
            # if the robot can't see any gold silver token or either there's a gold one closer. 
            if (d_gold!=-1 and d_gold<0.9):
             #If the robot gets closer than 0.9' to a gold wall
                 print("turns")
                 turns()
                 #Routine to get way of the wall
            
            else:
             #If the robot doesen't see neither the silver nor the gold token
                print("drive")
                drive(100,0.2)
                
        
        else:
         #If the robot sees a silver token and its closer to the robot than any other gold ones

            print (rot_y_silver)
            silver_routine(rot_y_silver)
            #Aproach to the siver token

                
            if d_silver < d_th_silver:
            #The distance between the robot and the detected siver token lies within the given treashold, the robot will operate the grab routine

                print ("grab")
                grab_routine(turns())
                #Grabbing routine of the silver token
                
###########################################
                    
main()
