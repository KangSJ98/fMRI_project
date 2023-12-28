'''
control_a = 5x1
control_b1 = 5x5 (왼)
control_b2 = 5x5 (오)
target = 9x35, 시작은 하단 6x35 에서만

배경은 흰색, control 배경은 회색, 블록은 검은색, 블록 사이즈를 그리드보다 살짝 작게해서 흰색 배경으로 구분되게
control_b1의 위치는 (3,8) 부터 (7,12)
control_b2의 위치는 (3,22) 부터 (7,26)
control_a의 위치는 (3,17) 부터 (7,17)
target의 위치는 (11,0) 부터 (20, 34)까지

1. control_a에서 1x1 control block 위치 선택
2. 1x1 control block 좌, 우 선택
    2-1. if control_b 에다가 최대로 움직였을 때 주변에 control_b 블록이 없거나 범위를 벗어나면 go 1
3. control_a + control_b 의 x최표 선택
4. 아래로 최대한 이동
    4-1. 한 줄이 차면 지우고 남은 위쪽 블록들 아래로 지운 줄 수만큼 내려오기
'''

import pygame
import sys

# initiate
pygame.init()


# screen setting
WIDTH_SCREEN, HEIGHT_SCREEN = 1400, 800
BLOCK_SIZE = 40
WIDTH_GAME, HEIGHT_GAME = 35, 20
WIDTH_A, HEIGHT_A = 1, 5
WIDTH_B, HEIGHT_B = 5, 5
WIDTH_TARGET, HEIGHT_TARGET = 35, 9
WIN = pygame.display.set_mode((WIDTH_SCREEN, HEIGHT_SCREEN))
pygame.display.set_caption("Tetris-like 게임")

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
    [0],
    [0]
]

# control_b
shape_control_b = [
    [1]
]
map_control_b1 = [
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 1, 1, 0, 0],
    [0, 0, 1, 0, 0],
    [0, 0, 1, 1, 0]
]

map_control_b2 = [
    [0, 0, 0, 0, 0],
    [1, 1, 1, 0, 0],
    [0, 1, 0, 0, 0],
    [0, 1, 0, 0, 0],
    [0, 1, 0, 0, 0]
]

# target
map_target = [[0] * WIDTH_TARGET for _ in range(HEIGHT_TARGET)]

# hole
for i in range(HEIGHT_TARGET - 6, HEIGHT_TARGET):
    for j in range(WIDTH_TARGET):
        map_target[i][j] = 1
for i in range(6):
    map_target[4][i+8] = 0
for i in range(3):
    map_target[5][i+10] = 0

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


clock = pygame.time.Clock()
game_over = False
stage = 0
shape_position = [[0,2], [2,0], [15,0]]

# Game Loof
while not game_over:
    stage_end = False

    while not stage_end:
        move = 0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game_over, stage_end = True, True
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

        if stage == 0:
            if move == 3:   # down
                shape_position[0], _ = move_shape(shape_control_a, shape_position[0], map_control_a, WIDTH_A, HEIGHT_A, 0, 1)
            elif move == 4: # up
                shape_position[0], _ = move_shape(shape_control_a, shape_position[0], map_control_a, WIDTH_A, HEIGHT_A, 0, -1)
            elif move == 5: # space
                stage = 1
            if move:
                print(shape_position)
        
        if stage == 1:
            if move == 1:   # left
                shape_position[1] = hard_drop(shape_control_b, shape_position[1], rotate_clockwise(map_control_b1), WIDTH_B, HEIGHT_B)
                print(map_control_b1)
                
            elif move == 2: # right
                shape_position[1] = hard_drop(shape_control_b, shape_position[1], rotate_counterclockwise(map_control_b2), WIDTH_B, HEIGHT_B)
                print(map_control_b2)
