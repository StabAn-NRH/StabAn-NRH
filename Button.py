import numpy as np

class Button:
    def __init__(self, spawn_position):
        self.appearance = 'Rectangle'
        self.position = np.array([spawn_position[0] - 3, spawn_position[1] - 3, spawn_position[0] + 3, spawn_position[1] + 3])
        self.borderPosition = np.array([spawn_position[0] - 6, spawn_position[1] - 6, spawn_position[0] + 6, spawn_position[1] + 6])
        self.center = np.array([(self.position[0] + self.position[2]) / 2, (self.position[1] + self.position[3]) / 2])
        self.outline = "#FF8000"
        self.borderOutline = "#000000"
        self.activated = False

    def isEnabled(self, x):
        if ((self.center[0] - x[0]) ** 2) + ((self.center[1] - x[1]) ** 2) < 20 ** 2 and not self.activated:
            print("button activated!!")
            self.activated = not self.activated