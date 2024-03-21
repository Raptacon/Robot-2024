import wpilib
from enum import Enum
import random

class Mode(Enum):
    RAINBOWHUE = 0
    RAINBOWBRIGHT = 1
    BLINK = 2
    FLASH = 3
    STATIC = 4
    RANDOM = 5

class Strip():
    def __init__(self, strip: list[wpilib.AddressableLED.LEDData],
                 name: str,
                 mode: Mode = Mode.RAINBOWBRIGHT,
                 hsv: list[int, int, int] = [243, 255, 128],
                 rgbP: list[int, int, int] = [0, 255, 0],
                 rgbS: list[int,int,int] = [255,255,255]):
        self.strip = strip
        self.name = name
        self.hsv = hsv[:]
        self.rgbPrimary = rgbP[:]
        self.rgbSecondary = rgbS[:]
        self.mode = mode

        self.ledPeriodicRate = 1.0
        self.fadeRate = 8
        self.rateS = 1.0 #default LED effects 1/s
        self.dutyCycle = 0.5
        self.timer = wpilib.Timer()
        self.timer.start()

    def periodic(self):
        match self.mode:
            case Mode.RAINBOWHUE:
                self.hsv[0] = rainbowHue(self.strip, self.hsv[0], self.hsv[1], self.hsv[2])
            case Mode.RAINBOWBRIGHT:
                self.hsv[2] = rainbowValue(self.strip, self.hsv[0], self.hsv[1], self.hsv[2], self.fadeRate)
            case Mode.BLINK |  Mode.FLASH | Mode.STATIC:
                blink(self.strip, self.timer, self.rateS, self.dutyCycle, self.rgbPrimary, self.rgbSecondary)
            case Mode.RANDOM:
                randomLeds(self.strip, self.timer, self.rateS)


    def getDefaultHue(self):
        if wpilib.DriverStation.getAlliance() == wpilib.DriverStation.Alliance.kBlue:
            return 243 #HSV Blue
        else:
            return 360 #HSV Red
    def getDefaultRgb(self):
        if wpilib.DriverStation.getAlliance() == wpilib.DriverStation.Alliance.kBlue:
            return [0, 0, 255]
        else:
            return [255, 0, 0]

    def setRainbowHue(self, startingHue: float = 0, saturation: float = 255, value: float = 128):
        self.hue = startingHue
        self.saturation = saturation
        self.value = value
        self.mode = Mode.RAINBOWHUE

    def setRainbowValue(self, startingHue: float = 0, saturation: float = 255, value: float = 128):
        self.hue = startingHue
        self.saturation = saturation
        self.value = value
        self.mode = Mode.RAINBOWBRIGHT
    def setBlink(self, rgb: list[int, int, int], rateS = 1.0, dutyCycle: float = 0.5):
        self.timer.reset()
        self.rateS = rateS
        self.dutyCycle = dutyCycle
        self.rgbPrimary = rgb
        self.rgbSecondary = [0,0,0]
        self.mode = Mode.BLINK
    def setFlash(self, OnRgb: list[int, int, int], OffRgb: list[int, int, int], rateS = 1.0, dutyCycle: float = 0.5):
        self.timer.reset()
        self.rateS = rateS
        self.dutyCycle = dutyCycle
        self.rgbPrimary = OnRgb
        self.rgbSecondary = OffRgb
        self.mode = Mode.FLASH
    def setStatic(self, rgb: list[int,int,int]):
        self.dutyCycle = 1.0
        self.rateS = 1.0
        self.rgbPrimary = rgb
        self.mode = Mode.STATIC
    def setRandom(self, rateS: float):
        self.dutyCycle = 1.0
        self.rateS = rateS
        self.mode = Mode.RANDOM
    def setTeamColor(self, chase = True):
        if chase:
            self.setRainbowValue(self.getDefaultHue(), 255, 128)
        else:
            self.setStatic(self.getDefaultRgb())


def rainbowHue(leds: list[wpilib.AddressableLED.LEDData], currentHue: float, saturation: float = 255, value: float = 128):
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
        leds[i].setHSV(int(hue), saturation, value)

    # Increase by to make the rainbow "move"
    currentHue += 3

    # Check bounds
    return currentHue % 180

def rainbowValue(leds: [wpilib.AddressableLED.LEDData], hue: int = 360, saturation: int = 255, startingValue: int = 0, step: float = 16):
    """
    Pass in the LEDs array and the current hue to animate a rainbow
    The new next hue is passed out
    """
    # For every pixel
    for i in range(len(leds)):
        # Calculate the hue - hue is easier for rainbows because the color
        # shape is a circle so only one value needs to precess
        value = (startingValue + (i * 180 / len(leds))) % 255

        # Set the value
        leds[i].setHSV(int(hue), int(saturation), int(value))

    # Increase by to make the rainbow "move"
    startingValue += step

    # Check bounds
    return startingValue % 255

def blink(leds: list[wpilib.AddressableLED.LEDData], timer: wpilib.Timer, rateS: float = 1.0, dutyCycle: float = 0.5, onRgb: list[int,int,int] = [0,255,0], offRgb: [int, int, int] = [0,0,0]):
    #check for rollover
    if timer.get() > rateS:
        timer.reset()

    #determine if should be on or off
    rgb = offRgb
    if timer.get() < rateS * dutyCycle:
        rgb = onRgb

    for led in leds:
        led.setRGB(*rgb)

def randomLeds(leds: list[wpilib.AddressableLED.LEDData], timer: wpilib.Timer, rateS: float = 1.0):
    if timer.get() < rateS:
        return
    timer.reset()

    for led in leds:
        led.setRGB(random.randint(0,255), random.randint(0,255), random.randint(0,255))
