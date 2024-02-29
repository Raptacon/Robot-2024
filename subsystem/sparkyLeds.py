import commands2
import wpilib
from utils.leds import Strip

class Leds(commands2.Subsystem):
    kLEDBuffer = 18 #one side temp
    def __init__(self):
        self.leds = wpilib.AddressableLED(0)
        self.ledData = [wpilib.AddressableLED.LEDData() for _ in range(self.kLEDBuffer)]
        self.currentHue = 243
        self.currentBright = 0
        #9 LED right 9 LED right
        self.strips = {}
        #Right - first 9 in order
        self.strips["right"]= Strip(self.ledData[0:9])
        #Left 2nd set of 9 reverse order
        self.strips["left"] =  Strip(self.ledData[9:18][::-1])
        self.strips["right"].setTeamColor()
        self.strips["left"].setTeamColor()

        #Confiugure the LED strip
        self.leds.setLength(self.kLEDBuffer)
        self.leds.setData(self.ledData)
        self.leds.start()

        
    def getStrip(self, name: str) -> Strip:
        if name in self.strips:
            return self.strips[name]
        return None

    def periodic(self):
        if not wpilib.RobotController.isSysActive() and not wpilib.DriverStation.isDisabled():
            self.strips["left"].setErrorMode(True, [255,255,0], [0,0,0])
            self.strips["right"].setErrorMode(True, [0,0,0], [255,255,0])
        else:
            self.strips["left"].setErrorMode(False)
            self.strips["right"].setErrorMode(False)

        for name,strip in self.strips.items():
            strip.periodic()

        # Set the LEDs
        self.leds.setData(self.ledData)
