from __future__ import print_function

import time
from sr.robot import *


R = Robot()
###########################################
"""
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
	Function to find the closest silver token within a 2 units radius in front of the robot

	Returns:
	dist (float): distance of the closest silver token (-1 if no silver token is detected in a 2 units radius in front of it)
	rot_y (float): angle between the robot and the closest silver token (-1 if no silver token is detected in a 2 units radius in front of it)
"""
def find_silver_token(): 

    dist = 2 # modificato 
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
	Function to find the closest silver token within a 2 units radius in front of the robot

	Returns:
	dist (float): distance of the closest gold token (-1 if no silver token is detected in a 2 units radius in front of it)
	rot_y (float): angle between the robot and the closest gold token (-1 if no silver token is detected in a 2 units radius in front of it)
"""
def find_golden_token(th):

    dist=2
    for token in R.see():
        if token.dist < dist and token.info.marker_type is MARKER_TOKEN_GOLD and -th < token.rot_y < th:
            dist=token.dist
	    rot_y=token.rot_y
    if dist==2:
		return -1, -1
    else:
   		return dist, rot_y

###########################################
"""
	Function to check if there's a golden token in the way of a silver one

	Args: 
	rot_s (float): angle between the robot and the closest silver token (-1 if no silver token is detected in a 2 units radius in front of it)
	d_s (float): distance of the closest silver token (-1 if no silver token is detected in a 2 units radius in front of it)
	rot_g (float): angle between the robot and the closest gold token (-1 if no silver token is detected in a 2 units radius in front of it)
	d_g (float): distance of the closest gold token (-1 if no silver token is detected in a 2 units radius in front of it)
	  	  
	Returns:
	True: if no silver is found in a 2 units angle in front of the robot or a gold token is closer to the robot than a silver is
	False: if the silver token is closer to the robot than any of the golden ones
"""
def gold_token_list(d_s,d_g):

	if ( d_s==-1):
		print("no silver")
		return True
	else:
	
		if (d_s>d_g ):
			print("gold closer than silver")
			return True
		elif (d_s<=d_g):
			print("silver closer than gold")
			return False

###########################################
"""
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
		#drive(10, 0.5)
		print("err")
	if rot_y>=0:
		turn(-25,0.1)
		#drive(20,0.1)
	else:
		turn(25,0.1)
   		#drive(20,0.1)
#########################################
"""
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
	Function to make the robot approach the silver token
    
	info: 
	the robot will adjust the angle to the angle of the token and drive to it until it will reach the distance thrashold in order to grab it
    
"""
def silver_routine(rot_y_silver,a_th):

	if rot_y_silver < -a_th:
		print ("turn neg")
		turn(-15, 0.1)
						
	if rot_y_silver > a_th:
		print ("turn pos")
		turn(+15, 0.1)
			
	if(-a_th<rot_y_silver<a_th ):
		print ("straight")
		drive(75,0.2)


###########################################


def main():

	d_th_silver = 0.4
	#Threashold to grab the silver token 
	
	a_th = 2
	#Trashold for the angle within whitch the robot has to be in order to go grab the silver token 
	
	gold= True
	#Initializing to true the bool variable gold 

	drive(100,3)
	#Moveing the robot straight towards the first token in order to initialize the direction of the movement of the robot counter clockwise 

	while (1):
	
		d_silver , rot_y_silver = find_silver_token()
		d_gold, rot_y_gold= find_golden_token(60)
		d_gold2, rot_y_gold2= find_golden_token(45)
		gold = gold_token_list(d_silver, d_gold2)
		
		if(gold):
			
			if (d_gold!=-1 and d_gold<0.7):
 			#If the robot gets close to a gold token and doesn't see a silver token 

				turns()
				print("turns")
			
			else:
 			#If the robot doesen't see neither the silver nor the gold token 
 			
				drive(75,0.1)
				#print("drive")
				
		
		else: 
 		#If the robot sees a silver token 

			print (rot_y_silver)
			silver_routine(rot_y_silver,a_th)
			#Aproach to the siver token 

				
			if d_silver < d_th_silver:
			#The robot is within the treashold and it will operate the grab routine

				print ("grab")
				
				grab_routine()
					
	
main()

