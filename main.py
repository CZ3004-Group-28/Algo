import time
import numpy as np
import pandas as pd

from consts import Direction
from algo.algo import MazeSolver


if __name__ == '__main__':
    maze_solver = MazeSolver(20, 20, 1, 1, Direction.NORTH)
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

    viz = [["0" for i in range(20)] for j in range(20)]
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
        if viz[o.x][o.y] == "0":
            viz[o.x][o.y] = str(counter)
        else:
            viz[o.x][o.y] += ",{}".format(counter)
        counter += 1

    df = pd.DataFrame(np.rot90(viz, 1))
    df.to_csv('test.csv')
