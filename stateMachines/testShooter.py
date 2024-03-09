from stateMachines.stateMachine import *
import wpilib
from subsystem.sparkyShooter import Shooter
from subsystem.sparkyShooterPivot import ShooterPivot


class TestShooterStateMachine(StateMachine):
    def __init__(self, debugMode=False, shooter:Shooter=None, shooterPivot:ShooterPivot=None):
        self.debugTimer = wpilib.Timer()
        self.debugTimer.start()

        self.shooter = shooter
        self.shooterPivot = shooterPivot

        states = []
        
        standby = State(
            name="Standby",
        )
        states.append(standby)

        lower = State(
            name="Lower",
            enter=lambda: self.debugTimer.reset(),
            run=lambda: self.shooterPivot.setLoading(),
            transition=lambda: "Wait" if self.shooterPivot.getController().getPositionError() < 0.1 else "" #idk if this will work
        )
        states.append(lower)

        wait = State(
            name="Wait"
            #in real code, this would have some emergency exit transition.
        )
        states.append(wait)

        handoff = State(
            name = "Handoff",
            run=lambda: self.shooter.runIntake(0.4),
            transition=lambda: "PrepFire" if self.debugTimer.advanceIfElapsed(0.5) else ""
        )
        states.append(handoff)

        prepFire = State(
            name="PrepFire",
            run=lambda: self.shooterPivot.setAmp(),
            transition=lambda: "Fire" if self.shooterPivot.getController().getPositionError() < 0.1 else "" #constant from set amp
        )
        states.append(prepFire)

        fire = State(
            name="Fire",
            enter=lambda: self.shooter.runShooters(3),
            transition=lambda: "Standby" if self.debugTimer.advanceIfElapsed(1) else "",
            exit=lambda: self.shooter.runShooters(0)
        )
        states.append(fire)
        
        super().__init__(states, None, debugMode)