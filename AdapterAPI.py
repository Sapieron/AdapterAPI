
__author__ = "Pawel Klisz"
__copyright__ = "Copyright 2020"

__license__ = "GPL"
__version__ = "0.1.0"
__maintainer__ = "Pawel Klisz"
__email__ = "pawelochojec@gmail.com"
__status__ = "Beta"

"""NOTE Please refer to README.md in order to get familiar with following interface"""

from enum import Enum

import colored_traceback.auto
import serial

################################################################################
#                                Code
################################################################################


class AdapterAPI:
    def __init__(self,
                 _port="/dev/ttyAMA0",
                 _baudrate=115200,
                 _timeout=1):
        self._correctFrameSize = 21
        self._defaultFrame  = "TTTTTTTTTTTTTTTTTTT\n\r"
        if len(self._defaultFrame) != self._correctFrameSize:
            raise ValueError("Frame size cannot be different then", self._correctFrameSize)

        self._port          = _port
        self._baudrate      = _baudrate
        self._timeout       = _timeout
        self._testedPort    = serial.Serial(self._port,
                                            self._baudrate,
                                            timeout= self._timeout)
        self._defaultFrame  = [ord(c) for c in self._defaultFrame]

    def CMD_GetCurrentConfig(self):
        """@brief Prints current port config to terminal"""
        print("Requested to print current port config:")
        print("Selected port:     ", self._port)
        print("Selected baudrate: ", self._baudrate)
        print("Selected timeout:  ", self._timeout, "s")

    def CMD_CheckConnection(self):
        """@brief Sends acknowledgement command

        @return True if succeeded, False if not succeeded

        @remark It's a blocking function!"""
        frame = self._commandFactory(self).BuildSayHelloWorld()
        print("Requested Hello World on ", self._port)
        self._testedPort.write(frame)
        line = self._testedPort.readline()
        if line == b"":
            print("Timeout occured on ", self._port)
            return False
        else:
            print("Received Hello World on ", self._port, ":")
            print(line)
            return True

    def CMD_ForceStopAll(self):
        """@brief Forces to stop every movement of steppers,
           servos and pump

           @return True if succedded, False if not succeeded"""
        frame = self._commandFactory(self).BuildForceStopAll()
        self._testedPort.write(frame)
        #TODO check if received NOK or OK

    def CMD_STEPPER_MoveToCoordinate(self,
                                     X,
                                     Y,
                                     Z):
        """@brief Moves controlled cartesian coordinate system to specified position for 3 axis'\n
        @param X - coordinate in [mm] to which stepper should move in X axis.
        Must be in range of -9999 to 9999\n
        @param Y - coordinate in [mm] to which stepper should move in Y axis.
        Must be in range of -9999 to 9999\n
        @param Z - coordinate in [mm] to which stepper should move in Z axis.
        Must be in range of -9999 to 9999"""
        frame = self._commandFactory(self).BuildMoveToCoordinate(X, Y, Z)
        self._testedPort.write(frame)

    def CMD_STEPPER_Rotate(self,
                           X,
                           Y,
                           Z):
        """@brief Rotates stepper motors by a specified number of rotations at the same time\n
        @param X - number of rotations which should be done on X axis.
        Must be in range of -9999 to 9999\n
        @param Y - number of rotations which should be done on Y axis.
        Must be in range of -9999 to 9999\n
        @param Z - number of rotations which should be done on Z axis.
        Must be in range of -9999 to 9999"""
        frame = self._commandFactory(self).BuildRotateStepper(X, Y, Z)
        self._testedPort.write(frame)

    def CMD_STEPPER_SetCurrentPositionAsZero(self):
        """@brief Sets current position of stepper motors to be zeroed. Useful after power-up"""
        frame = self._commandFactory(self).BuildSetCurrentPositionAsZero()
        self._testedPort.write(frame)

    def CMD_STEPPER_ForceStopMovement(self):
        """@brief Forces to stop every movement of steppers

           @return True if succedded, False if not succeeded"""
        frame = self._commandFactory(self).BuildForceStopMovement()
        self._testedPort.write(frame)
        #TODO check if received NOK or OK

    def CMD_DISPENSER_Rotate(self,
                             FoodA,
                             FoodB):
        """@brief Rotates food dispensers by a set number or rotations\n
           @param FoodA - number or rotations to be done by FoodA dispenser.
           Must be in range of -9999 to 9999\n
           @param FoodB - number or rotations to be done by FoodB dispenser.
           Must be in range of -9999 to 9999"""
        frame = self._commandFactory(self).BuildRotateFoodDispenser(FoodA, FoodB)
        self._testedPort.write(frame)

    def CMD_PUMP_RotateForMs(self,
                             time):
        """@brief Rotates pump for desired time in [ms]\n
           @param time - time in [ms] for which pump will be on.
           Must be in range of -9999 to 9999"""
        frame = self._commandFactory(self).BuildRotateWaterPump(time)
        self._testedPort.write(frame)

    def CMD_PUMP_FeedWater(self,
                           mililiters):
        """@brief Turns on water pump to pump desired amount of water in [ml]\n
           @param mililiters - amount of water to be pumped in [ml].
           Must be in range of -9999 to 9999"""
        frame = self._commandFactory(self).BuildFeedWater(mililiters)
        self._testedPort.write(frame)


    class _commandTags(Enum):
        SayHelloWorld            = 0x30
        MoveToCoordinate         = 0x31
        RotateStepper            = 0x32
        SetCurrentPositionAsZero = 0x33
        ForceStopMovement        = 0x34
        ForceStopAll             = 0x35
        RotateFoodDispenser      = 0x36
        RotateWaterPump          = 0x37
        FeedWater                = 0x38

    class _commandFactory:
        def __init__(self, master):
            self._master = master

        def BuildSayHelloWorld(self):
            frame    = self._master._defaultFrame[:]
            frame[0] = self._master._commandTags.SayHelloWorld.value
            return bytes(frame)

        def BuildMoveToCoordinate(self,
                                  X,
                                  Y,
                                  Z):
            X = int(X)
            Y = int(Y)
            Z = int(Z)
            self._CheckIfValueFits(X, Y, Z)

            frame    = self._master._defaultFrame[:]
            frame[0] = self._master._commandTags.MoveToCoordinate.value
            frame[1] = ord('X')
            if int(X < 0 ):
                frame[2] = ord("-")
            else:
                frame[2] = ord("+")
            X = abs(X)
            frame[3] = int(X / 1000) + 0x30
            frame[4] = int((X % 1000) / 100) + 0x30
            frame[5] = int((X % 100) / 10) + 0x30
            frame[6] = X % 10 + 0x30

            frame[7] = ord('Y')
            if int(Y < 0 ):
                frame[8] = ord("-")
            else:
                frame[8] = ord("+")
            Y = abs(Y)
            frame[9] = int(Y / 1000) + 0x30
            frame[10] = int((Y % 1000) / 100) + 0x30
            frame[11] = int((Y % 100) / 10) + 0x30
            frame[12] = Y % 10 + 0x30

            frame[13] = ord('Z')
            if int(Z < 0 ):
                frame[14] = ord("-")
            else:
                frame[14] = ord("+")
            Z = abs(Z)
            frame[15] = int(Z / 1000) + 0x30
            frame[16] = int((Z % 1000) / 100) + 0x30
            frame[17] = int((Z % 100) / 10) + 0x30
            frame[18] = Z % 10 + 0x30

            return bytes(frame)

        def BuildRotateStepper(self,
                        X,
                        Y,
                        Z):
            X = int(X)
            Y = int(Y)
            Z = int(Z)
            self._CheckIfValueFits(X, Y, Z)

            frame    = self._master._defaultFrame[:]
            frame[0] = self._master._commandTags.RotateStepper.value
            frame[1] = ord('X')
            if int(X < 0 ):
                frame[2] = ord("-")
            else:
                frame[2] = ord("+")
            X = abs(X)
            frame[3] = int(X / 1000) + 0x30
            frame[4] = int((X % 1000) / 100) + 0x30
            frame[5] = int((X % 100) / 10) + 0x30
            frame[6] = X % 10 + 0x30

            frame[7] = ord('Y')
            if int(Y < 0 ):
                frame[8] = ord("-")
            else:
                frame[8] = ord("+")
            Y = abs(Y)
            frame[9] = int(Y / 1000) + 0x30
            frame[10] = int((Y % 1000) / 100) + 0x30
            frame[11] = int((Y % 100) / 10) + 0x30
            frame[12] = Y % 10 + 0x30

            frame[13] = ord('Z')
            if int(Z < 0 ):
                frame[14] = ord("-")
            else:
                frame[14] = ord("+")
            Z = abs(Z)
            frame[15] = int(Z / 1000) + 0x30
            frame[16] = int((Z % 1000) / 100) + 0x30
            frame[17] = int((Z % 100) / 10) + 0x30
            frame[18] = Z % 10 + 0x30

            return bytes(frame)

        def BuildSetCurrentPositionAsZero(self):
            frame    = self._master._defaultFrame[:]
            frame[0] = self._master._commandTags.SetCurrentPositionAsZero.value
            return bytes(frame)

        def BuildForceStopMovement(self):
            frame    = self._master._defaultFrame[:]
            frame[0] = self._master._commandTags.ForceStopMovement.value
            return bytes(frame)

        def BuildForceStopAll(self):
            frame    = self._master._defaultFrame[:]
            frame[0] = self._master._commandTags.ForceStopAll.value
            return bytes(frame)

        def BuildRotateFoodDispenser(self,
                                     FoodA,
                                     FoodB):
            FoodA = int(FoodA)
            FoodB = int(FoodB)
            self._CheckIfValueFits(FoodA, FoodB)

            frame    = self._master._defaultFrame[:]
            frame[0] = self._master._commandTags.RotateFoodDispenser.value
            frame[1] = ord("A")
            if int(FoodA < 0 ):
                frame[2] = ord("-")
            else:
                frame[2] = ord("+")
            FoodA = abs(FoodA)
            frame[3] = int(FoodA / 1000) + 0x30
            frame[4] = int((FoodA % 1000) / 100) + 0x30
            frame[5] = int((FoodA % 100) / 10) + 0x30
            frame[6] = FoodA % 10 + 0x30

            frame[7]  = ord("B")
            if int(FoodB < 0 ):
                frame[8] = ord("-")
            else:
                frame[8] = ord("+")
            FoodB = abs(FoodB)
            frame[9]  = int(FoodB / 1000) + 0x30
            frame[10] = int((FoodB % 1000) / 100) + 0x30
            frame[11] = int((FoodB % 100) / 10) + 0x30
            frame[12] = FoodB % 10 + 0x30

            return bytes(frame)

        def BuildRotateWaterPump(self,
                                 time):
            frame    = self._master._defaultFrame[:]
            frame[0] = self._master._commandTags.RotateWaterPump.value

            self._CheckIfValueFits(time)

            frame[1] = ord("W")
            if int(time < 0 ):
                raise ValueError("Time of rotation cannot be a negative value")
            else:
                frame[2] = ord("+")

            time = abs(time)
            frame[3] = int(time / 1000) + 0x30
            frame[4] = int((time % 1000) / 100) + 0x30
            frame[5] = int((time % 100) / 10) + 0x30
            frame[6] = time % 10 + 0x30

            return bytes(frame)

        def BuildFeedWater(self,
                           mililiters):
            frame    = self._master._defaultFrame[:]
            frame[0] = self._master._commandTags.FeedWater.value

            self._CheckIfValueFits(mililiters)

            frame[1] = ord("W")
            if int(mililiters < 0 ):
                raise ValueError("Water amount to be pumped cannot be a negative value")
            else:
                frame[2] = ord("+")

            mililiters = abs(mililiters)
            frame[3] = int(mililiters / 1000) + 0x30
            frame[4] = int((mililiters % 1000) / 100) + 0x30
            frame[5] = int((mililiters % 100) / 10) + 0x30
            frame[6] = mililiters % 10 + 0x30

            return bytes(frame)

        def _CheckIfValueFits(self,
                              *argv):
            lowerBorderValue  = -9999
            higherBorderValue = 9999
            for arg in argv:
                if arg < lowerBorderValue or arg > higherBorderValue:
                    raise ValueError(f"Value must be in range {lowerBorderValue} to {higherBorderValue}")
