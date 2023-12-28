'''
control_a = 5x1
control_b1 = 5x5 (왼)
control_b2 = 5x5 (오)
target = 14x35, 시작은 하단 6x35 에서만, 9줄을 넘어가면 game over

배경은 흰색, control 배경은 회색, 블록은 검은색, 블록 사이즈를 그리드보다 살짝 작게해서 흰색 배경으로 구분되게
control_b1의 위치는 (8,3) 부터 (12,7))
control_b2의 위치는 (22,3) 부터 (26,7)
control_a의 위치는 (17,3)) 부터 (17,7)
target의 위치는 (0,8) 부터 (34,22)까지

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
WIDTH_SCREEN, HEIGHT_SCREEN = 1400, 920
BLOCK_SIZE = 40
WIDTH_GAME, HEIGHT_GAME = 35, 22
WIDTH_A, HEIGHT_A = 1, 5
WIDTH_B, HEIGHT_B = 5, 5
WIDTH_TARGET, HEIGHT_TARGET = 35, 14
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

def check_b_possible(current_map, shape_position):
    # check control_b attach b1 or b2
    devide = (current_map[max(0, shape_position[1] - 1)][shape_position[0]] + 
                current_map[shape_position[1]][max(0, shape_position[0] - 1)] + 
                current_map[min(HEIGHT_B - 1, shape_position[1] + 1)][shape_position[0]] + 
                current_map[shape_position[1]][min(WIDTH_B - 1, shape_position[0] + 1)]
    )
    if devide:
        return False
    else:
        return True



clock = pygame.time.Clock()
game_over = False


# Game Loof
while not game_over:
    stage_end = False
    phase = 0
    shape_position = [[0,2], [2,0], [15,0]]

    while not stage_end:
        move = 0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game_over, stage_end = True, True
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

        # phase 0
        if phase == 0:
            if move == 3:   # down
                shape_position[0], _ = move_shape(shape_control_a, shape_position[0], map_control_a, WIDTH_A, HEIGHT_A, 0, 1)
            elif move == 4: # up
                shape_position[0], _ = move_shape(shape_control_a, shape_position[0], map_control_a, WIDTH_A, HEIGHT_A, 0, -1)
            elif move == 5: # space
                # hard_drop(shape_control_a, shape_position[0], map_control_a, WIDTH_A, HEIGHT_A)
                shape_position[1][0] = shape_position[0][1]
                phase = 1
        
        # phase 1
        if phase == 1:
            if move == 1:   # left
                rotated_map = rotate_counterclockwise(map_control_b1)

                if rotated_map[0][shape_position[1][0]] == 1 or check_b_possible(rotated_map, hard_drop(shape_control_b, shape_position[1], rotated_map, WIDTH_B, HEIGHT_B)):
                    rotated_map[shape_position[1][1]][shape_position[1][0]] = 3
                    stage_end = True
                else:
                    rotated_map[shape_position[1][1]][shape_position[1][0]] = 1
                    phase = 2

                map_control_b1 = rotate_clockwise(rotated_map)
                shape_combine = map_control_b1
                
            elif move == 2: # right
                shape_position[1][0] = 4 - shape_position[1][0]
                rotated_map = rotate_clockwise(map_control_b2)

                if rotated_map[0][shape_position[1][0]] == 1 or check_b_possible(rotated_map, hard_drop(shape_control_b, shape_position[1], rotated_map, WIDTH_B, HEIGHT_B)):
                    rotated_map[shape_position[1][1]][shape_position[1][0]] = 3
                    stage_end = True
                else:
                    rotated_map[shape_position[1][1]][shape_position[1][0]] = 1
                    phase = 2
                map_control_b2 = rotate_counterclockwise(rotated_map)
                shape_combine = map_control_b2

        # phase 2
        if phase == 2:
            if move == 1:   # left
                shape_position[2], _ = move_shape(shape_combine, shape_position[2], map_target, WIDTH_TARGET, HEIGHT_TARGET, -1, 0)
            if move == 2:   # right
                shape_position[2], _ = move_shape(shape_combine, shape_position[2], map_target, WIDTH_TARGET, HEIGHT_TARGET, 1, 0)


        ### visualization
        ## fill all layer into background map (0 : WHITE, 1 : BLACK, 2 : GRAY)
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
                map_background[y + 8][x] = map_target[y][x]    

        # control combine
        if phase == 2:
            for y in range(HEIGHT_B):
                for x in range(WIDTH_B):
                    map_background[y + shape_position[2][1] + 8][x + shape_position[2][0]] = shape_combine[y][x]

        ## render
        # initiate background white
        WIN.fill(WHITE)

        # 0 : WHITE, 1 : BLACK, 2 : GRAY
        for y, row in enumerate(map_background):
            for x, value in enumerate(row):
                if value == 1:
                    pygame.draw.rect(WIN, BLACK, ((x + 0.1) * BLOCK_SIZE, (y + 0.1) * BLOCK_SIZE, BLOCK_SIZE * 0.9, BLOCK_SIZE * 0.9))
                elif value == 2:
                    pygame.draw.rect(WIN, GRAY, ((x + 0.1) * BLOCK_SIZE, (y + 0.1) * BLOCK_SIZE, BLOCK_SIZE * 0.9, BLOCK_SIZE * 0.9))
                elif value == -1:
                    pygame.draw.rect(WIN, RED, ((x + 0.1) * BLOCK_SIZE, (y + 0.1) * BLOCK_SIZE, BLOCK_SIZE * 0.9, BLOCK_SIZE * 0.9))
        
        # show phase
        font = pygame.font.Font(None, 36)
        text = font.render(f'phase : {phase}', True, BLACK)
        text_rect = text.get_rect()
        text_rect.bottomleft = (10, WIN.get_height() - 10)
        WIN.blit(text, text_rect)

        # screen update
        pygame.display.update()

        # FPS
        clock.tick(10)
