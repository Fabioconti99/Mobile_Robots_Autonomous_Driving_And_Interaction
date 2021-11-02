# [Research_Track_1](https://unige.it/en/off.f/2021/ins/51201.html?codcla=10635) , [Robotics Engineering](https://courses.unige.it/10635) ([UNIGE](https://unige.it/it/)) : First assignement
## Python Robotics Simulator <img height="30" src="https://github.com/Fabioconti99/RT1_Assignment_1/blob/main/images/python.png">
### Professor. [Carmine Recchiuto](https://github.com/CarmineD8)


--------------------
Project objectives
--------------------

The aim of this project was to code a Python script capable of making an holonomic robot <img height="25" width = "25" src="https://github.com/Fabioconti99/RT1_Assignment_1/blob/main/sr/robot.png"> behave correctly inside of a given environment.

Thanks to the simulator we used for the assignment (developed by [Student Robotics](https://studentrobotics.org)), the robot will spawn inside of an arena composed of squared tokens of two different colors:
* The **gold tokens** ![alt text](https://github.com/Fabioconti99/RT1_Assignment_1/blob/main/sr/token.png) represent the wall of the maze the robot had to navigate in. 
* The **silver tokens** ![alt text](https://github.com/Fabioconti99/RT1_Assignment_1/blob/main/sr/token_silver.png) represent the objects the robot has to interact with.

The behavior of the robot has to stand by the following rules:
* constantly driving the robot around the environment in the counter-clockwise direction,
* Avoiding the gold tokens, 
* And once the robot will get close enough to a silver token, it should grab it and move it behind itself.

Picture of the **Enviroment**:

![alt text](https://github.com/Fabioconti99/RT1_Assignment_1/blob/main/images/arena.png) 

With everything working correctly, the robot should lap around the circuit avoiding the gold tokens and grabbing the silver ones on an infinite loop.


----------------------
Installing and running
----------------------

The simulator requires a Python 2.7 installation, the [pygame](http://pygame.org/) library, [PyPyBox2D](https://pypi.python.org/pypi/pypybox2d/2.1-r331), and [PyYAML](https://pypi.python.org/pypi/PyYAML/).

Pygame, unfortunately, can be tricky (though [not impossible](http://askubuntu.com/q/312767)) to install in virtual environments. If you are using `pip`, you might try `pip install hg+https://bitbucket.org/pygame/pygame`, or you could use your operating system's package manager. Windows users could use [Portable Python](http://portablepython.com/). PyPyBox2D and PyYAML are more forgiving, and should install just fine using `pip` or `easy_install`.

## Running the script

To run one or more scripts in the simulator use `run.py`, passing it the file names. 

```bash
$ python run.py assignment.py
```

## Troubleshooting

When running `python run.py <file>`, you may be presented with an error: `ImportError: No module named 'robot'`. This may be due to a conflict between sr.tools and sr.robot. To resolve, symlink simulator/sr/robot to the location of sr.tools.

On Ubuntu, this can be accomplished by:

* Find the location of srtools: `pip show sr.tools`
* Get the location. In my case this was `/usr/local/lib/python2.7/dist-packages`
* Create symlink: `ln -s path/to/simulator/sr/robot /usr/local/lib/python2.7/dist-packages/sr/`


---------
Robot API
---------

The API for controlling a simulated robot is designed to be as similar as possible to the [SR API][sr-api].

### Motors ###

The simulated robot has two motors configured for skid steering, connected to a two-output [Motor Board](https://studentrobotics.org/docs/kit/motor_board). The left motor is connected to output `0` and the right motor to output `1`.


The Motor Board API is identical to [that of the SR API](https://studentrobotics.org/docs/programming/sr/motors/), except that motor boards cannot be addressed by serial number. So, to turn on the spot at one quarter of full power, one might write the following:

```python
R.motors[0].m0.power = 25
R.motors[0].m1.power = -25
```

-------------------------------------------
#### Functions which use this element ####

This element is mainly used inside the code to make the robot drive straight (`drive(speed, seconds)`) and turn around the vertical axis (`turn(speed, seconds)`).


* #### `drive(speed , seconds)`
    
    The function `drive(_,_)` sets a linear velocity to the robot resulting in a straight shifting. To do so, it makes the robot's motors run at the same speed for a certain amount of time. 
    
    **Arguments**:
    * *speed*: represents the speed at which the wheels will spin. The velocity of the spin assigned to the wheels is settable within the interval *-100<speed<100*. 
    * *second*: represents the time interval in seconds [*s*] during which the wheels will spin.
    
    **Returns**:
    
    * *NONE*
    
    **Code:**

```python
def drive(speed, seconds):

    R.motors[0].m0.power = speed
    R.motors[0].m1.power = speed
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0
```


* #### `turn(speed , seconds)`

    The function turn(_,_) sets an angular velocity to the robot resulting in a rotation around the y axis (perpendicular to the map). To achieve this behavior, the function makes the robot's motors run at an opposite speed for a certain amount of time. 

    **Arguments**:
    * *speed*: represents the module of the speed at which the wheels will spin. To make the robot spin around its vertical axis, the velocity of the spin assigned to the right wheel is opposite to the velocity of the left one. If the ***speed*** argument is **positive** the rotation will be counter-clockwise. Given a **negative *speed***, the robot will rotate **clockwise**.
    * *second*: represents the time interval in seconds [*s*] during which the wheels will spin.
    
    **Returns**:
    * *NONE*

**The function**:

```python
def drive(speed, seconds):

    R.motors[0].m0.power = speed
    R.motors[0].m1.power = -speed
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0
```


-------------------
### The Grabber ###

The robot is equipped with a grabber, capable of picking up a token which is in front of the robot and within 0.4 metres of the robot's centre. To pick up a token, call the `R.grab` method:

```python
success = R.grab()
```

The `R.grab` function returns `True` if a token was successfully picked up, or `False` otherwise. If the robot is already holding a token, it will throw an `AlreadyHoldingSomethingException`.

To drop the token, call the `R.release` method.

Cable-tie flails are not implemented.

---------------------------------------------
#### Functions which use these elements ####

* #### `grab_routine()`
    The function `grab_routine()` is used throughout the code to pick up **silver tokens** and place them right behind the trajectory of the robot. 
     What the function does is: 

   * letting the robot grab the object right in front of it, 
   * moving it right behind itself, 
   * releasing it, 
   * backing up a bit in order to not hit the token, 
   * turning back to the original trajectory,
   * and keep moving forward. 
  
  `grab_routine()` is called inside the main function only when the robot is very close to a silver token. The control on the relative distance between the robot and the token makes the robot always grab the object avoiding mistakes during the use of the `grab()` function.

    **Arguments**:
    * *NONE*

    **Returns**:
    * *NONE*

 **The function**:

```python
def grab_routine():

    R.grab()    
    turn(40,1.90)
    R.release()
    drive(-25,1)
    turn(-40,1.90)
```
* The following **gif** represents the behavior of the robot once the function is called in the `main()` function:

<p align="center">
<img height="300" src="https://github.com/Fabioconti99/RT1_Assignment_1/blob/main/images/grab.gif">
</p>


-------------------
### Vision ###

To help the robot find tokens and navigate, each token has markers stuck to it, as does each wall. The `R.see()` method returns a list of all the markers the robot can see, as `Marker` objects. The robot can only see markers which it is facing towards.

Each `Marker` object has the following attributes:

* `info`: a `MarkerInfo` object describing the marker itself. Has the following attributes:
    * `code`: the numeric code of the marker.
    * `marker_type`: the type of object the marker is attached to (either `MARKER_TOKEN_GOLD`, `MARKER_TOKEN_SILVER` or `MARKER_ARENA`).
    * `offset`: offset of the numeric code of the marker from the lowest numbered marker of its type. For example, token number 3 has the code 43, but offset 3.
    * `size`: the size that the marker would be in the real game, for compatibility with the SR API.
* `centre`: the location of the marker in polar coordinates, as a `PolarCoord` object. Has the following attributes:
    * `length`: the distance from the centre of the robot to the object (in metres).
    * `rot_y`: rotation about the Y axis in degrees.
* `dist`: an alias for `centre.length`
* `res`: the value of the `res` parameter of `R.see`, for compatibility with the SR API.
* `rot_y`: an alias for `centre.rot_y`
* `timestamp`: the time at which the marker was seen (when `R.see` was called).


For example, the following code lists all of the markers the robot can see:

```python

markers = R.see()
print "I can see", len(markers), "markers:"

for m in markers:
    if m.info.marker_type in (MARKER_TOKEN_GOLD, MARKER_TOKEN_SILVER):
        print " - Token {0} is {1} metres away".format( m.info.offset, m.dist )
        
    elif m.info.marker_type == MARKER_ARENA
        print " - Arena marker {0} is {1} metres away".format( m.info.offset, m.dist )
```

------------------------------------------
#### Functions which use this element ####

The `R.see` method is used in the code for making the robot aware of its surroundings. Thanks to the Data provided by this method, the robot will be able to move inside the environment according to the tasks it has to accomplish. 


* #### `find_silver_token()`
    This function will detect the closest silver token to the center of the robot within a defined area in front of it.
    In the following example, we can see how to cycle all the Data contained in the `R.see()` until we find the closest token to the robot:
```python
def find_token():
    dist=100
    for token in R.see():
        if token.dist < dist:
            dist=token.dist
        rot_y=token.rot_y
    if dist==100:
    return -1, -1
    else:
       return dist, rot_y 
```
In this case, there are no constraints about where and what the robot has to check. 
To get the Data about the position of the **closest silver token** within a determined area we have to take all the attributes returned by the `R.see()` method and filter them. 
Using only the `marker_type`, `length`, and `rot_y` attributes we can define the detecting area within which `find_silver_token()` will look for the closest silver token. 
Following the same concept of the previously shown cycle, our function will have to compute the same control on the distance between the tokens and the robot but with extra constraints. These limitations will prevent the cycle from considering tokens of different types other than silver and tokens located outside the detecting region. 

**Arguments**:
* *NONE*

**Returns**:
* If a silver token is detected inside the detecting area, the function will return the **robot's relative distance from the token** ad its **relative angle**. If the token is not detected, the function will return -1 for both relative distance and relative angle.

 **The function**:

```python
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
```

With these new restrictions, the detecting area will assume a fraction circle shape 90° degrees wide and 2 units deep right in front of the robot. 
The following picture shows how the detecting area looks like:


* #### `find_golden_token()`
This function works in a similar way to `find_silver_token()` but for gold tokens.
Thanks to this function, the robot will detect the closest gold token to the center of the robot within a defined area. The main difference between `find_silver_token()` and `find_golden_token()` is the wider detecting area of 120° degrees compared to the 90° degrees of the other one. 

**The function**:

```python
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
```

* An example of the **detecting area for gold tokens** is shown in the following picture:
<p align="center">
<img height="300" src="https://github.com/Fabioconti99/RT1_Assignment_1/blob/main/images/turns_detector.png">
</p>

* #### `gold_token_list(d_s,rot_s)`

    `gold_token_list(d_s,rot_s)` checks if the silver token detected by the function `find_silver_token()` is the closest one inside of a 60° degrees window centered around the detected silver token.
    
    **Arguments**:
    * *d_s*: distance of the closest silver token.
    * *rot_s*: relative angle between the robot and the closest silver token.
    
    **Returns**:
    * *True*: the function returns true if there is a golden token inside the detecting area closer to the robot than a silver one is. It also returns true if no silver tokens are detected.
    * *False*: the function will return false if the closest token detected by the robot is silver. 

 **The function**:

```python
def gold_token_list(d_s,rot_s):
    if ( d_s==-1):
        print("no silver")
        return True
    else:
        dist=2
        for token in R.see():
            if token.dist < dist and token.info.marker_type is MARKER_TOKEN_GOLD and rot_s-30 < token.rot_y < rot_s+30:
                   dist=token.dist
            rot_y=token.rot_y
        if dist==2:
            print("no gold")
            return False
        elif (d_s>dist):
            print("gold closer than silver")
            return True
        elif (d_s<=dist):
            print("silver closer than gold")
            return False
```

* The following picture shows the sensors the function needs to detect the silver and gold tokens:
<p align="center">
<img height="300" src="https://github.com/Fabioconti99/RT1_Assignment_1/blob/main/images/gold_token_list.png">
</p>

* #### `turns()`

    The function `turns()` has the role of making the robot turn towards the opposite direction of the closest wall of gold tokens. Thanks to it, the robot will never hit the walls of the maze and will keep driving in the counter-clockwise direction. 
    This function gets called only once the robot gets close to a gold wall. When it does, it will check with a scan on the left and right side of the robot where the closest gold token is. If the relative angle between the token and the robot is negative, the closest token will be on the left side of the robot. This value will trigger a right turn of the robot until it doesn't detect any other gold tokens in front of itself. At that point, it will stop turning and will continue driving forward. The opposite thing will happen if the detection of the closest gold token returns a positive value. 
    
    **Arguments**:
    * *NONE*

    **Returns**:
    * *NONE*

**The function**:

```python
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
```

* The following **gif** represents the behavior of the robot once the function is called in the `main()` function:

<p align="center">

<img height="300" src="https://github.com/Fabioconti99/RT1_Assignment_1/blob/main/images/turns.gif">
</p>

* The following **picture** shows the lateral sensors needed to turn to the other way of the direction of the wall:

<p align="center">

<img height="300" src="https://github.com/Fabioconti99/RT1_Assignment_1/blob/main/images/turns.png">
</p>


* #### `silver_routine(rot_y_silver,a_th=2)`
    
    The function `silver_routine(rot_y_silver,a_th)` doesen't directly uses the `R.see()` method but it's compleatly. However, The way the function works expliots the data coming from it. It uses the threshold initialized at the beginning of the `main` function to create a routine capable of approaching the detected silver tokens. The function will loop until the relative angle between the robot and the silver token settles in an angular window defined by the set threshold. Once this condition is taken care of, the robot will start driving towards the detected token.
    **Arguments**:
    * *rot_y_silver*: relative angle between the detected silver token and the robot
    * *a_th*: threashold within witch the robot will have to mantain its relative angle between itself and the detected silver token. 
    
    **Returns**:
    * *NONE*

**The Function**:
```python
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
```


* The following **gif** represents the behavior of the robot once the function is called in the `main()` function:

<p align="center">
<img height="300" src="https://github.com/Fabioconti99/RT1_Assignment_1/blob/main/images/silver_app.gif">
</p>


------------------------------
## The `main()` function

The `main()` function consists of a while-loop that updates data regarding the robot's position inside the arena at every cycle. Thanks to this information the if-statements of the function will decide what function is best to call to make the robot behave correctly. 

### flowchart of the `main()` function

<p align="center">
<img height="1000" src="https://github.com/Fabioconti99/RT1_Assignment_1/blob/main/images/flow.png">
</p>

### Explenation of the different sections of the flow chart:

* **Step 1**:
    Declaration of the grabbing distance threshold:
    
    * `d_th_silver = 0.4` 
    
* **Step 2**: 
    The call of `drive(100,3)` function before the while loop is a way to speed up the robot right after its spawn. This statement is not necessary for the robot to operate correctly but it helps to accelerate its action.

* **Step 3**: 
    Beginning of the `while(1):` loop.

* **Step 4**: 
    The call of all the functions needed to make the robot aware of its surroundings at every moment during its action.
    There are two different data sets about the position of the closest gold token. The only difference between the two is the angle within which the function detects the closest gold token. These sets are used at different points of the code.
    
```python
    d_silver , rot_y_silver = find_silver_token()
    d_gold, rot_y_gold= find_golden_token()
    gold = gold_token_list(d_silver, rot_y_silver)
```
* **Step 5**: 
    Thanks to the return of the function `gold_token_list(d_silver, rot_y_silver)` an if statement can determine whether the gold token is closer to the robot than the detected silver is. The if-statement will choose whether the robot will **approach** ( `silver_routine(rot_y_silver)`) and **grab** `grab_routine()` a silver token or if it will continue to navigate around the arena looking for one of them.    
    
```python
    if(gold):
        
        if (d_gold!=-1 and d_gold<0.7):
            #If the robot gets close to a gold token 
            
            turns()
            
        else:
            #If the robot doesen't see neither the silver nor the gold token 
             
            drive(100,0.15)
                    
            
    else: 
     #If the robot sees a silver token 

        silver_routine(rot_y_silver)
        #Aproach to the siver token 

            
        if d_silver < d_th_silver:
        #The robot is within the treashold and it will operate the grab routine
        
            grab_routine()
```

------------------------
Conclusions and results
-----------

### Video of the robot's performance
This video shows a speeded up version of the perfromance of the robot during its first lap of the arena: 


https://user-images.githubusercontent.com/91262561/139699494-1ea55888-eb89-4668-a06d-8f3775f41092.mp4



### Possible improvements
During the development of the code I came up with a few ideas that could make the robot work smoother throughout the entire run:

* With the implementation I came up with so far, the robot points the silver tokens within a small distance range. A future accomplishment for the project would be expanding the view of the silver tokens to a farther distance. This improvement would make the robot start the approach routine earlier turning into a faster driving process. To achieve such behavior, the detecting area of the silver tokens should be expended in the `find_silver_token()` function. However, changing this property would require some finer adjustments on the function `gold_token_list(d_silver, rot_y_silver)` which would have to take care of a larger detecting area. 

* Another way to improve the ability of the robot to approach silver tokens may be using the `code` attribute. `code` is one of the attributes of the object type `Marker`. Through this numeric token's identification, the robot could save the `code` of every single grabbed token and not view it as a grabbable object anymore. This type of control could let the robot have a 360° degrees view of its surroundings. Letting a wider field of view will help the robot identify tokens from every possible angle making it easier to identify and point the following token.
  I've already tried to implement a function capable of recognizing the code of the silver token without achieving any decent result. Working on this feature, I noticed that many times the latest approached token's code would not get saved inside the dedicated variable. This mistake makes it impossible for the robot to avoid the just detected token after the grabbing routine. With an improved saving method, this routine could be an efficient way of avoiding already grabbed silver tokens. 


### Conclusions
This project was my first approach to the Python programming language and the development of a well-structured git repository. Working on this assignment, I gained knowledge about the basic concepts of Python such as creating variables, managing functions, and delivering clear and well-structured code that could easily be understood by other developers. I also learned new skills about the use of [Git](https://git-scm.com) as a distributed control system which I had never worked with before

