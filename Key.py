import numpy as np

class Key:
    def __init__(self, spawn_position):
        self.appearance = 'circle'
        self.position = np.array([spawn_position[0] - 5, spawn_position[1] - 5, spawn_position[0] + 5, spawn_position[1] + 5])
        self.borderPosition = np.array([spawn_position[0] - 8, spawn_position[1] - 8, spawn_position[0] + 8, spawn_position[1] + 8])
        self.center = np.array([(self.position[0] + self.position[2]) / 2, (self.position[1] + self.position[3]) / 2])
        self.outline = "#FFFF00"
        self.borderOutline = "#000000"
        self.aquired = False

    def isNearby(self, x):
        if ((self.center[0] - x[0]) ** 2) + ((self.center[1] - x[1]) ** 2) < 8 ** 2 and not self.aquired:
            print("key aquired!")
            self.aquired = True