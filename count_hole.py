import pygame
import sys

# initiate
pygame.init()

# screen setting
WIDTH, HEIGHT = 480, 520
BLOCK_SIZE = 40
GRID_WIDTH, GRID_HEIGHT = 12, 12
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tetris-like 게임")

# color define
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# control block
SHAPE = [
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 1, 0],
    [0, 1, 1, 1, 0],
    [0, 0, 1, 0, 0]
]
SHAPE_COLOR = RED

# target block
background_map = [
    [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
    [5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5],
    [5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5],
    [5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5],
    [5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5],
    [5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5],
    [5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5],
    [5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5],
    [5, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 5],
    [5, 0, 0, 1, 1, 1, 0, 0, 0, 0, 1, 5],
    [5, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 5],
    [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
]

current_shape = SHAPE
current_color = SHAPE_COLOR
shape_position = [5, 2]

# Function def
def clear_previous_position():
    for y, row in enumerate(current_shape):
        for x, value in enumerate(row):
            if value:
                if 0 <= shape_position[0] + x < GRID_WIDTH and 0 <= shape_position[1] + y < GRID_HEIGHT:
                    background_map[shape_position[1] + y][shape_position[0] + x] = 0

def move_shape(dx, dy):
    clear_previous_position()
    can_move = True
    for y, row in enumerate(current_shape):
        for x, value in enumerate(row):
            if value:
                new_x, new_y = shape_position[0] + dx + x, shape_position[1] + dy + y
                if (
                    0 <= new_x < GRID_WIDTH
                    and 0 <= new_y < GRID_HEIGHT
                    and (background_map[new_y][new_x] == 1 or background_map[new_y][new_x] == 5)
                ):
                    can_move = False
                    break

    if can_move:
        shape_position[0] += dx
        shape_position[0] = max(shape_position[0], 0)
        shape_position[1] += dy
        shape_position[1] = min(shape_position[1], GRID_HEIGHT - len(current_shape))


clock = pygame.time.Clock()
game_over = False

# Game Loof
while not game_over:
    hole = 0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                game_over = True
            elif event.key == pygame.K_LEFT:
                move_shape(-1, 0)
            elif event.key == pygame.K_RIGHT:
                move_shape(1, 0)
            elif event.key == pygame.K_DOWN:
                move_shape(0, 1)
            elif event.key == pygame.K_UP:
                move_shape(0, -1)

    # fill control block into map
    for y, row in enumerate(current_shape):
        for x, value in enumerate(row):
            if value:
                if 0 <= shape_position[0] + x < GRID_WIDTH and 0 <= shape_position[1] + y < GRID_HEIGHT:
                    if not background_map[shape_position[1] + y][shape_position[0] + x]:
                        background_map[shape_position[1] + y][shape_position[0] + x] = 2

    # initiate background white
    WIN.fill(WHITE)

    # dark line grid
    for y in range(GRID_HEIGHT + 1):
        pygame.draw.line(WIN, BLACK, (0, y * BLOCK_SIZE), (GRID_WIDTH * BLOCK_SIZE, y * BLOCK_SIZE))
    for x in range(GRID_WIDTH + 1):
        pygame.draw.line(WIN, BLACK, (x * BLOCK_SIZE, 0), (x * BLOCK_SIZE, GRID_HEIGHT * BLOCK_SIZE))

    # black : target block, red : control block, green : hole
    for y, row in enumerate(background_map):
        for x, value in enumerate(row):
            if value == 1:
                pygame.draw.rect(WIN, BLACK, (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
            elif value == 2:
                pygame.draw.rect(WIN, SHAPE_COLOR, (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
            elif value == 5:
                pygame.draw.rect(WIN, GRAY, (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
            elif value == 0:
                for i in range(y):
                    if background_map[i][x] == 2:
                        pygame.draw.rect(WIN, GREEN, (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
                        hole += 1
                        break
                    pygame.draw.rect(WIN, WHITE, (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

    # show hole #
    font = pygame.font.Font(None, 36)
    text = font.render(f'Hole: {hole}', True, BLACK)
    text_rect = text.get_rect()
    text_rect.bottomleft = (10, WIN.get_height() - 10)
    WIN.blit(text, text_rect)

    # screen update
    pygame.display.update()

    # FPS
    clock.tick(10)


