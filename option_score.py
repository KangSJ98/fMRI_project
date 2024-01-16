from utils import *
from InitData.Block_Shape_345DB import b_database
import numpy as np

WIDTH_SCREEN, HEIGHT_SCREEN = 1404, 920
BLOCK_SIZE = 40
WIDTH_GAME, HEIGHT_GAME = 35, 22
WIDTH_A, HEIGHT_A = 1, 5
WIDTH_B, HEIGHT_B = 5, 5
WIDTH_TARGET, HEIGHT_TARGET = 20, 14

# control_b
shape_control_b = [
    [1]
]

def option_score_left(target):
    target_copy = [row[:] for row in target]
    orphan_result_databases = {}
    flatness_result_databases = {}
    for shape_name, matrix in b_database.items():
        shape_position = [[0,2], [0,0], [0,0]] # a(0,0~4), a(0~4,0), b(0~width, 0)
        min_hole = float('inf')
        min_flat = float('inf')

        for i in range(5):
            rotated_matrix = rotate_counterclockwise(matrix)
            shape_position[1] = [i,0]
            shape_position[2] = [0,0]
            if rotated_matrix[0][shape_position[1][0]] == 1 or check_b_possible(rotated_matrix, hard_drop(shape_control_b, shape_position[1], rotated_matrix, WIDTH_B, HEIGHT_B)):
                continue
            else:
                rotated_matrix[shape_position[1][1]][shape_position[1][0]] = 1
                
            combine_matrix = rotate_clockwise(rotated_matrix)
            left = hard_drop(rotate_counterclockwise(combine_matrix), shape_position[2], rotate_counterclockwise(target_copy), HEIGHT_TARGET, WIDTH_TARGET)
            right = hard_drop(rotate_clockwise(combine_matrix), [HEIGHT_TARGET-HEIGHT_B,0], rotate_clockwise(target_copy), HEIGHT_TARGET, WIDTH_TARGET)
            for j in range(WIDTH_TARGET - left[1] - WIDTH_B, right[1]):
                shape_position[2] = hard_drop(combine_matrix, [j,0], target_copy, WIDTH_TARGET, HEIGHT_TARGET)
                hole = count_orphan_hole(target_copy, combine_matrix, shape_position[2])
                flatness = measure_flatness_std(target_copy, combine_matrix, shape_position[2])
                if hole < min_hole:
                    min_hole = hole
                if flatness < min_flat:
                    min_flat = flatness
        orphan_result_databases[shape_name] = min_hole
        flatness_result_databases[shape_name] = min_flat
    return orphan_result_databases, flatness_result_databases

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
                for i in range(y,0,-1):
                    if target_copy[i][x] == 2:
                        hole += 1
                        break
                    elif target_copy[i][x] == 1:
                        break

    return hole

def measure_flatness_std(target, combine_matrix, shape_position):
    target_copy = [row[:] for row in target]
    target_height = [sum(column) for column in zip(*target_copy)]
    std_target = np.std(target_height)
    
    for y, row in enumerate(combine_matrix):
        for x, value in enumerate(row):
            if value:
                target_copy[shape_position[1] + y][shape_position[0] + x] = 2
    
    combine_height = [sum(column) for column in zip(*target_copy)]
    std_combine = np.std(combine_height)

    return std_combine - std_target
