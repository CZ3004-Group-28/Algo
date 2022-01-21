from consts import WIDTH, HEIGHT


def is_valid(center_x: int, center_y: int):
    return center_x > 0 and center_y > 0 and center_x < WIDTH - 1 and center_y < HEIGHT - 1
