from Utils.utils import *
from InitData.b_234DB import *
import numpy as np

# control_b
shape_control_b = [
    [1]
]

def option_score(target, right):
    """
    현재 target에 대해 모든 블록들의 점수를 반환
    left : 0, right : 1

    1열 : 블록 이름
    2열 ~ : 각 알고리즘에 해당하는 점수
    """
    target_copy = [row[:] for row in target]
    if right:
        database = right_database
    else:
        database = left_database
    result_database = []

    for shape_name, matrix in database.items():
        shape_position = [[0,2], [0,0], [0,0]] # a(0,0~4), a(0~4,0), b(0~width, 0)
        min_hole = float('inf')
        min_flat = float('inf')
        min_border = float('inf')
        # for all option a
        for i in range(HEIGHT_B):
            if right:
                matrix = flip_horizontally(matrix)
            rotated_matrix = rotate_counterclockwise(matrix)
            shape_position[1] = [i,0]
            shape_position[2] = [0,0]
            if rotated_matrix[0][shape_position[1][0]] == 1 or check_b_possible(rotated_matrix, hard_drop(shape_control_b, shape_position[1], rotated_matrix, WIDTH_B, HEIGHT_B)):
                continue
            else:
                rotated_matrix[shape_position[1][1]][shape_position[1][0]] = 1
            combine_matrix = rotate_clockwise(rotated_matrix)
            if right:
                combine_matrix = flip_horizontally(combine_matrix)

            left = hard_drop(rotate_counterclockwise(combine_matrix), shape_position[2], rotate_counterclockwise(target_copy), HEIGHT_TARGET, WIDTH_TARGET)
            right = hard_drop(rotate_clockwise(combine_matrix), [HEIGHT_TARGET-HEIGHT_B,0], rotate_clockwise(target_copy), HEIGHT_TARGET, WIDTH_TARGET)

            # for all possible location of combine shape 
            for j in range(WIDTH_TARGET - left[1] - WIDTH_B, right[1]):
                shape_position[2] = hard_drop(combine_matrix, [j,0], target_copy, WIDTH_TARGET, HEIGHT_TARGET)
                hole = count_orphan_hole(target_copy, combine_matrix, shape_position[2])
                flatness = measure_flatness_std(target_copy, combine_matrix, shape_position[2])
                border = count_border(target_copy, combine_matrix, shape_position[2])

                min_hole = min(min_hole, hole)
                min_flat = min(min_flat, flatness)
                min_border = min(min_border, border)
        result_database.append([shape_name, min_hole, min_flat, min_border])
    for i in range(len(result_database)):
        print(result_database[i])
    return result_database

def count_orphan_hole(target, combine_matrix, shape_position):
    """
    orphan hole의 개수
    """
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
    """
    도형을 넣은 뒤 평평도 - 넣기 전 평평도
    (평평도 : 높이의 표준편차)
    """
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

def count_border(target, combine_matrix, shape_position):
    """
    도형의 테두리가 target과 얼마나 많이 접하는지
    접하는 테두리 수 / 전체 테두리 수
    """
    target_copy = [row[:] for row in target]
    total_count_1 = 0
    total_count_2 = 0
    
    for y, row in enumerate(combine_matrix):
        for x, value in enumerate(row):
            if value:
                target_copy[shape_position[1] + y][shape_position[0] + x] = 2
    
    for y, row in enumerate(target_copy):
        for x, value in enumerate(row):
            if value == 2:
                count_ones, count_twos = count_neighbors(target_copy, y, x)
                total_count_1 += count_ones
                total_count_2 += count_twos
    border_combine = np.count_nonzero(combine_matrix) * 4 - total_count_2
    border_target = border_combine - total_count_1
    return border_target / border_combine

def count_neighbors(target, row, col):
    count_1 = 0
    count_2 = 0

    neighbors = [(row-1, col), (row+1,col), (row, col-1), (row, col+1)]

    for r, c in neighbors:
        if 0 <= r < len(target) and 0 <= c < len(target[0]):
            if target[r][c] == 1:
                count_1 += 1
            elif target[r][c] == 2:
                count_2 += 1
    
    return count_1, count_2

def euclidean_distance(a, b):
    """
    두 벡터 간의 유클리드 거리 계산
    """
    return np.sqrt(np.sum((np.array(a[1:]) - np.array(b[1:]))**2))

def recommend_similar(current_shape_name, data):
    """
    주어진 데이터에서 현재 도형에 대해 유클리드 거리가 작은 다른 도형을 반환
    """
    target_left = next(item for item in data if item[0] == current_shape_name)
    distances = [(item[0], euclidean_distance(target_left, item)) for item in data]
    distances.sort(key=lambda x: x[1])  # 거리가 작은 순으로 정렬

    return distances[0][0]
