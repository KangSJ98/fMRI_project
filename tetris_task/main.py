'''
control_a = 5x1
control_b1 = 5x5 (왼)
control_b2 = 5x5 (오)
next_control_b1 = 3x3
next_control_b2 = 3x3
target = 14x20, 시작은 하단 6x20 에서만, 9줄을 넘어가면 game over

배경은 흰색, control 배경은 회색, 블록은 검은색, 블록 사이즈를 그리드보다 살짝 작게해서 흰색 배경으로 구분되게
control_a의 위치는 (17,3)) 부터 (17,7)
control_b1의 위치는 (8,3) 부터 (12,7))
control_b2의 위치는 (22,3) 부터 (26,7)
next_control_b1의 위치는 (4,4) 부터 (7,7)
next_control_b2의 위치는 (28,4)부터 (33,7)
target의 위치는 (8,8) 부터 (27,22)까지

1. control_a에서 1x1 control block 위치 선택
2. 1x1 control block 좌, 우 선택
    2-1. if control_b 에다가 최대로 움직였을 때 주변에 control_b 블록이 없거나 범위를 벗어나면 go 1
3. control_a + control_b 의 x최표 선택
4. 아래로 최대한 이동
    4-1. 한 줄이 차면 지우고 남은 위쪽 블록들 아래로 지운 줄 수만큼 내려오기
'''

import pygame
import sys
import pickle
import os
import numpy as np
import random
from datetime import datetime
from InitData.b_234DB import *
from InitData.Target_Shape_20 import target_database
from Utils.utils import *
from Utils.option_score import *

current_datetime = datetime.now()
log_folder = current_datetime.strftime('%Y_%m_%d_%H_%M_%S')
os.makedirs(os.path.join('Log', log_folder), exist_ok=True)

# initiate
pygame.init()

# screen setting
WIN = pygame.display.set_mode((WIDTH_SCREEN, HEIGHT_SCREEN))
pygame.display.set_caption("Tetris-like 게임")

# color define
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# parameter
LINE_SCORE = 1

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

b1_name = random.choice(list(left_database.keys()))
b2_name = random.choice(list(right_database.keys()))
map_control_b1 = left_database[b1_name]
map_control_b2 = right_database[b2_name]
next_map_control_b1 = left_database[random.choice(list(left_database.keys()))]
next_map_control_b2 = right_database[random.choice(list(right_database.keys()))]

# target
for target, values in target_database.items():
    for _ in range(8):
        values.insert(0, [0] * 20)
target_num = 1
map_target = target_database[f'Target {target_num}']

# background layer
map_background = [[0] * WIDTH_GAME for _ in range(HEIGHT_GAME)]

clock = pygame.time.Clock()
game_over = False
score = 0
trial = 1

game_start_time = pygame.time.get_ticks()

def save_log(map_control_b1, map_control_b2, next_map_control_b1, next_map_control_b2, shape_position, map_target, trial, phase, move):
    """
    save all log of game
    /Log/trial_{trial}.txt
    """
    current_time = pygame.time.get_ticks() - game_start_time
    file_name = f'trial_{trial}.txt'
    file_path = os.path.join('Log', log_folder, file_name)
    with open(file_path, 'a') as file:
        file.write(f"Time : {current_time}\n")
        file.write(f"Control b1 : {map_control_b1}\n")
        file.write(f"Control b2 : {map_control_b2}\n")
        file.write(f"Control b1 next : {next_map_control_b1}\n")
        file.write(f"Control b2 next : {next_map_control_b2}\n")
        file.write(f"Shape position : {shape_position}\n")
        file.write(f"Target : {map_target}\n")
        file.write(f"Phase : {phase}\n")
        file.write(f"Move : {move}\n")

# Game Loof
while not game_over:
    trial_over = False
    map_target = target_database[f'Target {target_num}']
    map_background = [[0] * WIDTH_GAME for _ in range(HEIGHT_GAME)]

    while not trial_over:
        # trial initiate
        stage_end = False
        error_b = False
        phase = 1
        shape_position = [[0,2], [2,0], [7,0]]
        
        while not stage_end:
            # keybord input
            move = 0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    trial_over = True
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        game_over, trial_over, stage_end = True, True, True
                    elif event.key == pygame.K_r:
                        stage_end = True
                    elif event.key == pygame.K_LEFT:
                        move = 1
                    elif event.key == pygame.K_RIGHT:
                        move = 2
                    elif event.key == pygame.K_DOWN:
                        move = 3
                    elif event.key == pygame.K_UP:
                        move = 4
                    elif event.key == pygame.K_SPACE:
                        move = 5
                    save_log(map_control_b1, map_control_b2, next_map_control_b1, next_map_control_b2, shape_position, map_target, trial, phase, move)

            # phase 1
            if phase == 1:
                if move == 3:   # move down
                    shape_position[0], _ = move_shape(shape_control_a, shape_position[0], map_control_a, WIDTH_A, HEIGHT_A, 0, 1)
                elif move == 4: # move up
                    shape_position[0], _ = move_shape(shape_control_a, shape_position[0], map_control_a, WIDTH_A, HEIGHT_A, 0, -1)
                elif move == 5: # choose
                    shape_position[1][0] = shape_position[0][1]
                    phase = 2
            
            # phase 2
            if phase == 2:
                if move == 1:   # choose left
                    rotated_map = rotate_counterclockwise(map_control_b1)

                    # check option b is possible
                    # if impossible : go to phase 1
                    shape_position[1] = hard_drop(shape_control_b, shape_position[1], rotated_map, WIDTH_B, HEIGHT_B)
                    if rotated_map[0][shape_position[1][0]] == 1 or check_b_possible(rotated_map, shape_position[1]):
                        rotated_map[shape_position[1][1]][shape_position[1][0]] = 3
                        stage_end = True
                        error_b = True
                    else:
                        rotated_map[shape_position[1][1]][shape_position[1][0]] = 1
                        phase = 3

                    map_control_b1 = rotate_clockwise(rotated_map)
                    # shape_combime = control a + control b
                    shape_combine = map_control_b1
                    
                elif move == 2: # choose right
                    shape_position[1][0] = HEIGHT_B - 1 - shape_position[1][0]
                    rotated_map = rotate_clockwise(map_control_b2)

                    # check option b is possible
                    # if impossible : go to phase 1
                    shape_position[1] = hard_drop(shape_control_b, shape_position[1], rotated_map, WIDTH_B, HEIGHT_B)
                    if rotated_map[0][shape_position[1][0]] == 1 or check_b_possible(rotated_map, shape_position[1]):
                        rotated_map[shape_position[1][1]][shape_position[1][0]] = 3
                        stage_end = True
                        error_b = True
                    else:
                        rotated_map[shape_position[1][1]][shape_position[1][0]] = 1
                        phase = 3

                    map_control_b2 = rotate_counterclockwise(rotated_map)
                    # shape_combine = control a + control b
                    shape_combine = map_control_b2
                    map_control_b2 = next_map_control_b2
                    next_map_control_b2 = right_database[random.choice(list(right_database.keys()))]
                phase2_choice = move - 1 # left : 0, right : 1

            # phase 3
            if phase == 3:
                if move == 1:   # move left
                    shape_position[2], _ = move_shape(shape_combine, shape_position[2], map_target, WIDTH_TARGET, HEIGHT_TARGET, -1, 0)
                elif move == 2: # move right
                    shape_position[2], _ = move_shape(shape_combine, shape_position[2], map_target, WIDTH_TARGET, HEIGHT_TARGET, 1, 0)
                elif move == 5: # choose
                    shape_position[2] = hard_drop(shape_combine, shape_position[2], map_target, WIDTH_TARGET, HEIGHT_TARGET)
                    stage_end = True

                # add shape_combine to target
                for y, row in enumerate(shape_combine):
                    for x, value in enumerate(row):
                        if value:
                            map_target[y + shape_position[2][1]][x + shape_position[2][0]] = shape_combine[y][x]
                
                # remove line, check game over
                map_target, score = remove_line(map_target,score)
                trial_over = check_trial_over(map_target)
                if move == 5:
                    score_time = pygame.time.get_ticks()
                    result_database = option_score(map_target, phase2_choice)
                    map_control_b1 = next_map_control_b1
                    next_map_control_b1 = left_database[random.choice(list(left_database.keys()))]

                    # for shape_name, value in orphan_data.items():
                    #     orphan_value = orphan_data.get(shape_name, 'N/A')
                    #     flat_value = flat_data.get(shape_name, 'N/A')
                    #     border_value = border_data.get(shape_name,'N/A')
                    #     print(f"{shape_name} 결과 : orphan : {orphan_value}, flat : {flat_value}, border : {border_value}")

                    print(pygame.time.get_ticks() - score_time)

            ### visualization
            ## fill all layer into background map (0 : WHITE, 1 : BLACK, 2 : GRAY, 3 : RED)
            # control a
            for y in range(HEIGHT_A):
                map_background[y + 3][17] = 2
            map_background[shape_position[0][1] + 3][17] = 1

            # control b
            for y in range(HEIGHT_B):
                for x in range(WIDTH_B):
                    map_background[y + 3][x + 8] = 2 - map_control_b1[y][x]

                    map_background[y + 3][x + 22] = 2 - map_control_b2[y][x]
            
            # target
            for y in range(HEIGHT_TARGET):
                for x in range(WIDTH_TARGET):
                    map_background[y + 8][x + 8] = map_target[y][x]

            ## render
            # initiate background white
            WIN.fill(WHITE)

            # 0 : WHITE, 1 : BLACK, 2 : GRAY, -1 : RED
            for y, row in enumerate(map_background):
                for x, value in enumerate(row):
                    if value == 1:
                        pygame.draw.rect(WIN, BLACK, ((x + 0.1) * BLOCK_SIZE, (y + 0.1) * BLOCK_SIZE, BLOCK_SIZE * 0.8, BLOCK_SIZE * 0.8))
                    elif value == 2:
                        pygame.draw.rect(WIN, GRAY, ((x + 0.1) * BLOCK_SIZE, (y + 0.1) * BLOCK_SIZE, BLOCK_SIZE * 0.8, BLOCK_SIZE * 0.8))
                    elif value == -1:
                        pygame.draw.rect(WIN, RED, ((x + 0.1) * BLOCK_SIZE, (y + 0.1) * BLOCK_SIZE, BLOCK_SIZE * 0.8, BLOCK_SIZE * 0.8))

            # draw next block
            for y, row in enumerate(next_map_control_b1):
                for x, value in enumerate(row):
                    if value:
                        pygame.draw.rect(WIN, BLACK, ((x + 0.1) * BLOCK_SIZE * 0.6 + 4 * BLOCK_SIZE, (y + 0.1) * BLOCK_SIZE * 0.6 + 4 * BLOCK_SIZE, BLOCK_SIZE * 0.48, BLOCK_SIZE * 0.48))
                    else:
                        pygame.draw.rect(WIN, GRAY, ((x + 0.1) * BLOCK_SIZE * 0.6 + 4 * BLOCK_SIZE, (y + 0.1) * BLOCK_SIZE * 0.6 + 4 * BLOCK_SIZE, BLOCK_SIZE * 0.48, BLOCK_SIZE * 0.48))
            for y, row in enumerate(next_map_control_b2):
                for x, value in enumerate(row):
                    if value:
                        pygame.draw.rect(WIN, BLACK, ((x + 0.1) * BLOCK_SIZE * 0.6 + 28 * BLOCK_SIZE, (y + 0.1) * BLOCK_SIZE * 0.6 + 4 * BLOCK_SIZE, BLOCK_SIZE * 0.48, BLOCK_SIZE * 0.48))
                    else:
                        pygame.draw.rect(WIN, GRAY, ((x + 0.1) * BLOCK_SIZE * 0.6 + 28 * BLOCK_SIZE, (y + 0.1) * BLOCK_SIZE * 0.6 + 4 * BLOCK_SIZE, BLOCK_SIZE * 0.48, BLOCK_SIZE * 0.48))
            
            # show score, trial, phase
            font = pygame.font.Font(None, 36)
            text = font.render(f'score : {score}    trial : {trial}     phase : {phase}', True, BLACK)
            text_rect = text.get_rect()
            text_rect.bottomleft = (10, WIN.get_height() - 10)
            WIN.blit(text, text_rect)

            if error_b:
                font = pygame.font.Font(None, 72)
                text = font.render('Try again', True, RED)
                text_rect = text.get_rect()
                text_rect.centerx = WIN.get_width() // 2
                text_rect.top = BLOCK_SIZE * 8

                WIN.blit(text, text_rect)

                pygame.display.update()
                pygame.time.delay(1000)

            # screen update
            pygame.display.update()

            # FPS
            clock.tick(60)
    
    trial += 1
    target_num += 1
