from stateMachines.stateMachine import *
import random
import time

CHANCE_TO_SIGHT = 1
CHANCE_TO_STAY = 1
CHANCE_FOR_HORRIBLE_ERROR = 0

class IntakeStateMachine(StateMachine):
    def __init__(self, states=[], initialState=None, debugMode=False):
        self.noteSighted = False
        self.atDest = False

        states=[]

        #searching for note
        searching = State(
            name="SearchForNote",
            run=lambda: self.searchFunc(),
            transition=lambda: "MoveToNote" if self.noteSighted else ""
        )
        states.append(searching)

        #move to note (macro)
        move = State(
            name="MoveToNote",
            run=lambda: self.moveFunc(input("Did we move there? (Y for yes, N for no, M for assume manual control, anything else for moving): ")),
            transition=lambda: self.evalMove()
        )
        states.append(move)

        #lineup with note (micro)
        lineup = State(
            name="Lineup",
            run=lambda: self.moveFunc(input("Did we lineup right? (Y for yes, N for no, M for manual control, anything else for moving): ")),
            transition=lambda: self.evalLineup() 
        )
        states.append(lineup)

        manualDrive = State(
            name="ManualDrive",
            run=lambda: print("I'm driving ma!"),
            transition=lambda: "ROOT_STATE" if input("Still manual?: ") == "N" else ""
        )
        states.append(manualDrive)

        #reset the bot
        reset = State(
            name="Reset",
            enter=lambda: time.sleep(2),
            transition=lambda: "ROOT_STATE"
        )
        states.append(reset)

        #spin the motors!
        spin = State(
            name="SpinMotors",
            enter=lambda: self.spinThosePuppies(),
            transition=lambda: "Clamp" if self.checkForDisc() else ""
        )
        states.append(spin)

        #clamp the disc in the motors!
        clamp = State(
            name="Clamp",
            transition=lambda: "Gloop" if not input("Note lost? Enter Y for yes, anything else for no.: ") == "Y" else "ReverseClamp"
        )
        states.append(clamp)

        reverseClamp = State(
            name="ReverseClamp",
            run=lambda: print("\nFATAL ERROR\n"),
            transition=lambda: "Reset"
        )
        states.append(reverseClamp)

        #take augustus gloop up the tube
        gloop = State(
            name="Gloop",
            transition=lambda: "PrepFire" if self.checkForDisc() else "Reset"
        )
        states.append(gloop)

        #prep fire
        prepFire = State(
            name="PrepFire",
            enter=lambda: time.sleep(3),
            transition=lambda: "Fire"
        )
        states.append(prepFire)

        fire = State(
            name="Fire",
            enter=lambda: self.shoutFire(),
            transition=lambda: "Reset"
        )
        states.append(fire)

        super().__init__(states, initialState, debugMode)

    #searching functions
    def searchFunc(self): 
        print("Searching...")
        self.noteSighted = random.random() < CHANCE_TO_SIGHT
        self.destPos = (random.random()*200, random.random()*200)

    #moving functions
    def moveFunc(self, input):
        input = str(input)
        if input == 'Y':
            self.atDest = True
        elif input == 'N':
            self.atDest = False
            self.noteSighted = False
        elif input == 'M':
            self.overrideState("ManualDrive")
    
    def evalMove(self):
        if self.noteSighted:
            #ask for lineup if at dest and note in sight
            if self.atDest:
                self.atDest = False
                return "Lineup"
            #keep moving if we still see it
            else:
                return ""
        #lost sight of note
        else:
            return "SearchForNote"
    
    #lineup notes
    def evalLineup(self):
        if self.noteSighted:
            #we're ready for a note!
            if self.atDest:
                return "SpinMotors"
            #still lining up
            else:
                return ""
        #lost sight of note
        else:
            return "SearchForNote"
        
    #spinning motors
    def spinThosePuppies(self):
        print("Those puppers are revving!")
        time.sleep(1)
        print("Those puppers are spinning!")
    
    def checkForDisc(self):
        res = random.random() < CHANCE_TO_STAY
        if res == False:
            print("\nIt slipped out\n")
        
        return res
    
    def shoutFire(self):
        print("\n\nFIRE IN THE HOLE\n\n")
    

refTime = time.time()

# if __name__ == "__main__":
#     machine = IntakeStateMachine()
#     while True:
#         dt = time.time() - refTime
#         if dt > 0.1:
#             machine.run()
#             refTime = time.time()
