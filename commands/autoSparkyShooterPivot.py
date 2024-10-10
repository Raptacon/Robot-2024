from subsystem.sparkyShooterPivot import ShooterPivot
import commands2
from enum import Enum

class AutoShooterPivot(commands2.CommandBase):
    def __init__(self, pivot : ShooterPivot, position : str) -> None:
        super().__init__()
        self.pivot = pivot
        self.position = position

    def initialize(self) -> None:
        match self.position:
            case ShooterPositions.LOADING.value:
                self.pivot.setLoading()
            case ShooterPositions.AMP.value:
                self.pivot.setAmp()
            case ShooterPositions.CLIMB.value:
                self.pivot.setClimb()
    
    def isFinished(self) -> bool:
        return self.pivot.getController().atSetpoint()
    
class ShooterPositions(Enum):
    LOADING = "loading",
    AMP = "amp",
    CLIMB = "climb",