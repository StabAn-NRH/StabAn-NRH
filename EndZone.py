import numpy as np

class EndZone:
    def __init__(self, spawn_position):
        self.appearance = 'Rectangle'
        self.position = np.array([spawn_position[0] - 44, spawn_position[1] - 10, spawn_position[0] + 44, spawn_position[1] + 10])
        self.outline = "#FF8000"
        self.borderOutline = "#000000"
        self.activated = False

    def isEnabled(self, x):
        if ((self.center[0] - x[0]) ** 2) + ((self.center[1] - x[1]) ** 2) < 20 ** 2 and not self.activated:
            print("button activated!!")
            self.activated = not self.activated