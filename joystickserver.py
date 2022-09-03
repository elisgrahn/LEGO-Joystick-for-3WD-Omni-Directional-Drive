#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor, TouchSensor
from pybricks.parameters import Port, Stop, Color
from pybricks.tools import wait
from pybricks.media.ev3dev import SoundFile
from pybricks.messaging import BluetoothMailboxServer, TextMailbox
import math

# Initialize the EV3 brick
ev3 = EV3Brick()

# Initialize the mailbox
joystick = BluetoothMailboxServer()
server = TextMailbox('address', joystick)

# Define axes
axisA = Motor(Port.B) # Angular axis
axisX = Motor(Port.D) # Linear x-axis
axisY = Motor(Port.C) # Linear y-axis

# Define constants
PI = math.pi        # No comment
MAX_SPEED = 1000    # The maximum speed for motors (degree/s)
MIN_SPEED = 150     # The minimum speed for motors (Motor will turn off if given speed is lower)
DEADZONE = 0.4      # A factor between 0 and 1, if axis's position is less than it, that makes its position 0

# Define functions
def config(axis):

    # Configures the specified axis
    axis.reset_angle(0) # Set starting angle to 0

    # Rotate to positive max
    axis.run_until_stalled(20, then=Stop.COAST, duty_limit=40)  # Rotate as far as possible on axis
    wait(100)                                                   # Wait 100 ms
    positive = axis.angle()                                     # Get the positive max angle

    # Rotate to negative max
    axis.run_until_stalled(-20, then=Stop.COAST, duty_limit=40) # Rotate as far as possible on axis
    wait(100)                                                   # Wait 100 ms
    negative = axis.angle()                                     # Get the negative max angle

    # Calculate and rotate to center
    center = round((positive + negative)/2) # Calculate mean value, therfore center
    axis.run_target(20, center)             # Rotate back to center
    wait(100)                               # Wait 100 ms
    
    # Reset
    axis.reset_angle(0) # Reset center to angle 0
    axis.stop()         # Turn off motor
    
    # Returns the max angle for that axis
    return round(abs(positive-negative)/2)

def get_pos(axis, max_angle):

    # Calculates position of axis
    position = axis.angle() / max_angle
    return position

def calc_speed(angular, linear, drive_dir, angle):

    # Calculates speed based on desired angular and linear speed
    if(angle == None): speed = round(angular)   # No linear angle, means rotate on the spot, means run just the angular speed on wheels
    else: speed = round(angular + linear * math.cos(drive_dir - angle)) # Linear speed for each wheel is based on the wheels drivedirection and the desired drive angle

    # The fact that angular speed overrides linear speed is on purpouse,
    # the robot should be capable of driving linearly to then start rotating
    # on the spot if the user pushes the angular joystick far enough

    if(-MIN_SPEED < speed < MIN_SPEED): return '0'      # If resulting speed is lower than the minimum speed, don't drive that motor
    return str(max(min(speed, MAX_SPEED), -MAX_SPEED))  # Caps the value so that the speed never gets too big

# Tell user not to touch joystick while it is configuring 
ev3.speaker.set_volume(100, which='PCM')    # Max volume
ev3.speaker.play_file(SoundFile.NO)
ev3.speaker.play_file(SoundFile.TOUCH)

# Configure each axis by checking how far each axis can rotate and get max angle for that axis
max_angleA = config(axisA)
max_angleX = config(axisX)
max_angleY = config(axisY)

ev3.speaker.play_file(SoundFile.SEARCHING)  # Play a sound to confirm that the joystick is searching
joystick.wait_for_connection()              # Wait for connection with robot
ev3.speaker.play_file(SoundFile.CONFIRM)    # Play a sound to confirm bluetooth connection

# The angular speed is rotation on the spot while
# linear speed is in a set direction given by the
# angle that the xy-joystick is at

# Drivedirection is the angle that the wheel is at, an offset

a,y,x = 0,0,0   # Positions
angular = 0     # Angular speed
linear = 0      # Linear speed
angle = None    # Desired linear angle

while(True):

    # Gets a value between -1 and 1 representing the rotation of each axis
    a = get_pos(axisA, max_angleA)  # Angular position
    x = get_pos(axisX, max_angleX)  # Linear x position
    y = get_pos(axisY, max_angleY)  # Linear y position

    # Angular speed is decided by how far the angular axis has turned, is 0 if inside deadzone
    if(-DEADZONE < a < DEADZONE): angular = 0
    else: angular = a * MAX_SPEED

    # If hypotenuse of x and y is longer than deadzone-radius, get desired linear angle through arctan
    if(-DEADZONE < (x**2 + y**2)**0.5 < DEADZONE):
        angle = None
        linear = 0

    else:
        angle = math.atan2(x,y)         # atan2 gives the exact angle, even if x or y are negative, x/y since angle 0 is "forward" 
        if(angle < 0): angle += 2*PI        # +2*PI for negative angles since atan2 returns angles between -PI and PI
        angle = round(angle/(PI/6))*(PI/6)  # Rounds the angle to the nearest multiple of 30 degrees, this makes it easier to steer

        linear = MAX_SPEED  # Linear speed is maxspeed if outside deadzone

    # Calculate each motor speed based on angular- and linear speed, wheel drivedirection and, desired linear angle
    speedA = calc_speed(angular, linear, 5*(PI/6), angle)
    speedB = calc_speed(angular, linear, (PI/6), angle)
    speedC = calc_speed(angular, linear, 3*(PI/2), angle)

    # Send to robot's mailbox
    try: server.send(speedA+' '+speedB+' '+speedC)      # Try to send motor speed information to robot
    except: 
        ev3.speaker.play_file(SoundFile.ERROR_ALARM)    # Couldn't send info, must have lost connection
        break   # Quit program

    wait(100)   # Loop 10 times a second