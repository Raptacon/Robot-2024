import wpilib

from wpiutil.log import (
    DataLog, BooleanLogEntry, StringLogEntry, FloatLogEntry, IntegerLogEntry, 
)

telemetryEntries = [
    ["AButton", BooleanLogEntry, "/button/letter/a"],
    ["BButton", BooleanLogEntry, "/button/letter/b"],
    ["XButton", BooleanLogEntry, "/button/letter/x"],
    ["YButton", BooleanLogEntry, "/button/letter/y"],
    ["BackButton", BooleanLogEntry, "/button/front/back"],
    ["StartButton", BooleanLogEntry, "/button/front/start"],
    ["LeftBumper", BooleanLogEntry, "/button/bumper/left"],
    ["RightBumper", BooleanLogEntry, "/button/bumper/right"],
    ["LeftStickButton", BooleanLogEntry, "button/stickbutton/left"],
    ["RightStickButton", BooleanLogEntry, "button/stickbutton/right"],
    ["RightTrigger", FloatLogEntry, "button/trigger/right"],
    ["LeftTrigger", FloatLogEntry, "button/trigger/left"],
    ["JoystickLeftY", FloatLogEntry, "button/joystick/lefty"],
    ["JoystickLeftX", FloatLogEntry, "button/joystick/leftx"],
    ["JoystickRightY", FloatLogEntry, "button/joystick/righty"],
    ["JoystickRightX", FloatLogEntry, "button/joystick/rightx"],
    ["DPad", IntegerLogEntry, "button/dpad"]
]

class Telemetry():    
    def __init__(self, 
                 driverController: wpilib.XboxController, 
                 mechController: wpilib.XboxController
                 
                 
                 ):
        self.driverController = driverController
        self.mechController = mechController
        self.datalog = DataLog("log")
        for entryname, entrytype, logname in telemetryEntries:
            setattr(self, "driver" + entryname, entrytype(self.datalog, "driver/" + logname))
            setattr(self, "mech" + entryname, entrytype(self.datalog, "mech/" + logname))

    def getDriverControllerInputs(self):
        self.driverAButton.append(self.driverController.getAButton()) #bool
        self.driverBButton.append(self.driverController.getBButton()) #bool
        self.driverXButton.append(self.driverController.getXButton()) #bool
        self.driverYButton.append(self.driverController.getYButton()) #bool
        self.driverBackButton.append(self.driverController.getBackButton()) #left side , bool
        self.driverStartButton.append(self.driverController.getStartButton()) #right side , bool
        self.driverLeftBumper.append(self.driverController.getLeftBumper()) #bool
        self.driverRightBumper.append(self.driverController.getRightBumper()) #bool
        self.driverLeftStickButton.append(self.driverController.getLeftStickButton()) #bool
        self.driverRightStickButton.append(self.driverController.getRightStickButton()) #bool
        self.driverLeftTrigger.append(self.driverController.getLeftTriggerAxis()) #float 0-1
        self.driverRightTrigger.append(self.driverController.getRightTriggerAxis()) #float 0-1
        self.driverLeftY.append(self.driverController.getLeftY()) #float -1-1
        self.driverLeftX.append(self.driverController.getLeftX()) #float -1-1
        self.driverRightY.append(self.driverController.getRightY()) #float -1-1
        self.driverRightX.append(self.driverController.getRightX()) #float -1-1
        self.driverDPad.append(self.driverController.getPOV()) #ints

    def getMechControllerInputs(self):
        self.mechAButton.append(self.mechController.getAButton()) #bool
        self.mechBButton.append(self.mechController.getBButton()) #bool
        self.mechXButton.append(self.mechController.getXButton()) #bool
        self.mechYButton.append(self.mechController.getYButton()) #bool
        self.mechBackButton.append(self.mechController.getBackButton()) #left side , bool
        self.mechStartButton.append(self.mechController.getStartButton()) #right side , bool
        self.mechLeftBumper.append(self.mechController.getLeftBumper()) #bool
        self.mechRightBumper.append(self.mechController.getRightBumper()) #bool
        self.mechLeftStickButton.append(self.mechController.getLeftStickButton()) #bool
        self.mechRightStickButton.append(self.mechController.getRightStickButton()) #bool
        self.mechLeftTrigger.append(self.mechController.getLeftTriggerAxis()) #float 0-1
        self.mechRightTrigger.append(self.mechController.getRightTriggerAxis()) #float 0-1
        self.mechLeftY.append(self.mechController.getLeftY()) #float -1-1
        self.mechLeftX.append(self.mechController.getLeftX()) #float -1-1
        self.mechRightY.append(self.mechController.getRightY()) #float -1-1
        self.mechRightX.append(self.mechController.getRightX()) #float -1-1
        self.mechDPad.append(self.mechController.getPOV()) #ints
    
    def runDataCollections(self):
        self.getDriverControllerInputs()
        self.getMechControllerInputs()
        