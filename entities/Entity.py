from consts import Direction, EXPANDED_CELL, MOVE_DIRECTION
from utils import is_valid


class CellState:
    def __init__(self, x, y, direction: Direction = Direction.NORTH):
        self.x = x
        self.y = y
        self.direction = direction

    def cmp_position(self, x, y) -> bool:
        return self.x == x and self.y == y

    def is_eq(self, x, y, direction):
        return self.x == x and self.y == y and self.direction == direction

    def __repr__(self):
        return "x: {}, y: {}, d: {}".format(self.x, self.y, self.direction)


class Obstacle(CellState):
    def __init__(self, x: int, y: int, direction: Direction):
        super().__init__(x, y, direction)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.direction == other.direction

    def get_view_state(self) -> [CellState]:
        """
        This function returns the list of CellState that the robot can view image of the obstacle
        :return:
        """
        cells = []
        if self.direction == Direction.NORTH:
            if is_valid(self.x, self.y + 1 + EXPANDED_CELL * 2):
                cells.append(CellState(self.x, self.y + 1 + EXPANDED_CELL * 2,
                                       Direction.SOUTH))

            if is_valid(self.x, self.y + 2 + EXPANDED_CELL * 2):
                cells.append(CellState(self.x, self.y + 2 + EXPANDED_CELL * 2,
                                       Direction.SOUTH))

            if is_valid(self.x + 1 + EXPANDED_CELL * 2, self.y + 1 + EXPANDED_CELL * 2):
                cells.append(CellState(self.x + 1 + EXPANDED_CELL * 2, self.y + 1 + EXPANDED_CELL * 2,
                                       Direction.EAST_SOUTH))

            if is_valid(self.x - 1 - EXPANDED_CELL * 2, self.y + 1 + EXPANDED_CELL * 2):
                cells.append(CellState(self.x - 1 - EXPANDED_CELL * 2, self.y + 1 + EXPANDED_CELL * 2,
                                       Direction.SOUTH_WEST))

        elif self.direction == Direction.SOUTH:
            if is_valid(self.x, self.y - 1 - EXPANDED_CELL * 2):
                cells.append(CellState(self.x, self.y - 1 - EXPANDED_CELL * 2,
                                       Direction.NORTH))

            if is_valid(self.x, self.y - 2 - EXPANDED_CELL * 2):
                cells.append(CellState(self.x, self.y - 2 - EXPANDED_CELL * 2,
                                       Direction.NORTH))

            if is_valid(self.x + 1 + EXPANDED_CELL * 2, self.y - 1 - EXPANDED_CELL * 2):
                cells.append(CellState(self.x + 1 + EXPANDED_CELL * 2, self.y - 1 - EXPANDED_CELL * 2,
                                       Direction.WEST_NORTH))

            if is_valid(self.x - 1 - EXPANDED_CELL * 2, self.y - 1 - EXPANDED_CELL * 2):
                cells.append(CellState(self.x - 1 - EXPANDED_CELL * 2, self.y - 1 - EXPANDED_CELL * 2,
                                       Direction.NORTH_EAST))

        elif self.direction == Direction.EAST:
            if is_valid(self.x + 1 + EXPANDED_CELL * 2, self.y):
                cells.append(CellState(self.x + 1 + EXPANDED_CELL * 2, self.y,
                                       Direction.WEST))

            if is_valid(self.x + 2 + EXPANDED_CELL * 2, self.y):
                cells.append(CellState(self.x + 2 + EXPANDED_CELL * 2, self.y,
                                       Direction.WEST))

            if is_valid(self.x + 1 + EXPANDED_CELL * 2, self.y + 1 + EXPANDED_CELL * 2):
                cells.append(CellState(self.x + 1 + EXPANDED_CELL * 2, self.y + 1 + EXPANDED_CELL * 2,
                                       Direction.SOUTH_WEST))

            if is_valid(self.x + 1 + EXPANDED_CELL * 2, self.y - 1 - EXPANDED_CELL * 2):
                cells.append(CellState(self.x + 1 + EXPANDED_CELL * 2, self.y - 1 - EXPANDED_CELL * 2,
                                       Direction.WEST_NORTH))

        elif self.direction == Direction.WEST:
            if is_valid(self.x - 1 - EXPANDED_CELL * 2, self.y):
                cells.append(CellState(self.x - 1 - EXPANDED_CELL * 2, self.y,
                                       Direction.EAST))

            if is_valid(self.x - 2 - EXPANDED_CELL * 2, self.y):
                cells.append(CellState(self.x - 2 - EXPANDED_CELL * 2, self.y,
                                       Direction.EAST))

            if is_valid(self.x - 1 - EXPANDED_CELL * 2, self.y + 1 + EXPANDED_CELL * 2):
                cells.append(CellState(self.x - 1 - EXPANDED_CELL * 2, self.y + 1 + EXPANDED_CELL * 2,
                                       Direction.EAST_SOUTH))

            if is_valid(self.x - 1 - EXPANDED_CELL * 2, self.y - 1 - EXPANDED_CELL * 2):
                cells.append(CellState(self.x - 1 - EXPANDED_CELL * 2, self.y - 1 - EXPANDED_CELL * 2,
                                       Direction.NORTH_EAST))

        return cells


class Grid:
    def __init__(self, size_x: int, size_y: int):
        self.size_x = size_x
        self.size_y = size_y
        self.obstacles: [Obstacle] = []

    def add_obstacle(self, obstacle: Obstacle):
        to_add = True
        for ob in self.obstacles:
            if ob == obstacle:
                to_add = False
                break

        if to_add:
            self.obstacles.append(obstacle)

    def reset_obstacles(self):
        self.obstacles = []

    def get_obstacles(self):
        return self.obstacles

    def reachable(self, x: int, y: int) -> bool:
        if not self.is_valid_coord(x, y):
            return False

        for ob in self.obstacles: # handle the virtual expansion of the obstacles
            if max(abs(ob.x - x), abs(ob.y - y)) < EXPANDED_CELL * 2 + 1:
                return False

        return True

    def is_valid_coord(self, x: int, y: int) -> bool:
        if x < 1 or x >= self.size_x - 1 or y < 1 or y >= self.size_y - 1:
            return False

        return True

    def is_valid_cell_state(self, state: CellState) -> bool:
        return self.is_valid_coord(state.x, state.y)

    def get_view_obstacle_positions(self) -> [[CellState]]:
        """
        This function return a list of desired states for the robot to achieve based on the obstacle position and direction.
        The state is the position that the robot can see the image of the obstacle.
        :return: [[CellState]]
        """
        optimal_positions = []
        for ob in self.obstacles:
            view_states = [view_state for view_state in ob.get_view_state() if self.reachable(view_state.x, view_state.y)]
            assert(len(view_states) > 0)
            optimal_positions.append(view_states)

        return optimal_positions
