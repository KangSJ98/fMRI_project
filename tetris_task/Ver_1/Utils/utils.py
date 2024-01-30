WIDTH_SCREEN, HEIGHT_SCREEN = 1404, 920
BLOCK_SIZE = 40
WIDTH_GAME, HEIGHT_GAME = 35, 22
WIDTH_A, HEIGHT_A = 1, 4
WIDTH_B, HEIGHT_B = 4, 4
WIDTH_TARGET, HEIGHT_TARGET = 20, 14

def clear_previous_position(current_shape, shape_position, current_map, map_widgh, map_height):
    for y, row in enumerate(current_shape):
        for x, value in enumerate(row):
            if value:
                if 0<= shape_position[0] + x < map_widgh and 0<= shape_position[1] + y < map_height:
                    current_map[shape_position[1] + y][shape_position[0] + x] = 0
    
    return current_map

def move_shape(current_shape, shape_position, current_map, map_width, map_height, dx, dy):
    """
    input
    current shape
    shape position [x,y]
    dx
    dy

    output
    shape position [x + dx, y + dy]
    can move (if can return ture)
    """
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

def remove_line(current_map, score):
    """
    input
    target

    if the target row has no 0, remove

    output
    target
    """
    for y in range(HEIGHT_TARGET):
        if all(cell != 0 for cell in current_map[y]):
            del current_map[y]
            current_map.insert(0, [0] * WIDTH_TARGET)
            score += 1
        
    return current_map, score

def check_trial_over(current_map):
    """
    input
    target

    output
    if block over 9 line return true
    """
    if sum(current_map[HEIGHT_TARGET-10]) > 0:
        return True
    else:
        return False

def hard_drop(current_shape, shape_position, current_map, map_width, map_height):
    """
    input
    current shape
    shape position [x,y]
    current map

    output
    hard drop position of current shape [x',y']
    """
    position_copy = shape_position
    can_move = True
    while can_move:
        position_copy, can_move = move_shape(current_shape, position_copy, current_map, map_width, map_height, 0, 1)
    return position_copy

def rotate_clockwise(array):
    """
    rotate array clockwise
    """
    return [list(row) for row in zip(*reversed(array))]

def rotate_counterclockwise(array):
    """
    rotate array counter clockwise
    """
    return [list(row) for row in reversed(list(zip(*array)))]

def flip_horizontally(array):
    """
    flip array horizontally
    """
    return [row[::-1] for row in array]

# check control_b attach b1 or b2
def check_b_possible(current_map, shape_position):
    """
    input
    option b
    option a position [x,y]

    return
    a + b is devide?
    if devide : true
    """
    devide = (current_map[max(0, shape_position[1] - 1)][shape_position[0]] + 
                current_map[shape_position[1]][max(0, shape_position[0] - 1)] + 
                current_map[min(HEIGHT_B - 1, shape_position[1] + 1)][shape_position[0]] + 
                current_map[shape_position[1]][min(WIDTH_B - 1, shape_position[0] + 1)]
    )
    if devide:
        return False
    else:
        return True
