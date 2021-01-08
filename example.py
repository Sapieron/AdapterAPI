"""This file's purpose is to show example usage of AdapterAPI"""

from AdapterAPI import AdapterAPI

#Setup instance of AdapterAPI and provide port name and baudrate to constructor
AdapterHandler = AdapterAPI('/dev/ttyAMA0', 115200)

#Print config of instantianated class
AdapterHandler.CMD_GetCurrentConfig()

#Request an acknowledgement message to be sent from adapter
AdapterHandler.CMD_CheckConnection()

#Moves up to three steppers to specified position in [mm] at the same time
AdapterHandler.CMD_STEPPER_MoveToCoordinate(4444, 652, 10)

#Rotates up to three steppers at the same time with the requested [revs]
AdapterHandler.CMD_STEPPER_Rotate(1234, -9999, 0)

#Resets driver's X, Y and Z stepper motors software position to zero.
#Useful when powering-up the device
AdapterHandler.CMD_STEPPER_SetCurrentPositionAsZero()

#Forces steppers to stop moving.
#@note Current position must be reset (CMD_SetCurrentPositionAsZero) after using that command!
AdapterHandler.CMD_STEPPER_ForceStopMovement()

#Stops all movement - of stepper motors, servos and water pump
AdapterHandler.CMD_ForceStopAll()

#Make food dispenser feed one portion of food
AdapterHandler.CMD_DISPENSER_FeedOnce()

#Feeds 15ml of water
AdapterHandler.CMD_PUMP_FeedWater(15)
