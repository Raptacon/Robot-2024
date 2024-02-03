import wpilib

from wpiutil.log import (
    DataLog, BooleanLogEntry, StringLogEntry, FloatLogEntry, IntegerLogEntry, 
)

telemetryEntries = [
    ["AButton", BooleanLogEntry, "/button/letter/a"],
    ["BButton", BooleanLogEntry, "/button/letter/b"],
    ["XButton", BooleanLogEntry, "/button/letter/x"],
    ["YButton", BooleanLogEntry, "/button/letter/y"],
    ["backButton", BooleanLogEntry, "/button/front/back"],
    ["startButton", BooleanLogEntry, "/button/front/start"],
    ["leftBumper", BooleanLogEntry, "/button/bumper/left"],
    ["rightBumper", BooleanLogEntry, "/button/bumper/right"],
    ["leftStickButton", BooleanLogEntry, "button/stickbutton/left"],
    ["rightStickButton", BooleanLogEntry, "button/stickbutton/right"],
    ["rightTrigger", FloatLogEntry, "button/trigger/right"],
    ["leftTrigger", FloatLogEntry, "button/trigger/left"],
    ["joystickLeftY", FloatLogEntry, "button/joystick/lefty"],
    ["joystickLeftX", FloatLogEntry, "button/joystick/leftx"],
    ["joystickRightY", FloatLogEntry, "button/joystick/righty"],
    ["joystickRightX", FloatLogEntry, "button/joystick/rightx"],
    ["DPad", IntegerLogEntry, "button/dpad"]
]

class Telemetry():    
    def __init__(self, driverController: wpilib.XboxController):
        self.driverController = driverController
        self.datalog = DataLog("log")
        for entryname, entrytype, logname in telemetryEntries:
            setattr(self, entryname, entrytype(self.datalog, logname))

    def getDriverControllerInputs(self):
        self.AButton.append(self.driverController.getAButton()) #bool
        self.BButton.append(self.driverController.getBButton()) #bool
        self.XButton.append(self.driverController.getXButton()) #bool
        self.YButton.append(self.driverController.getYButton()) #bool
        self.backButton.append(self.driverController.getBackButton()) #left side , bool
        self.startButton.append(self.driverController.getStartButton()) #right side , bool
        self.leftBumper.append(self.driverController.getLeftBumper()) #bool
        self.rightBumper.append(self.driverController.getRightBumper()) #bool
        self.leftStickButton.append(self.driverController.getLeftStickButton()) #bool
        self.rightStickButton.append(self.driverController.getRightStickButton()) #bool
        self.leftTrigger.append(self.driverController.getLeftTriggerAxis()) #float 0-1
        self.rightTrigger.append(self.driverController.getRightTriggerAxis()) #float 0-1
        self.leftY.append(self.driverController.getLeftY()) #float -1-1
        self.leftX.append(self.driverController.getLeftX()) #float -1-1
        self.rightY.append(self.driverController.getRightY()) #float -1-1
        self.rightX.append(self.driverController.getRightX()) #float -1-1
        self.Dpad.append(self.driverController.getPOV()) #ints
        