#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor
from pybricks.parameters import Port
from pybricks.tools import wait
from pybricks.media.ev3dev import SoundFile
from pybricks.messaging import BluetoothMailboxClient, TextMailbox

# Initialize the EV3 brick
ev3 = EV3Brick()

# Initialize the mailbox
robot = BluetoothMailboxClient()
server = TextMailbox('address', robot)

# Define the motors
motorA = Motor(Port.B)  # Left motor
motorB = Motor(Port.D)  # Right motor
motorC = Motor(Port.C)  # Rear motor

# Define functions
def decode(string):

    # Decodes the instructions sent from the joystick    
    speeds = string.split() # Turn string into list

    a = int(speeds[0])  # Left
    b = int(speeds[1])  # Right
    c = int(speeds[2])  # Rear

    return a,b,c

def run_motor(motor, speed):

    # Runs the specified motor at the given speed
    if(speed == 0): motor.stop()    # No speed, turn off motor
    else: motor.run(speed)          # Run motor at speed

# Connect to mailbox
robot.connect('hawking')                    # Search for the joystick and connect to it
ev3.speaker.play_file(SoundFile.CONFIRM)    # Play a sound to confirm bluetooth connection

while(True):

    # Wait for message to be delivered to mailbox
    server.wait()

    # Read the mailbox
    message = server.read()

    # Decodes message into speeds
    speedA, speedB, speedC = decode(message)
    
    # Run motors at their speed
    run_motor(motorA, speedA)    # Left
    run_motor(motorB, speedB)    # Right
    run_motor(motorC, speedC)    # Rear