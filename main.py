import heapq
import math
import time
from python_tsp.exact import solve_tsp_dynamic_programming
import numpy as np
import pandas as pd

from consts import Direction, MOVE_DIRECTION, TURN_FACTOR


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

    def get_view_state(self) -> CellState:
        """
        This function returns the CellState that the robot can view image of the obstacle
        :return:
        """
        if self.direction == Direction.NORTH:
            return CellState(self.x, self.y + 1, Direction.SOUTH)
        elif self.direction == Direction.SOUTH:
            return CellState(self.x, self.y - 1, Direction.NORTH)
        elif self.direction == Direction.EAST:
            return CellState(self.x + 1, self.y, Direction.WEST)
        elif self.direction == Direction.WEST:
            return CellState(self.x - 1, self.y, Direction.EAST)


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

        for ob in self.obstacles:
            if ob.cmp_position(x, y):
                return False

        return True

    def is_valid_coord(self, x: int, y: int) -> bool:
        if x < 0 or x >= self.size_x or y < 0 or y >= self.size_y:
            return False

        return True

    def is_valid_cell_state(self, state: CellState) -> bool:
        return self.is_valid_coord(state.x, state.y)

    def get_view_obstacle_positions(self) -> [CellState]:
        """
        This function return a list of desired states for the robot to achieve based on the obstacle position and direction.
        The state is the position that the robot can see the image of the obstacle.
        :return: [CellState]
        """
        optimal_positions = []
        for ob in self.obstacles:
            view_state = ob.get_view_state()
            if self.is_valid_cell_state(view_state):
                optimal_positions.append(view_state)

        return optimal_positions


class Robot:
    def __init__(self, start_x: int, start_y: int, start_direction: Direction):
        self.states: [CellState] = [CellState(start_x, start_y, start_direction)]

    def get_current_state(self):
        return self.states[-1]

    def get_start_state(self):
        return self.states[0]

    def update_state(self, x, y, direction: Direction) -> CellState:
        new_state = CellState(x, y, direction)
        self.states.append(new_state)
        return new_state

    def clockwise(self) -> CellState:
        current_state = self.get_current_state()
        new_direction = Direction.clockwise(current_state.direction)
        return self.update_state(current_state.x, current_state.y, new_direction)

    def anti_clockwise(self) -> CellState:
        current_state = self.get_current_state()
        new_direction = Direction.anti_clockwise(current_state.direction)
        return self.update_state(current_state.x, current_state.y, new_direction)

    def move_forward(self) -> CellState:
        current_state = self.get_current_state()

        if current_state.direction == Direction.NORTH:
            return self.update_state(current_state.x, current_state.y + 1, current_state.direction)

        elif current_state.direction == Direction.EAST:
            return self.update_state(current_state.x + 1, current_state.y, current_state.direction)

        elif current_state.direction == Direction.WEST:
            return self.update_state(current_state.x - 1, current_state.y, current_state.direction)

        elif current_state.direction == Direction.SOUTH:
            return self.update_state(current_state.x, current_state.y - 1, current_state.direction)


#
# class OptimalOrderStore:
#     """
#     Class to temporarily stores the traversal orders of the robot
#     """
#
#     def __init__(self):
#         self.orders = []
#         self.optimal_cost = float("inf")
#
#     def update_orders(self, new_orders: [CellState], new_optimal_cost: int):
#         self.orders = []
#         for o in new_orders:
#             self.orders.append(o)
#
#         self.optimal_cost = new_optimal_cost


class MazeSolver:
    def __init__(
            self,
            size_x: int,
            size_y: int,
            robot_x: int,
            robot_y: int,
            robot_direction: Direction
    ):
        self.grid = Grid(size_x, size_y)
        self.robot = Robot(robot_x, robot_y, robot_direction)

    def add_obstacle(self, x: int, y: int, direction: Direction):
        obstacle = Obstacle(x, y, direction)
        self.grid.add_obstacle(obstacle)

    def reset_obstacles(self):
        self.grid.reset_obstacles()

    @staticmethod
    def compute_coord_distance(x1: int, y1: int, x2: int, y2: int, level=1):
        horizontal_distance = x1 - x2
        vertical_distance = y1 - y2

        if level == 2:
            # Euclidean distance
            return math.sqrt(horizontal_distance ** 2 + vertical_distance ** 2)

        return abs(horizontal_distance) + abs(vertical_distance)

    @staticmethod
    def compute_state_distance(start_state: CellState, end_state: CellState, level=1):
        return MazeSolver.compute_coord_distance(start_state.x, start_state.y, end_state.x, end_state.y, level)

    # def get_optimal_traversal_order(self) -> [CellState]:
    #     # calculate optimal_cost table
    #     items = [self.robot.get_start_state()]
    #
    #     for ob in self.grid.get_view_obstacle_positions():
    #         items.append(ob)
    #
    #     cost_table = np.zeros((len(items), len(items)))
    #     for s in range(len(items) - 1):
    #         for e in range(s + 1, len(items)):
    #             cost_table[s][e] = self.compute_state_distance(items[s], items[e])
    #             cost_table[e][s] = cost_table[s][e]
    #
    #     optimal_order = OptimalOrderStore()
    #
    #     def recursive_optimal(current_index: int, current_cost: int, visited: [CellState]):
    #         if current_cost >= optimal_order.optimal_cost:
    #             return
    #
    #         if len(visited) == len(items):
    #             optimal_order.update_orders(visited, current_cost)
    #             return
    #
    #         for i in range(1, len(items)):
    #             # skip index 0 as it is the start position of the robot
    #             if items[i] not in visited:
    #                 visited.append(items[i])
    #                 # cost of moving from current item to the next item
    #                 move_cost = cost_table[current_index][i]
    #                 recursive_optimal(i, current_cost + move_cost, visited)
    #                 visited.pop()
    #
    #     recursive_optimal(0, 0, [items[0]])
    #     return optimal_order

    def get_optimal_order_dp(self) -> [CellState]:
        # calculate optimal_cost table
        items = [self.robot.get_start_state()]

        for ob in self.grid.get_view_obstacle_positions():
            items.append(ob)

        cost_table, path_table = self.path_cost_generator(items)
        cost_np = np.zeros((len(items), len(items)))

        for s in range(len(items) - 1):
            for e in range(s + 1, len(items)):
                cost_np[s][e] = cost_table[(items[s], items[e])]
                cost_np[e][s] = cost_np[s][e]

        cost_np[:, 0] = 0
        permutation, distance = solve_tsp_dynamic_programming(cost_np)
        optimal_path = [items[0]]

        for i in range(len(permutation) - 1):
            from_item = items[permutation[i]]
            to_item = items[permutation[i + 1]]

            cur_path = path_table[(from_item, to_item)]
            for j in range(1, len(cur_path)):
                optimal_path.append(CellState(cur_path[j][0], cur_path[j][1], cur_path[j][2]))

        return optimal_path, distance

    def get_neighbors(self, x, y):
        """
        Return a list of tuples with format:
        newX, newY, new_direction
        """
        neighbors = []

        for dx, dy, md in MOVE_DIRECTION:
            if self.grid.reachable(x + dx, y + dy):
                neighbors.append((x + dx, y + dy, md))

        return neighbors

    def path_cost_generator(self, states: [CellState]):
        path_table = dict()
        cost_table = dict()

        def record_path(start, end, parent: dict, cost: int):
            cost_table[(start, end)] = cost
            cost_table[(end, start)] = cost

            path = []
            cursor = (end.x, end.y, end.direction)

            while cursor in parent:
                path.append(cursor)
                cursor = parent[cursor]

            path.append(cursor)

            path_table[(start, end)] = path[::-1]
            path_table[(end, start)] = path

        def astar_search(start: CellState, end: CellState):
            # astar search algo with three states: x, y, direction
            if (start, end) in path_table:
                return

            # use heuristics to guide the search: distance is calculated by f = g + h
            # g is the actual distance moved so far from the start node to current node
            # h is the heuristic distance from current node to end node
            g_distance = {(start.x, start.y, start.direction): 0}

            # format of each item in heap: (f_distance of node, x coord of node, y coord of node)
            heap = [(self.compute_state_distance(start, end), start.x, start.y, start.direction)]
            parent = dict()
            visited = set()

            while heap:
                _, cur_x, cur_y, cur_direction = heapq.heappop(heap)

                if (cur_x, cur_y, cur_direction) in visited:
                    continue

                if end.is_eq(cur_x, cur_y, cur_direction):
                    record_path(start, end, parent, g_distance[(cur_x, cur_y, cur_direction)])
                    return

                visited.add((cur_x, cur_y, cur_direction))
                cur_distance = g_distance[(cur_x, cur_y, cur_direction)]

                for next_x, next_y, new_direction in self.get_neighbors(cur_x, cur_y):
                    if (next_x, next_y, new_direction) in visited:
                        continue

                    move_cost = Direction.rotation_cost(new_direction, cur_direction) * TURN_FACTOR + 1
                    # new cost is calculated by the cost to reach current state + cost to move from
                    # current state to new state + heuristic cost from new state to end state
                    next_cost = cur_distance + move_cost + \
                                self.compute_coord_distance(next_x, next_y, end.x, end.y)

                    if (next_x, next_y) not in g_distance or \
                            g_distance[(next_x, next_y, new_direction)] > cur_distance + move_cost:
                        g_distance[(next_x, next_y, new_direction)] = cur_distance + move_cost
                        parent[(next_x, next_y, new_direction)] = (cur_x, cur_y, cur_direction)

                        heapq.heappush(heap, (next_cost, next_x, next_y, new_direction))

        for i in range(len(states) - 1):
            for j in range(i + 1, len(states)):
                astar_search(states[i], states[j])

        return cost_table, path_table


if __name__ == '__main__':
    maze_solver = MazeSolver(20, 20, 0, 0, Direction.NORTH)
    maze_solver.add_obstacle(5, 7, Direction.SOUTH)
    maze_solver.add_obstacle(5, 13, Direction.WEST)
    maze_solver.add_obstacle(15, 4, Direction.NORTH)
    maze_solver.add_obstacle(12, 9, Direction.EAST)
    maze_solver.add_obstacle(15, 15, Direction.SOUTH)
    # maze_solver.add_obstacle(9, 1, Direction.NORTH)
    # maze_solver.add_obstacle(19, 19, Direction.WEST)
    # maze_solver.add_obstacle(1, 16, Direction.EAST)
    # maze_solver.add_obstacle(8, 8, Direction.WEST)
    # maze_solver.add_obstacle(10, 18, Direction.SOUTH)
    # maze_solver.add_obstacle(4, 10, Direction.WEST)

    print("Manual A*")
    start = time.time()
    optimal_path, distance = maze_solver.get_optimal_order_dp()
    print(time.time() - start)
    print(distance)
    for o in optimal_path:
        print(o)

    viz = [[0 for i in range(20)] for j in range(20)]
    viz[5][7] = None
    viz[5][13] = None
    viz[15][4] = None
    viz[12][9] = None
    viz[15][15] = None
    # viz[9][1] = None
    # viz[19][19] = None
    # viz[1][16] = None
    # viz[8][8] = None

    counter = 1
    for o in optimal_path:
        viz[o.x][o.y] = counter
        counter += 1

    df = pd.DataFrame(np.rot90(viz, 1))
    df.to_csv('test.csv')
