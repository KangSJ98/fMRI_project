from Utils.utils import *
from InitData.b_234DB import *

# control_b
shape_control_b = [
    [1]
]

def option_score(target):
    """
    input:
    target array

    output:
    left_result, right_result
    {shape name : [min_hole, min_hole_position, min_flat, min_flat_position}
    """
    target_copy = [row[:] for row in target]
    result_database_right = {}
    result_database_left = {}
    # left and right
    for select_right in range(2):
        if select_right:
            database = right_database
        else:
            database = left_database
        
        # for all option b
        for shape_name, matrix in database.items():
            shape_position = [[0,0], [0,0], [0,0]]
            min_hole = float('inf')
            min_flat = float('inf')

            # for all option a
            for i in range(HEIGHT_A):
                if select_right:
                    matrix = flip_horizontally(matrix)
                rotated_matrix = rotate_counterclockwise(matrix)
                shape_position = [[0,0], [i,0], [0,0]]

                # check b possible
                if rotated_matrix[0][shape_position[1][0]] == 1 or check_b_possible(rotated_matrix, hard_drop(shape_control_b, shape_position[1], rotated_matrix, WIDTH_B, HEIGHT_B)):
                    continue
                else:
                    rotated_matrix[shape_position[1][1]][shape_position[1][0]] = 1
                
                combine_matrix = rotate_clockwise(rotated_matrix)
                if select_right:
                    combine_matrix = flip_horizontally(combine_matrix)
                
                left = hard_drop(rotate_counterclockwise(combine_matrix), shape_position[2], rotate_counterclockwise(target_copy), HEIGHT_TARGET, WIDTH_TARGET)
                right = hard_drop(rotate_clockwise(combine_matrix), [HEIGHT_TARGET-HEIGHT_B,0], rotate_clockwise(target_copy), HEIGHT_TARGET, WIDTH_TARGET)

                # for all possible location of combine shape
                for j in range(WIDTH_TARGET - left[1] - WIDTH_B, right[1]):
                    shape_position[2] = hard_drop(combine_matrix, [j,0], target_copy, WIDTH_TARGET, HEIGHT_TARGET)
                    hole = count_orphan_hole(target_copy, combine_matrix, shape_position[2])
                    flatness = measure_flatness_std(target_copy, combine_matrix, shape_position[2])

                    if min_hole > hole:
                        min_hole = hole
                        min_hole_position = shape_position[2]
                    if min_flat > flatness:
                        min_flat = flatness
                        min_flat_position = shape_position[2]
            if select_right:
                result_database_right[shape_name] = [min_hole, min_hole_position, min_flat, min_flat_position]
            else:
                result_database_left[shape_name] = [min_hole, min_hole_position, min_flat, min_flat_position]
    return result_database_left, result_database_right

def count_orphan_hole(target, combine_matrix, shape_position):
    """
    input
    target array
    combine matrix : option a + option b
    shape position : [j,0]

    output
    number of orphan hole
    0 is the best
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
    input
    target array
    combine matrix : option a + option b
    shape position : [j,0]

    output
    flatness of (option b + target) - flatness of (target)
    flatness : std of each colume
    lower is better
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
    input
    target array
    combine matrix : option a + option b
    shape position : [j,0]

    output
    접하지 않는 테두리 수 / 전체 테두리 수 (0~1)
    lower is better
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
    """
    input
    target
    cell position(row, col)

    output
    number of 1 and 2 in the neighbor
    """
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
    input
    two vector

    output
    euclidean distance between two vectors
    """
    return np.sqrt(np.sum((np.array(a[1:]) - np.array(b[1:]))**2))

def find_closest_shape(data, option, score):
    closest_shapes = []
    min_difference = float('inf')

    for shape_name, values in data.items():
        difference = abs(score - values[2 * option])

        if difference < min_difference:
            min_difference = difference
            closest_shapes = [shape_name]
        elif difference == min_difference:
            closest_shapes.append(shape_name)

    if not closest_shapes:
        return None

    return random.choice(closest_shapes)
