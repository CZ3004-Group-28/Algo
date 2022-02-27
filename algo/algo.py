import heapq
import math
import numpy as np
from entities.Robot import Robot
from entities.Entity import Obstacle, CellState, Grid, GridFastestCar
from consts import Direction, MOVE_DIRECTION, TURN_FACTOR, ITERATIONS, TURN_RADIUS
from python_tsp.exact import solve_tsp_dynamic_programming


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
        self.path_table = dict()
        self.cost_table = dict()

    def add_obstacle(self, x: int, y: int, direction: Direction, obstacle_id: int):
        obstacle = Obstacle(x, y, direction, obstacle_id)
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

    @staticmethod
    def get_visit_options(n):
        s = []
        l = bin(2 ** n - 1).count('1')

        for i in range(2 ** n):
            s.append(bin(i)[2:].zfill(l))

        s.sort(key=lambda x: x.count('1'), reverse=True)
        return s

    def get_optimal_order_dp(self) -> [CellState]:
        distance = 1e9
        optimal_path = []

        # all possible positions to be able to view the obstacles
        all_view_positions = self.grid.get_view_obstacle_positions()

        for op in self.get_visit_options(len(all_view_positions)):
            # op is string of length view position formed by 1 and 0
            # if index == 1 means the view_positions[index] is selected to visit, otherwise drop
            # calculate optimal_cost table
            items = [self.robot.get_start_state()]
            cur_view_positions = []
            print(op)
            for idx in range(len(all_view_positions)):
                if op[idx] == '1':
                    items = items + all_view_positions[idx]
                    cur_view_positions.append(all_view_positions[idx])

            self.path_cost_generator(items)

            combination = []
            self.generate_combination(cur_view_positions, 0, [], combination, [ITERATIONS])

            for c in combination: # run the algo some times ->
                visited_candidates = [0] # add the start state of the robot

                cur_index = 1
                for index, view_position in enumerate(cur_view_positions):
                    visited_candidates.append(cur_index + c[index])
                    cur_index += len(view_position)

                cost_np = np.zeros((len(visited_candidates), len(visited_candidates)))

                for s in range(len(visited_candidates) - 1):
                    for e in range(s + 1, len(visited_candidates)):
                        u = items[visited_candidates[s]]
                        v = items[visited_candidates[e]]
                        if (u, v) in self.cost_table.keys():
                            cost_np[s][e] = self.cost_table[(u, v)]
                        else:
                            cost_np[s][e] = 1e9
                        cost_np[e][s] = cost_np[s][e]
                cost_np[:, 0] = 0
                _permutation, _distance = solve_tsp_dynamic_programming(cost_np)
                if _distance >= distance:
                    continue

                optimal_path = [items[0]]
                distance = _distance

                for i in range(len(_permutation) - 1):
                    from_item = items[visited_candidates[_permutation[i]]]
                    to_item = items[visited_candidates[_permutation[i + 1]]]

                    cur_path = self.path_table[(from_item, to_item)]
                    for j in range(1, len(cur_path)):
                        optimal_path.append(CellState(cur_path[j][0], cur_path[j][1], cur_path[j][2]))

                    optimal_path[-1].set_screenshot(to_item.screenshot_id)

            if optimal_path:
                # if found optimal path, return
                break

        return optimal_path, distance

    @staticmethod
    def generate_combination(view_positions, index, current, result, iteration_left):
        if index == len(view_positions):
            result.append(current[:])
            return

        if iteration_left[0] == 0:
            return

        iteration_left[0] -= 1
        for j in range(len(view_positions[index])):
            current.append(j)
            MazeSolver.generate_combination(view_positions, index + 1, current, result, iteration_left)
            current.pop()

    def get_neighbors(self, x, y, direction):  # TODO: see the behavior of the robot and adjust...
        """
        Return a list of tuples with format:
        newX, newY, new_direction
        """
        neighbors = []
        # assume that after follow this direction, the car direction is EXACTLY md
        for dx, dy, md in MOVE_DIRECTION:
            if md == direction:  # if the new direction == md
                if self.grid.reachable(x + dx, y + dy):  # go forward;
                    neighbors.append((x + dx, y + dy, md))
                if self.grid.reachable(x - dx, y - dy):  # go back;
                    neighbors.append((x - dx, y - dy, md))

            else:  # consider 8 case
                # north <-> east
                if direction == Direction.NORTH and md == Direction.EAST:
                    if self.grid.reachable(x + TURN_RADIUS*3, y + TURN_RADIUS):
                        neighbors.append((x + TURN_RADIUS*3, y + TURN_RADIUS, md))
                    if self.grid.reachable(x - TURN_RADIUS*3, y - TURN_RADIUS):
                        neighbors.append((x - TURN_RADIUS*3, y - TURN_RADIUS, md))

                if direction == Direction.EAST and md == Direction.NORTH:
                    if self.grid.reachable(x + TURN_RADIUS, y + TURN_RADIUS*3):
                        neighbors.append((x + TURN_RADIUS, y + TURN_RADIUS*3, md))
                    if self.grid.reachable(x - TURN_RADIUS, y - TURN_RADIUS*3):
                        neighbors.append((x - TURN_RADIUS, y - TURN_RADIUS*3, md))

                # east <-> south
                if direction == Direction.EAST and md == Direction.SOUTH:
                    if self.grid.reachable(x + TURN_RADIUS, y - TURN_RADIUS*3):
                        neighbors.append((x + TURN_RADIUS, y - TURN_RADIUS*3, md))
                    if self.grid.reachable(x - TURN_RADIUS, y + TURN_RADIUS*3):
                        neighbors.append((x - TURN_RADIUS, y + TURN_RADIUS*3, md))

                if direction == Direction.SOUTH and md == Direction.EAST:
                    if self.grid.reachable(x + TURN_RADIUS*3, y - TURN_RADIUS):
                        neighbors.append((x + TURN_RADIUS*3, y - TURN_RADIUS, md))
                    if self.grid.reachable(x - TURN_RADIUS*3, y + TURN_RADIUS):
                        neighbors.append((x - TURN_RADIUS*3, y + TURN_RADIUS, md))

                # south <-> west
                if direction == Direction.SOUTH and md == Direction.WEST:
                    if self.grid.reachable(x - TURN_RADIUS*3, y - TURN_RADIUS):
                        neighbors.append((x - TURN_RADIUS*3, y - TURN_RADIUS, md))
                    if self.grid.reachable(x + TURN_RADIUS*3, y + TURN_RADIUS):
                        neighbors.append((x + TURN_RADIUS*3, y + TURN_RADIUS, md))

                if direction == Direction.WEST and md == Direction.SOUTH:
                    if self.grid.reachable(x - TURN_RADIUS, y - TURN_RADIUS*3):
                        neighbors.append((x - TURN_RADIUS, y - TURN_RADIUS*3, md))
                    if self.grid.reachable(x + TURN_RADIUS, y + TURN_RADIUS*3):
                        neighbors.append((x + TURN_RADIUS, y + TURN_RADIUS*3, md))

                # west <-> north
                if direction == Direction.WEST and md == Direction.NORTH:
                    if self.grid.reachable(x - TURN_RADIUS, y + TURN_RADIUS*3):
                        neighbors.append((x - TURN_RADIUS, y + TURN_RADIUS*3, md))
                    if self.grid.reachable(x + TURN_RADIUS, y - TURN_RADIUS*3):
                        neighbors.append((x + TURN_RADIUS, y - TURN_RADIUS*3, md))

                if direction == Direction.NORTH and md == Direction.WEST:
                    if self.grid.reachable(x - TURN_RADIUS*3, y + TURN_RADIUS):
                        neighbors.append((x - TURN_RADIUS*3, y + TURN_RADIUS, md))
                    if self.grid.reachable(x + TURN_RADIUS*3, y - TURN_RADIUS):
                        neighbors.append((x + TURN_RADIUS*3, y - TURN_RADIUS, md))

        return neighbors

    def path_cost_generator(self, states: [CellState]):

        def record_path(start, end, parent: dict, cost: int):
            self.cost_table[(start, end)] = cost
            self.cost_table[(end, start)] = cost

            path = []
            cursor = (end.x, end.y, end.direction)

            while cursor in parent:
                path.append(cursor)
                cursor = parent[cursor]

            path.append(cursor)

            self.path_table[(start, end)] = path[::-1]
            self.path_table[(end, start)] = path

        def astar_search(start: CellState, end: CellState):
            # astar search algo with three states: x, y, direction
            if (start, end) in self.path_table:
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

                for next_x, next_y, new_direction in self.get_neighbors(cur_x, cur_y, cur_direction):
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


class FastCarSolver:
    def __init__(self, size_x: int, size_y: int, robot_x: int, robot_y: int, goal_x: int, goal_y: int):
        self.grid = GridFastestCar(size_x, size_y, robot_x, robot_y, goal_x, goal_y)

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

    def get_neighbors(self, x, y, direction):  # TODO: see the behavior of the robot and adjust...
        """
        Return a list of tuples with format:
        newX, newY, new_direction
        """
        neighbors = []
        # assume that after follow this direction, the car direction is EXACTLY md
        for dx, dy, md in MOVE_DIRECTION:
            if md == direction:  # if the new direction == md
                if self.grid.reachable(x + dx, y + dy):  # go forward;
                    neighbors.append((x + dx, y + dy, md))
                if self.grid.reachable(x - dx, y - dy):  # go back;
                    neighbors.append((x - dx, y - dy, md))

            else:  # consider 8 case
                # north <-> east
                if direction == Direction.NORTH and md == Direction.EAST:
                    if self.grid.reachable(x + TURN_RADIUS*3, y + TURN_RADIUS):
                        neighbors.append((x + TURN_RADIUS*3, y + TURN_RADIUS, md))
                    if self.grid.reachable(x - TURN_RADIUS*3, y - TURN_RADIUS):
                        neighbors.append((x - TURN_RADIUS*3, y - TURN_RADIUS, md))

                if direction == Direction.EAST and md == Direction.NORTH:
                    if self.grid.reachable(x + TURN_RADIUS, y + TURN_RADIUS*3):
                        neighbors.append((x + TURN_RADIUS, y + TURN_RADIUS*3, md))
                    if self.grid.reachable(x - TURN_RADIUS, y - TURN_RADIUS*3):
                        neighbors.append((x - TURN_RADIUS, y - TURN_RADIUS*3, md))

                # east <-> south
                if direction == Direction.EAST and md == Direction.SOUTH:
                    if self.grid.reachable(x + TURN_RADIUS, y - TURN_RADIUS*3):
                        neighbors.append((x + TURN_RADIUS, y - TURN_RADIUS*3, md))
                    if self.grid.reachable(x - TURN_RADIUS, y + TURN_RADIUS*3):
                        neighbors.append((x - TURN_RADIUS, y + TURN_RADIUS*3, md))

                if direction == Direction.SOUTH and md == Direction.EAST:
                    if self.grid.reachable(x + TURN_RADIUS*3, y - TURN_RADIUS):
                        neighbors.append((x + TURN_RADIUS*3, y - TURN_RADIUS, md))
                    if self.grid.reachable(x - TURN_RADIUS*3, y + TURN_RADIUS):
                        neighbors.append((x - TURN_RADIUS*3, y + TURN_RADIUS, md))

                # south <-> west
                if direction == Direction.SOUTH and md == Direction.WEST:
                    if self.grid.reachable(x - TURN_RADIUS*3, y - TURN_RADIUS):
                        neighbors.append((x - TURN_RADIUS*3, y - TURN_RADIUS, md))
                    if self.grid.reachable(x + TURN_RADIUS*3, y + TURN_RADIUS):
                        neighbors.append((x + TURN_RADIUS*3, y + TURN_RADIUS, md))

                if direction == Direction.WEST and md == Direction.SOUTH:
                    if self.grid.reachable(x - TURN_RADIUS, y - TURN_RADIUS*3):
                        neighbors.append((x - TURN_RADIUS, y - TURN_RADIUS*3, md))
                    if self.grid.reachable(x + TURN_RADIUS, y + TURN_RADIUS*3):
                        neighbors.append((x + TURN_RADIUS, y + TURN_RADIUS*3, md))

                # west <-> north
                if direction == Direction.WEST and md == Direction.NORTH:
                    if self.grid.reachable(x - TURN_RADIUS, y + TURN_RADIUS*3):
                        neighbors.append((x - TURN_RADIUS, y + TURN_RADIUS*3, md))
                    if self.grid.reachable(x + TURN_RADIUS, y - TURN_RADIUS*3):
                        neighbors.append((x + TURN_RADIUS, y - TURN_RADIUS*3, md))

                if direction == Direction.NORTH and md == Direction.WEST:
                    if self.grid.reachable(x - TURN_RADIUS*3, y + TURN_RADIUS):
                        neighbors.append((x - TURN_RADIUS*3, y + TURN_RADIUS, md))
                    if self.grid.reachable(x + TURN_RADIUS*3, y - TURN_RADIUS):
                        neighbors.append((x + TURN_RADIUS*3, y - TURN_RADIUS, md))

        return neighbors

    def get_path(self):
        full_path = []
        cache = dict()
        cache_dist = dict()

        def record_path(start, end, parent: dict, distance):
            path = []
            cursor = (end.x, end.y, end.direction)

            while cursor in parent:
                path.append(cursor)
                cursor = parent[cursor]

            for i in reversed(path):
                full_path.append(CellState(i[0], i[1], i[2]))

            key = (start.x, start.y, start.direction, end.x, end.y, end.direction)
            cache[key] = path
            cache_dist[key] = distance

        def astar_search(start: CellState, end: CellState):
            key = (start.x, start.y, start.direction, end.x, end.y, end.direction)
            if key in cache:
                path = cache[key]

                for i in reversed(path):
                    full_path.append(CellState(i[0], i[1], i[2]))

                return cache_dist[key]

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
                    return g_distance[(cur_x, cur_y, cur_direction)]

                visited.add((cur_x, cur_y, cur_direction))
                cur_distance = g_distance[(cur_x, cur_y, cur_direction)]

                for next_x, next_y, new_direction in self.get_neighbors(cur_x, cur_y, cur_direction):
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

            return -1

        result = []
        best_distance = 10000
        for view_states in self.grid.get_possible_path_options():
            full_path = [view_states[0]]
            exist_path = True
            d = 0
            for i in range(len(view_states) - 1):
                d += astar_search(view_states[i], view_states[i + 1])
                if d == -1:
                    exist_path = False
                    break

            if exist_path and best_distance > d:
                result = full_path
                best_distance = d

        return result

if __name__ == "__main__":
    pass
