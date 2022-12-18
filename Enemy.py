import numpy as np

class Enemy:
    def __init__(self, spawn_position, direction):
        self.appearance = 'circle'
        self.position = np.array([spawn_position[0] - 5, spawn_position[1] - 5, spawn_position[0] + 5, spawn_position[1] + 5])
        self.borderPosition = np.array([spawn_position[0] - 8, spawn_position[1] - 8, spawn_position[0] + 8, spawn_position[1] + 8])
        self.center = np.array([(self.position[0] + self.position[2]) / 2, (self.position[1] + self.position[3]) / 2])
        self.outline = "#0000FF"
        self.borderOutline = "#000000"
        self.travel = direction

    def move(self):
        if self.travel == "down":
            if self.borderPosition[3] >= 159:
                self.travel = "up"
            else:
                self.position[1] += 4
                self.position[3] += 4
                self.borderPosition[1] += 4
                self.borderPosition[3] += 4
        else:
            if self.borderPosition[1] <= 79:
                self.travel = "down"
            else:
                self.position[1] -= 4
                self.position[3] -= 4
                self.borderPosition[1] -= 4
                self.borderPosition[3] -= 4