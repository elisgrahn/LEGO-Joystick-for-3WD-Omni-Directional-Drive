#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, InfraredSensor)
from pybricks.parameters import Port, Button
from pybricks.media.ev3dev import SoundFile

# Initialize the EV3 brick
ev3 = EV3Brick()

# Define infrared sensor
ir = InfraredSensor(Port.S4)  # Av någon anledning viktigt att det är just port 4
ir.mode = 'IR-REMOTE'

# Define the motors
motorA = Motor(Port.B)  # Left motor
motorB = Motor(Port.D)  # Right motor
motorC = Motor(Port.C)  # Rear motor

FULL_SPEED = 1000    # The maximum speed for motors (degree/s)
HALF_SPEED = 500

# Altert user that robot is ready6a
ev3.speaker.play_file(SoundFile.CONFIRM)

while(True):

    pressed = ir.keypad()

    left_up = False
    right_up = False
    left_down = False
    right_down = False

    if(Button.LEFT_UP in pressed): left_up = True
    if(Button.RIGHT_UP in pressed): right_up = True
    if(Button.LEFT_DOWN in pressed): left_down = True
    if(Button.RIGHT_DOWN in pressed): right_down = True

    if(left_up):
        # Drifta fram vänster
        motorA.run(-FULL_SPEED)
        motorB.run(FULL_SPEED)
        motorC.run(HALF_SPEED)

    elif(left_down):
        # Snett bak vänster
        motorA.run(FULL_SPEED)
        motorB.stop()
        motorC.run(-FULL_SPEED)

    elif(right_up):
        # Drifta fram höger
        motorA.run(-FULL_SPEED)
        motorB.run(FULL_SPEED)
        motorC.run(-HALF_SPEED)

    elif(right_down):
        # Snett bak höger
        motorA.stop()
        motorB.run(-FULL_SPEED)
        motorC.run(FULL_SPEED)

    elif(left_up and right_up): 
        # Framåt
        motorA.run(-FULL_SPEED)
        motorB.run(FULL_SPEED)
        motorC.stop()

    elif(left_down and right_down):
        # Bakåt
        motorA.run(FULL_SPEED)
        motorB.run(-FULL_SPEED)
        motorC.stop()

    elif(left_up and left_down):
        # Rotera vänster
        motorA.run(FULL_SPEED)
        motorB.run(FULL_SPEED)
        motorC.run(FULL_SPEED)
        

    elif(right_up and right_down):
        # Rotera höger
        motorA.run(-FULL_SPEED)
        motorB.run(-FULL_SPEED)
        motorC.run(-FULL_SPEED)

    else:
        # Stanna
        motorA.stop()   
        motorB.stop()
        motorC.stop()   