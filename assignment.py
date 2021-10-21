from __future__ import print_function

import time
from sr.robot import *


R = Robot()


def drive(speed, seconds):

    R.motors[0].m0.power = speed
    R.motors[0].m1.power = speed
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0


def turn(speed, seconds):

    R.motors[0].m0.power = speed
    R.motors[0].m1.power = -speed
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0

###########################################

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

def find_golden_token():

    dist=0.8
    for token in R.see():
        if token.dist < dist and token.info.marker_type is MARKER_TOKEN_GOLD and -60 < token.rot_y < 60:
            dist=token.dist
	    rot_y=token.rot_y
    if dist==0.8:
		return False
    else:
   		return True



###########################################

def gold_token_list(p,d):

	a=False
	for token in R.see():
		"""token.info.marker_type is MARKER_TOKEN_GOLD and (p-4< token.rot_y <p+4 and  token.dist<d) or"""
		if (token.info.marker_type is MARKER_TOKEN_GOLD and (p-4< token.rot_y <p+4 and  token.dist<d) or d==-1):
			a=True # c'e un gold
	
	return a

###########################################

def turns():
	dist=100
	for token in R.see():
		if token.dist < dist and token.info.marker_type is MARKER_TOKEN_GOLD and (-105 < token.rot_y < -75 or 75<token.rot_y<105):
			dist=token.dist
			rot_y=token.rot_y
	if dist==100:
		drive(10, 0.5)
		print("aaaaa")
	if rot_y>=0:
		turn(-15,0.2)
	else:
		turn(15,0.2)
   		
#########################################

def grab_routine():
	R.grab()	
	turn(40,1.90)
	drive(20,1)
	R.release()
	drive(-20,1)
	turn(-40,1.90)
	
#########################################


def main():

	d_th_silver = 0.4
	a_th = 2
	d_silver , rot_y_silver = find_silver_token()
	golden = find_golden_token()
	gold= True
	drive(100,3)
	
	while (1):
	
		d_silver , rot_y_silver = find_silver_token()
		golden = find_golden_token()
		
		if(gold): # non vedo silver in linea d'aria
			gold = gold_token_list(rot_y_silver , d_silver )
			if (golden):
			
				print (rot_y_silver)
				print (d_silver)
				
				turns()
				print("turns")
			
			else:
				drive(75,0.1)
				print("drive")
		
		else: # vedo un silver
		
			print (rot_y_silver)
			
			if rot_y_silver < -a_th:
				print ("turn neg")
				turn(-15, 0.1)
						
			if rot_y_silver > a_th:
				print ("turn pos")
				turn(+10, 0.1)
			
			if(-a_th<rot_y_silver<a_th ):
				print ("straight")
				drive(100,0.1)
				
				if d_silver < d_th_silver:
					
					print ("grab")
					gold=True
					grab_routine()
					
	
main()

