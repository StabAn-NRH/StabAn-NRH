import numpy as np
import time
import Enemy
class Character:
    def __init__(self, width, height):
        self.appearance = 'rectangle'
        self.state = None
        self.alive = True
        self.position = np.array([width/2 - 5, height/2 - 5, width/2 + 5, height/2 + 5])
        self.borderPosition = np.array([width/2 - 8, height/2 - 8, width/2 + 8, height/2 + 8])
        # 총알 발사를 위한 캐릭터 중앙 점 추가
        self.center = np.array([(self.position[0] + self.position[2]) / 2, (self.position[1] + self.position[3]) / 2])
        self.outline = "#000000"
        self.jumping = 'ground'
        self.height = 0

    def move(self, walls, command = None):
        if command['move'] == False:
            self.state = None
        else:
            self.state = 'move'

            if command['up_pressed']:
                final_distance = -5
                for wall in walls:
                    if wall[0] <= self.center[0] <= wall[2] and wall[3] >= self.borderPosition[1] - 5 and wall[1] <= self.borderPosition[3] - 5:
                        distance = wall[3] - (self.borderPosition[1]) + 1
                        if distance >= 0:
                            final_distance = 0
                        elif -5 <= distance < 0:
                            final_distance = distance
                        else:
                            final_distance = -5
                
                self.position[1] += final_distance
                self.borderPosition[1] += final_distance
                self.position[3] += final_distance
                self.borderPosition[3] += final_distance
                
            if command['down_pressed']:
                final_distance = 5
                for wall in walls:
                    if wall[0] <= self.center[0] <= wall[2] and wall[1] <= self.borderPosition[3] + 5 and wall[3] >= self.borderPosition[1] + 5:
                        distance = wall[1] - (self.borderPosition[3]) - 1
                        if distance <= 0:
                            final_distance = 0
                        elif 0 < distance <= 5:
                            final_distance = distance
                        else:
                            final_distance = 5
    
                self.position[1] += final_distance
                self.borderPosition[1] += final_distance
                self.position[3] += final_distance
                self.borderPosition[3] += final_distance

            if command['left_pressed']:
                final_distance = -5
                for wall in walls:
                    if wall[1] <= self.center[1] <= wall[3] and wall[2] >= self.borderPosition[0] - 5 and wall[0] <= self.borderPosition[2] - 5:
                        distance = wall[2] - (self.borderPosition[0]) + 1
                        if distance >= 0:
                            final_distance = 0
                        elif -5 <= distance < 0:
                            final_distance = distance
                        else:
                            final_distance = -5
                self.position[0] += final_distance
                self.borderPosition[0] += final_distance
                self.position[2] += final_distance
                self.borderPosition[2] += final_distance
                
            if command['right_pressed']:
                final_distance = 5
                for wall in walls:
                    if wall[1] <= self.center[1] <= wall[3] and wall[0] <= self.borderPosition[2] + 5 and wall[2] >= self.borderPosition[0] + 5:
                        distance = wall[0] - (self.borderPosition[2]) - 1
                        if distance <= 0:
                            final_distance = 0
                        elif 0 < distance <= 5:
                            final_distance = distance
                        else:
                            final_distance = 5
                self.position[0] += final_distance
                self.borderPosition[0] += final_distance
                self.position[2] += final_distance
                self.borderPosition[2] += final_distance
                
        self.center = np.array([(self.position[0] + self.position[2]) / 2, (self.position[1] + self.position[3]) / 2]) 
    def jump(self):
        if self.jumping == 'rising':
            self.borderPosition[0] -= 1
            self.borderPosition[2] += 1
            self.position[0] -= 1
            self.position[2] += 1

            self.borderPosition[1] -= 1
            self.borderPosition[3] += 1
            self.position[1] -= 1
            self.position[3] += 1

            self.height += 1
        
        elif self.jumping == 'falling' and self.height > 0:
            self.borderPosition[0] += 1
            self.borderPosition[2] -= 1
            self.position[0] += 1
            self.position[2] -= 1

            self.borderPosition[1] += 1
            self.borderPosition[3] -= 1
            self.position[1] += 1
            self.position[3] -= 1

            self.height -= 1

        else:
            self.jumping = 'ground'
    
    
        #center update
        self.center = np.array([(self.position[0] + self.position[2]) / 2, (self.position[1] + self.position[3]) / 2]) 

    def collision(self, enemy):
        if ((self.center[0] - enemy.center[0]) ** 2) + ((self.center[1] - enemy.center[1]) ** 2) < (17 ** 2):
            return True
        else:
            return False

    def respawn(self, width, height):
        self.alive = not self.alive
        self.jumping = 'ground'
        self.height = 0
        self.position = np.array([width/2 - 5, height/2 - 5, width/2 + 5, height/2 + 5])
        self.borderPosition = np.array([width/2 - 8, height/2 - 8, width/2 + 8, height/2 + 8])
        self.borderPosition[0] = 8
        self.borderPosition[2] = self.borderPosition[0] + 16
        self.position[0] = self.borderPosition[0] + 3
        self.position[2] = self.borderPosition[2] - 3
    