import commands2
import wpilib
from utils.leds import Strip

class Leds(commands2.Subsystem):
    kLEDBuffer = 36 #one side temp
    def __init__(self):
        self.leds = wpilib.AddressableLED(0)
        self.ledData = [wpilib.AddressableLED.LEDData() for _ in range(self.kLEDBuffer)]
        self.currentHue = 243
        self.currentBright = 0
        #9 LED frontRight 9 LED frontRight
        self.strips = {}
        #Right Front - first 9 in order
        self.strips["frontRight"]= Strip(self.ledData[0:9], "fr")
        #Right Read- 2nd 9 in reverse order
        self.strips["rearRight"]= Strip(self.ledData[9:18][::-1], "rr")
        #Left 3rd set of 9 in order
        self.strips["rearLeft"] = Strip(self.ledData[18:27], "rl")
        #Left 4th set of 9 reverse order
        self.strips["frontLeft"] = Strip(self.ledData[27:36][::-1], "fl")
        self.strips["frontRight"].setTeamColor()
        self.strips["frontLeft"].setTeamColor()
        self.strips["rearLeft"].setRainbowHue()
        self.strips["rearRight"].setRainbowHue()

        #Confiugure the LED strip
        self.leds.setLength(self.kLEDBuffer)
        self.leds.setData(self.ledData)
        self.leds.start()


    def getStrip(self, name: str) -> Strip:
        if name in self.strips:
            return self.strips[name]
        return None

    def periodic(self):
        for name,strip in self.strips.items():
            strip.periodic()

        # Set the LEDs
        self.leds.setData(self.ledData)
