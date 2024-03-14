from wpilib import DigitalInput
import logging
import traceback

log = logging.getLogger("breakBeamFactory")

def createBreakBeam(DIOport : int):
    """
    Call this to create a break beam on the given DIO port.
    DIO ports are found on the RoboRIO
    Call the DigitalInput.get() to determine if the breakbeam sees something
    """
    try:
        breakBeam = DigitalInput(DIOport)
        return breakBeam
    except Exception as e:
        log.error(f"Failed to create breakBeam for DIO port {DIOport}")
        log.error(f"Error caught: {e}")
        traceback.print_exception(e)
        return None
