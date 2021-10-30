# [Research_Track_1](https://unige.it/en/off.f/2021/ins/51201.html?codcla=10635) , [Robotics Engineering](https://courses.unige.it/10635) ([UNIGE](https://unige.it/it/)) : First assignement
## Python Robotics Simulator
### Professor. [Carmine Recchiuto](https://github.com/CarmineD8)

-----------------------

Project objectives
--------------------

The aim of this project was to code a Python script <code><img height="20" src="https://github.com/Fabioconti99/RT1_Assignment_1/blob/main/images/python.png"></code> capable of making an holonomic robot <img height="25" width = "25" src="https://github.com/Fabioconti99/RT1_Assignment_1/blob/main/sr/robot.png"> behave correctly inside of a given environment.

Thanks to the simulator we used for the assignement (developed by [Student Robotics](https://studentrobotics.org)), the robot will spawn inside of an arena composed of squared tokens of two different colors:
* The **gold tokens** ![alt text](https://github.com/Fabioconti99/RT1_Assignment_1/blob/main/sr/token.png) rappresent the wall of the maze the robot had to navigate in. 
* The **silver tokens** ![alt text](https://github.com/Fabioconti99/RT1_Assignment_1/blob/main/sr/token_silver.png) rappresent the objects the robot has to interact with.

The behavior of the robot has to stand by the following rules:
* constantly driving the robot around the environment in the counter-clockwise direction,
* Avoiding the gold tokens, 
* And once the robot will get close enough to a silver token placed inside the environment, grabbing it and moves it behind itself.

Picture of the **Enviroment**:
![alt text](https://github.com/Fabioconti99/RT1_Assignment_1/blob/main/images/arena.png) 

With everything working correctely, the robot should lap around the circuit avoiding the gold tokens and grabbing the silver ones on an infinite loop.


Installing and running
----------------------

The simulator requires a Python 2.7 installation, the [pygame](http://pygame.org/) library, [PyPyBox2D](https://pypi.python.org/pypi/pypybox2d/2.1-r331), and [PyYAML](https://pypi.python.org/pypi/PyYAML/).

Pygame, unfortunately, can be tricky (though [not impossible](http://askubuntu.com/q/312767)) to install in virtual environments. If you are using `pip`, you might try `pip install hg+https://bitbucket.org/pygame/pygame`, or you could use your operating system's package manager. Windows users could use [Portable Python](http://portablepython.com/). PyPyBox2D and PyYAML are more forgiving, and should install just fine using `pip` or `easy_install`.

## Running the script

To run one or more scripts in the simulator, use `run.py`, passing it the file names. 

```bash
$ python run.py assignment.py
```

## Troubleshooting

When running `python run.py <file>`, you may be presented with an error: `ImportError: No module named 'robot'`. This may be due to a conflict between sr.tools and sr.robot. To resolve, symlink simulator/sr/robot to the location of sr.tools.

On Ubuntu, this can be accomplished by:

* Find the location of srtools: `pip show sr.tools`
* Get the location. In my case this was `/usr/local/lib/python2.7/dist-packages`
* Create symlink: `ln -s path/to/simulator/sr/robot /usr/local/lib/python2.7/dist-packages/sr/`


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

#### Functions which use this element ####

This element is mainly used inside the code to make the robot drive straght (`drive(speed , seconds)`) and turn around the vertical axis (`turn(speed , seconds)`).

* #### `drive(speed , seconds)`
    
    The function `drive(_,_)` sets a linear velocity to the robot resulting into a straight shifting. In order to achive this behaveour, the function makes the robot's motors run at the same speed for certain amount of time. 
    
    **Arguments**:
    
    * *speed*: rappresents the speed at which the wheels will spin. The velocity of the spin assigned to the wheels is settable within the interval *-100<speed<100*. 
    * *second*: rappresents the time interval in seconds [*s*] during which the wheels will spin.
    
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

    The function `turn(_,_)` sets an angular velocity to the robot resulting into a rotation around the y axis (perpendicular to the map). In order to achive this behaveour, the function makes the robot's motors run at opposit speed for certain amount of time. 

    **Arguments**:
    * *speed*: rappresents the module of the speed at which the wheels will spin. In order to make the robot spin around its own vertical axis, the velocity of the spin assigned to the right wheel is opposit to the velocity of the left one. If the ***speed*** argument is **positive** the rotation will be counter-clockwise. Given a **negative *speed***, the robot will rotate **clockwise**.
    * *second*: rappresents the time interval in seconds [*s*] during which the wheels will spin.
    
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

#### Functions which use these elements ####

* #### `grab_routine()`
    The function `grab_routine()` is used throught out the code to pick up **silver tokens** and placeing them right behind tajectory of the robot. 
    What the function does is: 

     * letting the robot grab the object right infront it, 
     * moveing it right behind itself, 
     * releasing it, 
     * backing up a bit in oder to not hit the token, 
     * turning back to the original trajectory,
     * and keep moveing forward. 
     
     `grab_routine()`  is called inside the main function only when the robot is very close to a silver token. The control on the relative distance between the robot and the token makes the robot always grab the object avoiding mistaks during the use of the `grab()` function.

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
The following **gif** rappresents the behavior of the robot once the function is called in the main function:
<img height="200" src="https://github.com/Fabioconti99/RT1_Assignment_1/blob/main/images/grab.gif">

-------------------
### Vision ###

To help the robot find tokens and navigate, each token has markers stuck to it, as does each wall. The `R.see` method returns a list of all the markers the robot can see, as `Marker` objects. The robot can only see markers which it is facing towards.

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

#### Functions which use this element ####

The `R.see` method is used in the code as a way of makeing the robot aware of its surroundings. Thanks to the Data provided by this method, the robot will be able to move inside the enviroment according to the tasks it has to accomplish. 


* #### `find_silver_token()`
    This function will detect the closest silver token to the center of the robot within a defined area in front of it.
    In the following example we can se how to cicle all the Data contained in the `R.see()` until we find the closest token to the robot:
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
In this case there are no constraints about where and what the robot has to look for. 
In order to get the Data about the position of **closest silver token** within a determined area we have to take all the attributes returned by the `R.see()` method and filter them. 
Using only the `marker_type`, `length`, and `rot_y` attributes we can define the detecting area within which  `find_silver_token()` will look for the closest silver token. 
Following the same concept of the previously shown cicle, our function will have to compute the same control on the distance between the tokens and the robot but with extra constrains. These limitations will prevent the cicle to concider tokens of different type other than silver and tokens located outside the detecting region. 
**Arguments**:
* *NONE*

**Returns**:
* If a silver token is detected inside the detecting area, the function will return the **robot's relative distance from the token** ad its **relative angle**. If the token is not detected, the function will return -1 for both relative distace and relative angle.

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

With these new restrictions applied, the detecting area will assume a fraction circle shape 90 degrees wide and 2 units deep right in front of the robot. 
The following picture shows how the detecting area looks like:


* #### `find_golden_token(angle)`
This function works in a similar way of  `find_silver_token()` but for gold tokens.
Thanks to this function the robot will be able to detect the closest gold token to the center of the robot within a defined area. The main difference that distingush its behavior to the `find_silver_token()` is the fact that `find_golden_token(angle)` has an input **argument** which tels the function how wide the circle fraction of the detecting area has to be. 

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

* #### `gold_token_list(d_s,d_g)`

    This function tells the robot if the silver token detected by the function `find_silver_token()` is the closest token overall. 
    
    **Arguments**:
    * *d_s*: Distance of the closest silver token
    * *d_g*: Distance of the closest gold token
    
    **Returns**:
    * *True*: the function returns true if there is a golden token inside the detecting area closer to robot than a silver one is. It also returns true if no silver tokens are detected.
    * *False*: the function will return false if the closest token detected by the robot is silver. 

 **The function**:

```python
def gold_token_list(d_s,d_g):

    if ( d_s==-1):
        print("no silver")
        return True
    else:
        if (d_s>d_g and d_g!=-1):
            print("gold closer than silver")
            return True
        elif (d_s<=d_g):
            print("silver closer than gold")
            return False
```

* #### `turns()`

    The function `turns()` has the role of makeing the robot turn towards the opposit direction of the closest wall of gold tokens. Thanks to this function the robot will never hit the walls of the maze and will keep driveing towards the counter-clockwise direction. 
    This function is only called once the robot gets close to a gold wall. When it does thanks to the `R.see()` method, the function will check with a scan on the left and right side of the robot where the closest gold token is. if the relative angle between the token and the robot is negative it means that the closest token is on the left side of the robot. This value will trigger a right turn of the robot until it doesen't detect any other gold tokens infront of itself. At that point it will stop turning and it will continue driveing forward. The opposit thing will happen if the detection of the closest gold token returns a positive value. 
    
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
The following gif shows how the robot behaves calling this function:
<img height="200" src="https://github.com/Fabioconti99/RT1_Assignment_1/blob/main/images/turns.gif">

* #### `silver_routine(rot_y_silver,a_th)`
    
    The function `silver_routine(rot_y_silver,a_th)` uses the threshold initialised at the beginning of the main function to create a routine capable of approaching the detected silver tokens. The function will loop until the relative angle between the robot and the silver token will be contained in an angular window defined by the set threshold. Once this condition is met the robot will start driving towards the silver token.
    **Arguments**:
    * *rot_y_silver*: relative angle between the detected silver token and the robot
    * *a_th*: threashold within witch the robot will have to mantain its relative angle between itself and the detected silver token. 
    
    **Returns**:
    * *NONE*
    
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
------------------------------

## The `main()` function

The `main()` function consists of a while loop which at every cycle updates the data regarding the position of the robot inside of the arena. Thanks to this information  the if statements of the function will decide what function is best to call to make the robot behave correctly. 

### flowchart of the `main()` function

<img height="500" src="https://github.com/Fabioconti99/RT1_Assignment_1/blob/main/sr/flow.png">

### Explenation of the different sections of the flow chart:

* **Step 1**:
    At the beginning of the function some it's necessary to declaire some thresholds that will be used later in the code:
    
    * `d_th_silver = 0.4`: distance threshold to grab the silver token
    * `a_th = 2`: Angle trashold within whitch the robot has to be able to go grab the silver token 
    
* **Step 2**: 
    The call of `drive(100,3)` function before the while loop is a way to accelerate the movemnt of the robot right after the spawn. This is a superfluous statement but it helps to accellerate its action.

* **Step 3**: 
    Beginning of the `while(1):` loop.

* **Step 4**: 
    The call of all the functions needed to make the robot aware of its surroundings at every moment during its action.
    There are two different sets of Data about the position of the closest gold token. The only difference between the two is the angle within which the function detects the closest gold token. These sets are used at different points of the code.
    
```python
    d_silver , rot_y_silver = find_silver_token()
    d_gold, rot_y_gold= find_golden_token(60)
    d_gold2, rot_y_gold2= find_golden_token(20)
    gold = gold_token_list(d_silver, d_gold2)
```
* **Step 5**: 
    Thanks to the return of the function `gold_token_list(d_silver, d_gold2)` an if statement can determine whether the gold token is closer to the robot than the detected silver is. The if statement will chose whether the robot will **approach** ( `silver_routine(rot_y_silver,a_th)`) and **grab** `grab_routine()` a silver token or if it will  continue navigate around the arena looking for one of them. 
    
```python
    if(gold):
        
        if (d_gold!=-1 and d_gold<0.7):
            #If the robot gets close to a gold token 
            
            print("turns")
            turns()
            
        else:
            #If the robot doesen't see neither the silver nor the gold token 
             
            drive(75,0.1)
                    
            
    else: 
     #If the robot sees a silver token 

        print (rot_y_silver)
        silver_routine(rot_y_silver,a_th)
        #Aproach to the siver token 

            
        if d_silver < d_th_silver:
        #The robot is within the treashold and it will operate the grab routine

            print ("grab")
            grab_routine()
```

Conclusions and results
-----------
### Video of the robot's performance
This video shows a speeded ap version of the perfromance of the robot during its first lap of the arena: 
<img height="400" src="https://github.com/Fabioconti99/RT1_Assignment_1/blob/main/images/the_whole_run.mp4">

### Possible improvements
During the developing of the code i came up with a few ideas that could make the robot work smoother through out the entire run:
* With the implementation I came up with so far, the robot points the silver tokens with in a little range. A future accomplishment for the project would be being able to view the silver tokens from a way farther distance. This improvement would make the robot start the approach routine earlier making the process of driveing towards the tokens way faster. 
* Another way to improve the proformance of the robot would be 
This project was my first approach to the Python programming language and to the developing of a well structured git repository. Thanks to it, I gained knowledge about to the basic concepts of Python such as creating variables, managing functions, and delivering clear and well structured code that could easily be understood by other developers. I also learnd new skills about the use of [Git](https://git-scm.com) as a distributed control system which I had never worked with.

