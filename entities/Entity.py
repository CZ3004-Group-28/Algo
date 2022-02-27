from consts import Direction, EXPANDED_CELL, MOVE_DIRECTION
from helper import is_valid


class CellState:
    def __init__(self, x, y, direction: Direction = Direction.NORTH, screenshot_id=-1):
        self.x = x
        self.y = y
        self.direction = direction
        self.screenshot_id = screenshot_id  # if screenshot_od != -1, the snapshot is taken at that position is for the obstacle with id = screenshot_id

    def cmp_position(self, x, y) -> bool:
        return self.x == x and self.y == y

    def is_eq(self, x, y, direction):
        return self.x == x and self.y == y and self.direction == direction

    def __repr__(self):
        return "x: {}, y: {}, d: {}".format(self.x, self.y, self.direction)

    def set_screenshot(self, screenshot_id):
        self.screenshot_id = screenshot_id

    def get_dict(self):
        return {'x': self.x, 'y': self.y, 'd': self.direction, 's': self.screenshot_id}


class Obstacle(CellState):
    def __init__(self, x: int, y: int, direction: Direction, obstacle_id: int):
        super().__init__(x, y, direction)
        self.obstacle_id = obstacle_id

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.direction == other.direction

    def get_view_state(self) -> [CellState]:
        """
        This function returns the list of CellState that the robot can view image of the obstacle
        :return:
        """
        cells = []
        if self.direction == Direction.NORTH:
            if is_valid(self.x, self.y + EXPANDED_CELL * 2):
                cells.append(CellState(self.x, self.y + EXPANDED_CELL * 2,
                                       Direction.SOUTH, self.obstacle_id))

            if is_valid(self.x, self.y + 1 + EXPANDED_CELL * 2):
                cells.append(CellState(self.x, self.y + 1 + EXPANDED_CELL * 2,
                                       Direction.SOUTH, self.obstacle_id))

            if is_valid(self.x, self.y + 2 + EXPANDED_CELL * 2):
                cells.append(CellState(self.x, self.y + 2 + EXPANDED_CELL * 2,
                                       Direction.SOUTH, self.obstacle_id))

            # if is_valid(self.x + 1 + EXPANDED_CELL * 2, self.y + 1 + EXPANDED_CELL * 2):
            #     cells.append(CellState(self.x + 1 + EXPANDED_CELL * 2, self.y + 1 + EXPANDED_CELL * 2,
            #                            Direction.EAST_SOUTH))
            #
            # if is_valid(self.x - 1 - EXPANDED_CELL * 2, self.y + 1 + EXPANDED_CELL * 2):
            #     cells.append(CellState(self.x - 1 - EXPANDED_CELL * 2, self.y + 1 + EXPANDED_CELL * 2,
            #                            Direction.SOUTH_WEST))

        elif self.direction == Direction.SOUTH:
            if is_valid(self.x, self.y - EXPANDED_CELL * 2):
                cells.append(CellState(self.x, self.y - EXPANDED_CELL * 2,
                                       Direction.NORTH, self.obstacle_id))

            if is_valid(self.x, self.y - 1 - EXPANDED_CELL * 2):
                cells.append(CellState(self.x, self.y - 1 - EXPANDED_CELL * 2,
                                       Direction.NORTH, self.obstacle_id))

            if is_valid(self.x, self.y - 2 - EXPANDED_CELL * 2):
                cells.append(CellState(self.x, self.y - 2 - EXPANDED_CELL * 2,
                                       Direction.NORTH, self.obstacle_id))

            # if is_valid(self.x + 1 + EXPANDED_CELL * 2, self.y - 1 - EXPANDED_CELL * 2):
            #     cells.append(CellState(self.x + 1 + EXPANDED_CELL * 2, self.y - 1 - EXPANDED_CELL * 2,
            #                            Direction.WEST_NORTH))
            #
            # if is_valid(self.x - 1 - EXPANDED_CELL * 2, self.y - 1 - EXPANDED_CELL * 2):
            #     cells.append(CellState(self.x - 1 - EXPANDED_CELL * 2, self.y - 1 - EXPANDED_CELL * 2,
            #                            Direction.NORTH_EAST))

        elif self.direction == Direction.EAST:
            if is_valid(self.x + EXPANDED_CELL * 2, self.y):
                cells.append(CellState(self.x + EXPANDED_CELL * 2, self.y,
                                       Direction.WEST, self.obstacle_id))

            if is_valid(self.x + 1 + EXPANDED_CELL * 2, self.y):
                cells.append(CellState(self.x + 1 + EXPANDED_CELL * 2, self.y,
                                       Direction.WEST, self.obstacle_id))

            if is_valid(self.x + 2 + EXPANDED_CELL * 2, self.y):
                cells.append(CellState(self.x + 2 + EXPANDED_CELL * 2, self.y,
                                       Direction.WEST, self.obstacle_id))

            # if is_valid(self.x + 1 + EXPANDED_CELL * 2, self.y + 1 + EXPANDED_CELL * 2):
            #     cells.append(CellState(self.x + 1 + EXPANDED_CELL * 2, self.y + 1 + EXPANDED_CELL * 2,
            #                            Direction.SOUTH_WEST))
            #
            # if is_valid(self.x + 1 + EXPANDED_CELL * 2, self.y - 1 - EXPANDED_CELL * 2):
            #     cells.append(CellState(self.x + 1 + EXPANDED_CELL * 2, self.y - 1 - EXPANDED_CELL * 2,
            #                            Direction.WEST_NORTH))

        elif self.direction == Direction.WEST:
            if is_valid(self.x - EXPANDED_CELL * 2, self.y):
                cells.append(CellState(self.x - EXPANDED_CELL * 2, self.y,
                                       Direction.EAST, self.obstacle_id))

            if is_valid(self.x - 1 - EXPANDED_CELL * 2, self.y):
                cells.append(CellState(self.x - 1 - EXPANDED_CELL * 2, self.y,
                                       Direction.EAST, self.obstacle_id))

            if is_valid(self.x - 2 - EXPANDED_CELL * 2, self.y):
                cells.append(CellState(self.x - 2 - EXPANDED_CELL * 2, self.y,
                                       Direction.EAST, self.obstacle_id))

            # if is_valid(self.x - 1 - EXPANDED_CELL * 2, self.y + 1 + EXPANDED_CELL * 2):
            #     cells.append(CellState(self.x - 1 - EXPANDED_CELL * 2, self.y + 1 + EXPANDED_CELL * 2,
            #                            Direction.EAST_SOUTH))
            #
            # if is_valid(self.x - 1 - EXPANDED_CELL * 2, self.y - 1 - EXPANDED_CELL * 2):
            #     cells.append(CellState(self.x - 1 - EXPANDED_CELL * 2, self.y - 1 - EXPANDED_CELL * 2,
            #                            Direction.NORTH_EAST))

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

    def reachable(self, x: int, y: int) -> bool: # TODO: adjust;
        if not self.is_valid_coord(x, y):
            return False

        for ob in self.obstacles:  # handle the virtual expansion of the obstacles
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
            view_states = [view_state for view_state in ob.get_view_state() if
                           self.reachable(view_state.x, view_state.y)]
            optimal_positions.append(view_states)

        return optimal_positions


class Wall:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

class GridFastestCar:
    def __init__(self, size_x: int, size_y: int, robot_x: int, robot_y: int, goal_x: int, goal_y: int):
        self.size_x = size_x
        self.size_y = size_y
        self.robot_x = robot_x
        self.robot_y = robot_y
        self.walls = []
        self.goal_x = goal_x
        self.goal_y = goal_y

        self.add_car_park()
        self.add_goal_wall()

    def is_valid_coord(self, x: int, y: int) -> bool:
        if x < 1 or x >= self.size_x - 1 or y < 1 or y >= self.size_y - 1:
            return False

        return True

    def is_valid_cell_state(self, state: CellState) -> bool:
        return self.is_valid_coord(state.x, state.y)

    def add_goal_wall(self):
        # size of wall is 10x60
        for i in range(6):
            self.walls.append(Wall(self.goal_x + i, self.goal_y))

    def add_car_park(self):
        if self.robot_y < 2:
            raise Exception('Invalid car park position')
        for i in range(-3, 5):
            self.walls.append(Wall(self.robot_x + i, self.robot_y - 2))

        for i in range(-1, 4):
            self.walls.append(Wall(self.robot_x - 3, self.robot_y + i))
            self.walls.append(Wall(self.robot_x + 4, self.robot_y + i))

    def reachable(self, x: int, y: int):
        if not self.is_valid_coord(x, y):
            return False

        for w in self.walls:  # handle the virtual expansion of the obstacles
            if max(abs(w.x - x), abs(w.y - y)) < EXPANDED_CELL * 2 + 1:
                return False

        return True

    def get_possible_path_options(self):
        # try to generate possible path that robot can travel around the goal obstacle
        options = []

        for i in range(7):
            for j in range(3):
                for k in range(2):
                    for t in range(2):
                        positions = [CellState(self.robot_x, self.robot_y, Direction.NORTH), # start position of robot
                                     CellState(self.goal_x + i, self.goal_y - 3 - j, Direction.NORTH), # point below goal ob
                                     CellState(self.goal_x + 8, self.goal_y + k, Direction.NORTH),# point right next to goal ob
                                     CellState(self.goal_x + 3, self.goal_y + 3 + t, Direction.WEST), # point upon goal ob
                                     CellState(self.goal_x - 3, self.goal_y, Direction.SOUTH), # point on the left of ob
                                     CellState(self.robot_x, self.robot_y + 1, Direction.SOUTH)] # car park

                        options.append(positions)
        return options
