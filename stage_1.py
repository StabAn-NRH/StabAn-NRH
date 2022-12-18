from PIL import Image, ImageDraw, ImageFont
import time
import random
import math
import cv2 as cv
import numpy as np
from colorsys import hsv_to_rgb
from Enemy import Enemy
from Character import Character
from Joystick import Joystick
from Button import Button
from Key import Key
from EndZone import EndZone

'''
        7
        6
  1  2  3  4  5
        8
        9
'''
def rotate(rotatee, degree):  # 60분법 입력 -> 라디안
    # 1번째 원
    coordinate = [int(190 + (32 * math.cos(math.radians(float(degree - 180))))), int(180 - (32 * math.sin(math.radians(float(degree - 180)))))]
    rotatee[0].borderPosition = np.array([coordinate[0] - 8, coordinate[1] - 8, coordinate[0] + 8, coordinate[1] + 8])
    rotatee[0].position = np.array([coordinate[0] - 5, coordinate[1] - 5, coordinate[0] + 5, coordinate[1] + 5])
    
    # 2번째 원
    coordinate = [int(190 + (16 * math.cos(math.radians(float(degree - 180))))), int(180 - (16 * math.sin(math.radians(float(degree - 180)))))]
    rotatee[1].borderPosition = np.array([coordinate[0] - 8, coordinate[1] - 8, coordinate[0] + 8, coordinate[1] + 8])
    rotatee[1].position = np.array([coordinate[0] - 5, coordinate[1] - 5, coordinate[0] + 5, coordinate[1] + 5])
    
    # 4번째 원
    coordinate = [int(190 + (16 * math.cos(math.radians(float(degree))))), int(180 - (16 * math.sin(math.radians(float(degree)))))]
    rotatee[3].borderPosition = np.array([coordinate[0] - 8, coordinate[1] - 8, coordinate[0] + 8, coordinate[1] + 8])
    rotatee[3].position = np.array([coordinate[0] - 5, coordinate[1] - 5, coordinate[0] + 5, coordinate[1] + 5])
    
    # 5번째 원
    coordinate = [int(190 + (32 * math.cos(math.radians(float(degree))))), int(180 - (32 * math.sin(math.radians(float(degree)))))]
    rotatee[4].borderPosition = np.array([coordinate[0] - 8, coordinate[1] - 8, coordinate[0] + 8, coordinate[1] + 8])
    rotatee[4].position = np.array([coordinate[0] - 5, coordinate[1] - 5, coordinate[0] + 5, coordinate[1] + 5])
    
    # 6번째 원
    coordinate = [int(190 + (16 * math.cos(math.radians(float(degree - 270))))), int(180 - (16 * math.sin(math.radians(float(degree - 270)))))]
    rotatee[5].borderPosition = np.array([coordinate[0] - 8, coordinate[1] - 8, coordinate[0] + 8, coordinate[1] + 8])
    rotatee[5].position = np.array([coordinate[0] - 5, coordinate[1] - 5, coordinate[0] + 5, coordinate[1] + 5])

    # 7번째 원
    coordinate = [int(190 + (32 * math.cos(math.radians(float(degree - 270))))), int(180 - (32 * math.sin(math.radians(float(degree - 270)))))]
    rotatee[6].borderPosition = np.array([coordinate[0] - 8, coordinate[1] - 8, coordinate[0] + 8, coordinate[1] + 8])
    rotatee[6].position = np.array([coordinate[0] - 5, coordinate[1] - 5, coordinate[0] + 5, coordinate[1] + 5])
    
    # 8번째 원
    coordinate = [int(190 + (16 * math.cos(math.radians(float(degree - 90))))), int(180 - (16 * math.sin(math.radians(float(degree - 90)))))]
    rotatee[7].borderPosition = np.array([coordinate[0] - 8, coordinate[1] - 8, coordinate[0] + 8, coordinate[1] + 8])
    rotatee[7].position = np.array([coordinate[0] - 5, coordinate[1] - 5, coordinate[0] + 5, coordinate[1] + 5])
    
    # 9번째 원
    coordinate = [int(190 + (32 * math.cos(math.radians(float(degree - 90))))), int(180 - (32 * math.sin(math.radians(float(degree - 90)))))]
    rotatee[8].borderPosition = np.array([coordinate[0] - 8, coordinate[1] - 8, coordinate[0] + 8, coordinate[1] + 8])
    rotatee[8].position = np.array([coordinate[0] - 5, coordinate[1] - 5, coordinate[0] + 5, coordinate[1] + 5])
    
def makeWalls():
    walls = []
    for i in range(104, 136, 4):
        walls.append((0, i, 0 + 3, i + 3))
    
    for i in range(0, 32, 4):
        walls.append((i, 104, i + 3, 104 + 3))
    for i in range(0, 32, 4):
        walls.append((i, 135 - 3, i + 3, 135))

    for i in range(103, 71, -4):
        walls.append((31 - 3, i - 3, 31, i))
    for i in range(136, 168, 4):
        walls.append((31 - 3, i, 31, i + 3))

    for i in range(32, 56, 4):
        walls.append((i, 72, i + 3, 72 + 3))
    for i in range(56, 72, 4):
        walls.append((i, 72, i + 3, 72 + 3))
    for i in range(72, 100, 4):
        walls.append((i, 72, i + 3, 72 + 3))
    for i in range(32, 56, 4):
        walls.append((i, 167 - 3, i + 3, 167))
    for i in range(56, 72, 4):
        walls.append((i, 167 - 3, i + 3, 167))
    for i in range(72, 100, 4):
        walls.append((i, 167 - 3, i + 3, 167))

    for i in range(103, 71, -4):
        walls.append((99 - 3, i - 3, 99, i))
    for i in range(136, 168, 4):
        walls.append((99 - 3, i, 99, i + 3))

    for i in range(96, 148, 4):
        walls.append((i, 104, i + 3, 104 + 3))
    for i in range(96, 148, 4):
        walls.append((i, 135 - 3, i + 3, 135))

    for i in range(132, 204, 4):
        walls.append((147 - 3, i, 147, i + 3))
    
    for i in range(140, -4, -4):
        walls.append((i, 203 - 3, i + 3, 203))

    for i in range(204, 228, 4):
        walls.append((0, i, 0 + 3, i + 3))
    
    for i in range(0, 236, 4):
        walls.append((i, 227 - 3, i + 3, 227))

    for i in range(224, 0, -4):
        walls.append((235 - 3, i, 235, i + 3))

    for i in range(228, 144, -4):
        walls.append((i, 4, i + 3, 4 + 3))

    for i in range(4, 108, 4):
        walls.append((147 - 3, i, 147, i + 3))
    return walls

def drawWalls(walls, canvas):
    for point in walls:
        canvas.rectangle(point, fill = (0, 0, 0))

def main():
    print("start...")
    joystick = Joystick()
    my_image = Image.new("RGB", (joystick.width, joystick.height))
    my_draw = ImageDraw.Draw(my_image)
    my_draw.rectangle((0, 0, joystick.width, joystick.height), fill=(255, 0, 0, 100))
    joystick.disp.image(my_image)
    # 잔상이 남지 않는 코드 & 대각선 이동 가능
    my_circle = Character(joystick.width, joystick.height)
    my_circle.borderPosition[0] = 8
    my_circle.borderPosition[2] = my_circle.borderPosition[0] + 16
    my_circle.position[0] = my_circle.borderPosition[0] + 3
    my_circle.position[2] = my_circle.borderPosition[2] - 3
    my_draw.rectangle((0, 0, joystick.width, joystick.height), fill = (255, 255, 255, 100))
    enemy_1 = Enemy((43, 87), "down")
    enemy_2 = Enemy((63, 151), "up")
    enemy_3 = Enemy((83, 87), "down")

    enemy_rot_1 = Enemy((158, 180), "rotate")
    enemy_rot_2 = Enemy((174, 180), "rotate")
    enemy_rot_3 = Enemy((190, 180), "rotate")
    enemy_rot_4 = Enemy((206, 180), "rotate")
    enemy_rot_5 = Enemy((222, 180), "rotate")

    enemy_rot_6 = Enemy((190, 164), "rotate")
    enemy_rot_7 = Enemy((190, 148), "rotate")
    enemy_rot_8 = Enemy((190, 196), "rotate")
    enemy_rot_9 = Enemy((190, 212), "rotate")

    enemy_line_1 = Enemy((158, 40), "left")
    enemy_line_2 = Enemy((158, 56), "left")
    enemy_line_3 = Enemy((158, 72), "left")
    enemy_line_4 = Enemy((158, 88), "left")
    button = Button((228, 119))
    key = Key((16, 214))
    endzone = EndZone((190, 16))
    stage_1_walls = makeWalls()

    enemys_list = [enemy_1, enemy_2, enemy_3]
    enemys_rotate_list = [enemy_rot_1, enemy_rot_2, enemy_rot_3, enemy_rot_4, enemy_rot_5, enemy_rot_6, enemy_rot_7, enemy_rot_8, enemy_rot_9]
    enemys_line_list = [enemy_line_1, enemy_line_2, enemy_line_3, enemy_line_4]

    blink_count = 0
    rotate_degree = 0
    rotate_speed = -30

    while True:
        my_circle.center = np.array([(my_circle.position[0] + my_circle.position[2]) / 2, (my_circle.position[1] + my_circle.position[3]) / 2])
        for enemy in enemys_list:
            enemy.center = np.array([(enemy.position[0] + enemy.position[2]) / 2, (enemy.position[1] + enemy.position[3]) / 2])
        for enemy in enemys_rotate_list:
            enemy.center = np.array([(enemy.position[0] + enemy.position[2]) / 2, (enemy.position[1] + enemy.position[3]) / 2])
        for enemy in enemys_line_list:
            enemy.center = np.array([(enemy.position[0] + enemy.position[2]) / 2, (enemy.position[1] + enemy.position[3]) / 2])
        command = {'move': False, 'up_pressed': False , 'down_pressed': False, 'left_pressed': False, 'right_pressed': False}

        if key.aquired and my_circle.center[1] <= endzone.position[3]:
            break
        
        if not joystick.button_U.value:  # up pressed
            command['up_pressed'] = True
            command['move'] = True

        if not joystick.button_D.value:  # down pressed
            command['down_pressed'] = True
            command['move'] = True

        if not joystick.button_L.value:  # left pressed
            command['left_pressed'] = True
            command['move'] = True

        if not joystick.button_R.value:  # right pressed
            command['right_pressed'] = True
            command['move'] = True

        if not joystick.button_A.value and my_circle.jumping == "ground":
            my_circle.jumping = "rising"

        if not joystick.button_B.value:
            button.isEnabled(my_circle.center)

        if my_circle.height >= 5:
            my_circle.jumping = "falling"

        
        for enemy in enemys_list:
            if not my_circle.alive:
                break
            elif my_circle.collision(enemy) and my_circle.height <= 1:
                my_circle.alive = not my_circle.alive
        for enemy in enemys_rotate_list:
            if not my_circle.alive:
                break
            elif my_circle.collision(enemy) and my_circle.height <= 1:
                my_circle.alive = not my_circle.alive
        for enemy in enemys_line_list:
            if not my_circle.alive:
                break
            elif my_circle.collision(enemy) and my_circle.height <= 1:
                my_circle.alive = not my_circle.alive
            
        if my_circle.alive:
            my_circle.move(stage_1_walls, command)
            my_circle.jump()
        
        #그리는 순서가 중요합니다. 배경을 먼저 깔고 위에 그림을 그리고 싶었는데 그림을 그려놓고 배경으로 덮는 결과로 될 수 있습니다.
        my_draw.rectangle((0, 0, joystick.width, joystick.height), fill = (180, 181, 254))
        my_draw.rectangle((4, 108, 28, 134), fill = (181, 254, 180))
        my_draw.rectangle((tuple(endzone.position)), fill = (181, 254, 180))
        drawWalls(stage_1_walls, my_draw)

        key.isNearby(my_circle.center)
        if not key.aquired:
            my_draw.ellipse(tuple(key.borderPosition), fill = (0, 0, 0))
            my_draw.ellipse(tuple(key.position), fill = (255, 255, 0))

        for enemy in enemys_list:
            if enemy.travel == "down":
                if enemy.borderPosition[3] >= 159:
                    enemy.travel = "up"
                else:
                    enemy.position[1] += 4
                    enemy.position[3] += 4
                    enemy.borderPosition[1] += 4
                    enemy.borderPosition[3] += 4
            elif enemy.travel == "up":
                if enemy.borderPosition[1] <= 79:
                    enemy.travel = "down"
                else:
                    enemy.position[1] -= 4
                    enemy.position[3] -= 4
                    enemy.borderPosition[1] -= 4
                    enemy.borderPosition[3] -= 4
            my_draw.ellipse(tuple(enemy.borderPosition), outline = enemy.borderOutline, fill = (0, 0, 0))
            my_draw.ellipse(tuple(enemy.position), outline = enemy.outline, fill = (0, 0, 255))


        for enemy in enemys_line_list:
            if enemy.travel == "left":
                if enemy.borderPosition[2] >= 228:
                    enemy.travel = "right"
                else:
                    enemy.position[0] += 8
                    enemy.position[2] += 8
                    enemy.borderPosition[0] += 8
                    enemy.borderPosition[2] += 8
            elif enemy.travel == "right":
                if enemy.borderPosition[0] <= 150:
                    enemy.travel = "left"
                else:
                    enemy.position[0] -= 8
                    enemy.position[2] -= 8
                    enemy.borderPosition[0] -= 8
                    enemy.borderPosition[2] -= 8
            my_draw.ellipse(tuple(enemy.borderPosition), outline = enemy.borderOutline, fill = (0, 0, 0))
            my_draw.ellipse(tuple(enemy.position), outline = enemy.outline, fill = (0, 0, 255))
        
        if button.activated:
            rotate_speed = -5
        else:
            rotate_speed = -30
        rotate(enemys_rotate_list, rotate_degree)

        for enemy in enemys_rotate_list:
            my_draw.ellipse(tuple(enemy.borderPosition), fill = (0, 0, 0))
            my_draw.ellipse(tuple(enemy.position), fill = (0, 0, 255))
        
        if abs(rotate_degree) % 360 == 0 and rotate_degree != 0:
            rotate_degree = 0
        else:
            rotate_degree += rotate_speed

        if not my_circle.alive:
            if blink_count == 8:
                blink_count = 0
                my_circle.respawn(joystick.width, joystick.height)
                button.activated = False
                key.aquired = False
            elif blink_count % 2 == 0:
                my_draw.rectangle(tuple(my_circle.borderPosition), fill = (255, 255, 255))
                my_draw.rectangle(tuple(my_circle.position), fill = (255, 255, 255))
                blink_count += 1
            else:
                my_draw.rectangle(tuple(my_circle.borderPosition), fill = (0, 0, 0))
                my_draw.rectangle(tuple(my_circle.position), fill = (255, 0, 0))
                blink_count += 1
        else:
            my_draw.rectangle(tuple(my_circle.borderPosition), fill = (0, 0, 0))
            my_draw.rectangle(tuple(my_circle.position), fill = (255, 0, 0))

        if not button.activated:
            my_draw.rectangle(tuple(button.borderPosition), fill = (0, 0, 0))
            my_draw.rectangle(tuple(button.position), fill = (255, 128, 0))
        else:
            my_draw.rectangle(tuple(button.borderPosition), fill = (0, 0, 0))
            my_draw.rectangle(tuple(button.position), fill = (0, 255, 255))

        #좌표는 동그라미의 왼쪽 위, 오른쪽 아래 점 (x1, y1, x2, y2)
        joystick.disp.image(my_image)
    print("You Escaped!")    

if __name__ == '__main__':
    main()