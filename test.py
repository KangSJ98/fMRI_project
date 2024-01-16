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
from datetime import datetime
from InitData.Block_Shape_345DB import b_database
from InitData.b_sequence import b1_sequence, b2_sequence
from InitData.Target_Shape_20 import target_database

# add path
task_dir = os.path.dirname(os.path.abspath(__file__))
block_data_path = os.path.join(task_dir, 'InitData', 'Block_Shape_data.pkl')
b1_sequence_data_path = os.path.join(task_dir, 'InitData', 'b1_sequence.pkl')
b2_sequence_data_path = os.path.join(task_dir, 'InitData', 'b2_sequence.pkl')
target_data_path = os.path.join(task_dir, 'InitData', 'Target_Shape_data.pkl')

current_datetime = datetime.now()
log_folder = current_datetime.strftime('%Y_%m_%d_%H_%M_%S')
os.makedirs(os.path.join('Log', log_folder), exist_ok=True)

# initiate
pygame.init()

# screen setting
WIDTH_SCREEN, HEIGHT_SCREEN = 1404, 920
BLOCK_SIZE = 40
WIDTH_GAME, HEIGHT_GAME = 35, 22
WIDTH_A, HEIGHT_A = 1, 5
WIDTH_B, HEIGHT_B = 5, 5
WIDTH_TARGET, HEIGHT_TARGET = 20, 14
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
    [0],
    [0]
]

# control_b
shape_control_b = [
    [1]
]

b1_num, b2_num = 0, 0

map_control_b1 = b_database[b1_sequence[b1_num]]
map_control_b2 = b_database[b2_sequence[b2_num]]

# target
for target, values in target_database.items():
    for _ in range(8):
        values.insert(0, [0] * 20)
target_num = 1
map_target = target_database[f'Target {target_num}']

# background layer
map_background = [[0] * WIDTH_GAME for _ in range(HEIGHT_GAME)]

### function def
def clear_previous_position(current_shape, shape_position, current_map, map_widgh, map_height):
    for y, row in enumerate(current_shape):
        for x, value in enumerate(row):
            if value:
                if 0<= shape_position[0] + x < map_widgh and 0<= shape_position[1] + y < map_height:
                    current_map[shape_position[1] + y][shape_position[0] + x] = 0
    
    return current_map

def move_shape(current_shape, shape_position, current_map, map_width, map_height, dx, dy):
    clear_previous_position(current_shape, shape_position, current_map, map_width, map_height)
    can_move = True
    for y, row in enumerate(current_shape):
        for x, value in enumerate(row):
            if value:
                new_x, new_y = shape_position[0] + dx + x, shape_position[1] + dy + y
                if(
                    (new_x < 0 or map_width <= new_x)
                    or (new_y < 0 or map_height <= new_y)
                    or current_map[new_y][new_x] == 1
                ):
                    can_move = False
                    break
    
    if can_move:
        shape_position[0] += dx
        shape_position[1] += dy
    
    return shape_position, can_move

def hard_drop(current_shape, shape_position, current_map, map_width, map_height):
    can_move = True
    while can_move:
        shape_position, can_move = move_shape(current_shape, shape_position, current_map, map_width, map_height, 0, 1)
    return shape_position

def rotate_clockwise(array):
    return [list(row) for row in zip(*reversed(array))]

def rotate_counterclockwise(array):
    return [list(row) for row in reversed(list(zip(*array)))]

# check control_b attach b1 or b2
def check_b_possible(current_map, shape_position):
    devide = (current_map[max(0, shape_position[1] - 1)][shape_position[0]] + 
                current_map[shape_position[1]][max(0, shape_position[0] - 1)] + 
                current_map[min(HEIGHT_B - 1, shape_position[1] + 1)][shape_position[0]] + 
                current_map[shape_position[1]][min(WIDTH_B - 1, shape_position[0] + 1)]
    )
    if devide:
        return False
    else:
        return True

# if the target row is full, remove
def remove_line(current_map, score):
    for y in range(HEIGHT_TARGET):
        if sum(current_map[y]) == WIDTH_TARGET:
            del current_map[y]
            current_map.insert(0, [0] * WIDTH_TARGET)
            score += LINE_SCORE
        
    return current_map, score

# if block over 9 line, game over
def check_trial_over(current_map):
    if sum(current_map[HEIGHT_TARGET-10]) > 0:
        return True
    else:
        return False

def save_log(map_control_b1, map_control_b2, next_map_control_b1, next_map_control_b2, shape_position, map_target, trial, phase, move):
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

def option_score_left(target):
    target_copy = [row[:] for row in target]
    orphan_result_databases = {}
    for shape_name, matrix in b_database.items():
        shape_position = [[0,2], [0,0], [0,0]] # a(0,0~4), a(0~4,0), b(0~width, 0)
        min_hole = float('inf')

        for i in range(5):
            rotated_matrix = rotate_counterclockwise(matrix)
            shape_position[1][0] = i
            if rotated_matrix[0][shape_position[1][0]] == 1 or check_b_possible(rotated_matrix, hard_drop(shape_control_b, shape_position[1], rotated_matrix, WIDTH_B, HEIGHT_B)):
                continue
            else:
                rotated_matrix[shape_position[1][1]][shape_position[1][0]] = 1
            
            combine_matrix = rotate_clockwise(rotated_matrix)
            left = hard_drop(rotate_counterclockwise(combine_matrix), shape_position[2], rotate_counterclockwise(target_copy), HEIGHT_TARGET, WIDTH_TARGET)
            right = hard_drop(rotate_clockwise(combine_matrix), shape_position[2], rotate_clockwise(target_copy), HEIGHT_TARGET, WIDTH_TARGET)
            
            for j in range(WIDTH_TARGET - left[1], right[1]):
                shape_position[2] = hard_drop(combine_matrix, [j,0], target_copy, WIDTH_TARGET, HEIGHT_TARGET)
                hole = count_orphan_hole(target_copy, combine_matrix, shape_position[2])
                if hole < min_hole:
                    min_hole = hole
        orphan_result_databases[shape_name] = min_hole
    return orphan_result_databases

def count_orphan_hole(target, combine_matrix, shape_position):
    target_copy = [row[:] for row in target]
    for y, row in enumerate(combine_matrix):
        for x, value in enumerate(row):
            if value:
                target_copy[shape_position[1] + y][shape_position[0] + x] = 2

    hole = 0
    for y, row in enumerate(target_copy):
        for x, value in enumerate(row):
            if value == 0:
                for i in range(y):
                    if target_copy[i][x] == 2:
                        hole += 1
                        break

    return hole

def count_flat(target, combine_matrix, shape_position)


    

clock = pygame.time.Clock()
game_over = False
score = 0
trial = 1

game_start_time = pygame.time.get_ticks()

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
        map_control_b1 = b_database[b1_sequence[b1_num]]
        next_map_control_b1 = b_database[b1_sequence[b1_num + 1]]
        map_control_b2 = b_database[b2_sequence[b2_num]]
        next_map_control_b2 = b_database[b2_sequence[b2_num + 1]]

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
                    if rotated_map[0][shape_position[1][0]] == 1 or check_b_possible(rotated_map, hard_drop(shape_control_b, shape_position[1], rotated_map, WIDTH_B, HEIGHT_B)):
                        rotated_map[shape_position[1][1]][shape_position[1][0]] = 3
                        stage_end = True
                        error_b = True
                    else:
                        rotated_map[shape_position[1][1]][shape_position[1][0]] = 1
                        phase = 3
                        b1_num += 1

                    map_control_b1 = rotate_clockwise(rotated_map)
                    # shape_combime = control a + control b
                    shape_combine = map_control_b1
                    
                elif move == 2: # choose right
                    shape_position[1][0] = 4 - shape_position[1][0]
                    rotated_map = rotate_clockwise(map_control_b2)

                    # check option b is possible
                    # if impossible : go to phase 1
                    if rotated_map[0][shape_position[1][0]] == 1 or check_b_possible(rotated_map, hard_drop(shape_control_b, shape_position[1], rotated_map, WIDTH_B, HEIGHT_B)):
                        rotated_map[shape_position[1][1]][shape_position[1][0]] = 3
                        stage_end = True
                        error_b = True
                    else:
                        rotated_map[shape_position[1][1]][shape_position[1][0]] = 1
                        phase = 3
                        b2_num += 1

                    map_control_b2 = rotate_counterclockwise(rotated_map)
                    # shape_combine = control a + control b
                    shape_combine = map_control_b2
                choice = move

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
                    orphan_data = option_score_left(map_target)
                    for shape_name, value in orphan_data.items():
                        print(f"{shape_name} 결과 : {value}")

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
