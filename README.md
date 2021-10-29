# [Research_Track_1](https://unige.it/en/off.f/2021/ins/51201.html?codcla=10635) , [Robotics Engineering](https://courses.unige.it/10635) ([UNIGE](https://unige.it/it/)) : First assignement.
## Python Robotics Simulator.
### Professor. [Carmine Ricchiuto](https://github.com/CarmineD8).

-----------------------

Project objectives
--------------------

The aim of this project was to code a Python script <code><img height="20" src="https://github.com/Fabioconti99/my_Research_Track/blob/main/images/python.png"></code> capable of making holonomic robot ![alt text](https://github.com/Fabioconti99/my_Research_Track/blob/main/sr/robot.png) behave correctly inside of a given environment. 
Thanks to the simulator we used for the assignement (developed by [Student Robotics](https://studentrobotics.org)), the robot will spawn inside of an arena composed of squared tokens of two different colors:
* The **gold tokens** ![alt text](https://github.com/Fabioconti99/my_Research_Track/blob/main/sr/token_gold.png) rappresent the wall of the maze the robot had to navigate in. 
* The **silver tokens** ![alt text](https://github.com/Fabioconti99/my_Research_Track/blob/main/sr/token_silver.png) rappresent the objects the robot has to interact with.

The behavior of the robot has to stand by the following rules:
* constantly driving the robot around the environment in the counter-clockwise direction,
* Avoiding the gold tokens, 
* And once the robot will get close enough to a silver token placed inside the environment, grabbing it and moves it behind itself.

Picture of the **Enviroment**:
![alt text](https://github.com/Fabioconti99/my_Research_Track/blob/main/images/arena.png) 

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

### The Grabber ###


The robot is equipped with a grabber, capable of picking up a token which is in front of the robot and within 0.4 metres of the robot's centre. To pick up a token, call the `R.grab` method:

```python
success = R.grab()
```

The `R.grab` function returns `True` if a token was successfully picked up, or `False` otherwise. If the robot is already holding a token, it will throw an `AlreadyHoldingSomethingException`.

To drop the token, call the `R.release` method.

Cable-tie flails are not implemented.

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


Conclusions
-----------
This project was my first approach to the Python programming language and to the developing a well structured git repository. Thanks to it, I gained some knowledge about to the basic concepts of Python such as creating variables, managing functions, and delivering clear and well structured code that could be easily understood by other developers. 

