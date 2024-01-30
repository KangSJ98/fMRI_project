'''
control_a = 4x1
(5,0) ~ (5,3)
control_b1 = 4x4 (left)
(0,0) ~ (3,3)
control_b2 = 4x4 (right)
(7,0) ~ (10,3)
target = 10x7 (6x7(target) + 4x7(combine))
(2,2) ~ (8,11)

1. present purpose(hole : orphan hole, flat : flatness) seperate by color
2. choose the control a position
3. choose control b1 or b2
    3-1. if the block is not complete, go to 1
4. choose the best position (best score of present purpose), 1s delay
'''

import pygame
import os
from datetime import datetime
from InitData.b_234DB import *
from InitData.Target_Shape_20 import target_database
from Utils.utils import *
from Utils.option_score import *

# make log file
current_datetime = datetime.now()
log_folder = current_datetime.strftime('%Y_%m_%d_%H_%M_%S')
os.makedirs(os.path.join('Log', log_folder), exist_ok=True)

# initiate
pygame.init()
clock = pygame.time.Clock()
game_over = False
trial = 1
target_num = 1

game_start_time = pygame.time.get_ticks()

# screen setting
WIN = pygame.display.set_mode((WIDTH_SCREEN, HEIGHT_SCREEN))
pygame.display.set_caption("Task Version 2")

# color define
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# control_a
shape_control_a = [
    [1]
]
map_control_a = [
    [0],
    [0],
    [0],
    [0]
]

# control_b
shape_control_b = [
    [1]
]

# target
for target, values in target_database.items():
    for _ in range(4):
        values.insert(0, [0] * WIDTH_TARGET)

# game loof
while not game_over:
    trial_over = False
    error_b = False
    phase = 1
    purpose = random.choice(['hole','flat'])
    print(purpose)
    shape_position = [[0,2],[0,0],[0,0]] # 0 : control_a, 1 : control_b, 2 : combine

    # target reset
    map_target = target_database[f'Target {target_num}']

    # option scroe
    left_score, right_score = option_score(map_target)
    b1_name = random.choice(list(left_database.keys()))
    b2_name = find_closest_shape(right_score, purpose, left_score[b1_name][purpose][0])
    map_control_b1 = left_database[b1_name]
    map_control_b2 = right_database[b2_name]

    # background layer
    map_background = [[0] * WIDTH_GAME for _ in range(HEIGHT_GAME)]

    while not trial_over:
        # keybord input
        move = 0
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game_over, trial_over = True, True
                elif event.key == pygame.K_LEFT:
                    move = 'left'
                elif event.key == pygame.K_RIGHT:
                    move = 'right'
                elif event.key == pygame.K_DOWN:
                    move = 'down'
                elif event.key == pygame.K_UP:
                    move = 'up'
                elif event.key == pygame.K_SPACE:
                    move = 'space'
        
        # phase 1
        if phase == 1:
            if move == 'down':
                shape_position[0], _ = move_shape(shape_control_a, shape_position[0], map_control_a, WIDTH_A, HEIGHT_A, 0, 1)
            elif move == 'up':
                shape_position[0], _ = move_shape(shape_control_a, shape_position[0], map_control_a, WIDTH_A, HEIGHT_A, 0, -1)
            elif move == 'space':
                shape_position[1][0] = shape_position[0][1]
                phase = 2
        # phase 2
        if phase == 2:
            phase2_choice = move
            if move == 'left':
                rotated_map = rotate_counterclockwise(map_control_b1)
                shape_position[1] = hard_drop(shape_control_b, shape_position[1], rotated_map, WIDTH_B, HEIGHT_B)

                # check option b is possible
                if rotated_map[0][shape_position[1][0]] == 1 or check_b_possible(rotated_map, shape_position[1]):
                    rotated_map[shape_position[1][1]][shape_position[1][0]] = 3
                    trial_over, error_b = True, True
                else:
                    rotated_map[shape_position[1][1]][shape_position[1][0]] = 1
                    phase = 3

                map_control_b1 = rotate_clockwise(rotated_map)
                shape_combine = map_control_b1 # shape_combine = control_a + control_b
            elif move == 'right':
                print(map_control_b2)
                shape_position[1][0] = HEIGHT_B - shape_position[1][0] - 1
                rotated_map = rotate_clockwise(map_control_b2)
                shape_position[1] = hard_drop(shape_control_b, shape_position[1], rotated_map, WIDTH_B, HEIGHT_B)

                # check option b is possible
                if rotated_map[0][shape_position[1][0]] == 1 or check_b_possible(rotated_map, shape_position[1]):
                    rotated_map[shape_position[1][1]][shape_position[1][0]] = 3
                    trial_over, error_b = True, True
                else:
                    rotated_map[shape_position[1][1]][shape_position[1][0]] = 1
                    phase = 3

                map_control_b2 = rotate_counterclockwise(rotated_map)
                shape_combine = map_control_b2 # shape_combine = control_a + control_b
        # phase 3
        if phase == 3:
            # best position of current purpose
            if phase2_choice == 'left':
                shape_position[2] = left_score[b1_name][purpose][1]
            else:
                shape_position[2] = right_score[b2_name][purpose][1]
            print(f'shape position = {shape_position[2]}, shape_combine : {shape_combine}')

            # add shape_combine to target
            for y, row in enumerate(shape_combine):
                for x, value in enumerate(row):
                    if value:
                        map_target[y + shape_position[2][1]][x + shape_position[2][0]] = shape_combine[y][x]
            trial_over = True
        ### render
        ## fill all layer into background map (0 : WHITE, 1 : BLACK, 2 : GRAY, 3 : RED)
        # control_a
        for y in range(HEIGHT_A):
            map_background[y][5] = 2
        map_background[shape_position[0][1]][5] = 1

        # control_b
        for y in range(HEIGHT_B):
            for x in range(WIDTH_B):
                map_background[y][x] = 2 - map_control_b1[y][x]
                map_background[y][x + 7] = 2 - map_control_b2[y][x]
        
        # target
        for y in range(4,HEIGHT_TARGET):
            for x in range(WIDTH_TARGET):
                map_background[y + 2][x + 2] = map_target[y][x]
        
        ## render
        # white background
        WIN.fill(WHITE)

        # background map (0 : WHITE, 1 : BLACK, 2 : GRAY, -1 : RED)
        for y, row in enumerate(map_background):
            for x, value in enumerate(row):
                if value == 1:
                    pygame.draw.rect(WIN, BLACK, ((x + 0.1) * BLOCK_SIZE, (y + 0.1) * BLOCK_SIZE, BLOCK_SIZE * 0.8, BLOCK_SIZE * 0.8))
                elif value == 2:
                    pygame.draw.rect(WIN, GRAY, ((x + 0.1) * BLOCK_SIZE, (y + 0.1) * BLOCK_SIZE, BLOCK_SIZE * 0.8, BLOCK_SIZE * 0.8))
                elif value == -1:
                    pygame.draw.rect(WIN, RED, ((x + 0.1) * BLOCK_SIZE, (y + 0.1) * BLOCK_SIZE, BLOCK_SIZE * 0.8, BLOCK_SIZE * 0.8))
        
        # show b error message
        if error_b:
            font = pygame.font.Font(None, 72)
            text = font.render('Try again', True, RED)
            text_rect = text.get_rect()
            text_rect.centerx = WIN.get_width() // 2
            text_rect.top = BLOCK_SIZE * HEIGHT_A

            WIN.blit(text, text_rect)

        # screen update
        pygame.display.update()
        
        # FPS
        clock.tick(60)

        # if trial end, delay 1s
        if error_b or phase == 3:
            pygame.time.delay(10000)

    trial += 1
    target_num += 1