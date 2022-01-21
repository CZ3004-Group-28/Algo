import heapq
import math
import numpy as np
from random import randint
from entities.Robot import Robot
from entities.Entity import Obstacle, CellState, Grid
from consts import Direction, MOVE_DIRECTION, TURN_FACTOR, ITERATIONS
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

    def get_optimal_order_dp(self) -> [CellState]:
        # calculate optimal_cost table
        items = [self.robot.get_start_state()]
        # all possible positions to be able to view the obstacles
        view_positions = self.grid.get_view_obstacle_positions()

        for view_position in view_positions:
            items = items + view_position

        cost_table, path_table = self.path_cost_generator(items)

        optimal_path = []
        distance = 1e9

        for _ in range(ITERATIONS): # run the algo some times ->
            visited_candidates = [0] # add the start state of the robot

            cur_index = 1
            for view_position in view_positions:
                visited_candidates.append(cur_index + randint(0, len(view_position) - 1))
                cur_index += len(view_position)

            cost_np = np.zeros((len(visited_candidates), len(visited_candidates)))
            print(visited_candidates)

            for s in range(len(visited_candidates) - 1):
                for e in range(s + 1, len(visited_candidates)):
                    u = items[visited_candidates[s]]
                    v = items[visited_candidates[e]]
                    if (u, v) in cost_table.keys():
                        cost_np[s][e] = cost_table[(u, v)]
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


if __name__ == "__main__":
    pass
