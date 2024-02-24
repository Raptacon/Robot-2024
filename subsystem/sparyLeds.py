import commands2
import wpilib

class Leds(commands2.Subsystem):
    kLEDBuffer = 9 #one side temp
    def __init__(self):
        self.leds = wpilib.AddressableLED(0)
        self.ledData = [wpilib.AddressableLED.LEDData() for _ in range(self.kLEDBuffer)]
        self.currentHue = 243
        self.currentBright = 0

        #Confiugure the LED strip
        self.leds.setLength(self.kLEDBuffer)
        self.leds.setData(self.ledData)
        self.leds.start()

        
    def periodic(self):
        if wpilib.DriverStation.getAlliance() == wpilib.DriverStation.Alliance.kBlue:
            self.currentHue = 243
        else:
            self.currentHue = 360
        # Fill the buffer with a rainbow
        #self.currentHue = rainbow(self.ledData, self.currentHue)
        self.currentBright = rainbowBright(self.ledData, self.currentHue, self.currentBright)
        # Set the LEDs
        self.leds.setData(self.ledData)



def rainbow(leds: [wpilib.AddressableLED.LEDData], currentHue: float):
    """
    Pass in the LEDs array and the current hue to animate a rainbow
    The new next hue is passed out
    """
    # For every pixel
    for i in range(len(leds)):
        # Calculate the hue - hue is easier for rainbows because the color
        # shape is a circle so only one value needs to precess
        hue = (currentHue + (i * 180 / len(leds))) % 180

        # Set the value
        leds[i].setHSV(int(hue), 255, 128)

    # Increase by to make the rainbow "move"
    currentHue += 3

    # Check bounds
    return currentHue % 180

def rainbowBright(leds: [wpilib.AddressableLED.LEDData], hue: float, currentBright, step: float = 16):
    """
    Pass in the LEDs array and the current hue to animate a rainbow
    The new next hue is passed out
    """
    # For every pixel
    for i in range(len(leds)):
        # Calculate the hue - hue is easier for rainbows because the color
        # shape is a circle so only one value needs to precess
        bright = (currentBright + (i * 180 / len(leds))) % 255

        # Set the value
        leds[i].setHSV(int(hue), 255, int(bright))

    # Increase by to make the rainbow "move"
    currentBright += step

    # Check bounds
    return currentBright % 255