import time

from consts import Direction
from algo.algo import MazeSolver, FastCarSolver
from flask import Flask, request, jsonify
from flask_cors import CORS
from model import *

from helper import command_generator

app = Flask(__name__)
CORS(app)
model = load_model()


@app.route('/path', methods=['POST'])
def path_finding():
    content = request.json

    obstacles = content['obstacles']
    maze_solver = MazeSolver(20, 20, 1, 1, Direction.NORTH)

    for ob in obstacles:
        maze_solver.add_obstacle(ob['x'], ob['y'], ob['d'], ob['id'])

    print("Manual A*")
    start = time.time()
    optimal_path, distance = maze_solver.get_optimal_order_dp()
    print(time.time() - start)
    print(distance)

    path_results = []
    for o in optimal_path:
        path_results.append(o.get_dict())

    return jsonify({
        "data": {
            'distance': distance,
            'path': path_results,
            'commands': command_generator(optimal_path)
        },
        "error": None
    })

@app.route('/fastest_car', methods=['POST'])
def fastest_car():
    content = request.json

    size_x = content['size_x']
    size_y = content['size_y']
    robot_x = content['robot_x']
    robot_y = content['robot_y']
    goal_x = content['goal_x']
    goal_y = content['goal_y']

    solver = FastCarSolver(size_x, size_y, robot_x, robot_y, goal_x, goal_y)

    print("Manual A*")
    start = time.time()
    optimal_path = solver.get_path()
    print(time.time() - start)

    path_results = []
    for o in optimal_path:
        path_results.append(o.get_dict())

    return jsonify({
        "data": {
            'path': path_results,
            'commands': command_generator(optimal_path)
        },
        "error": None
    })

@app.route('/image', methods=['POST'])
def image_predict():
    # save the image file to the uploads folder
    file = request.files['file']
    filename = file.filename
    print(filename)
    file.save(os.path.join('uploads', filename))
    # perform image recognition
    # filename format: "<timestamp>_<obstacle_id>.jpeg"
    obstacle_id = file.filename.split("_")[1].strip(".jpg")
    image_id = predict_image(filename, model)

    result = {
        "obstacle_id": obstacle_id,
        "image_id": image_id
    }

    # only include the "stop" field if the request is for the "navigate around obstacle" feature
    if obstacle_id in ['N', 'S', 'E', 'W']:
        # set stop to True if non-bullseye detected
        result['stop'] = image_id != "10"

    return jsonify(result)


@app.route('/navigate', methods=['POST'])
def navigate():
    def get_direction(d: int) -> str:
        if d == Direction.NORTH:
            return "N"
        if d == Direction.SOUTH:
            return "S"
        if d == Direction.EAST:
            return "E"
        else:
            return "W"

    content = request.json
    obstacle = content["obstacle"]
    robot = content["robot"]

    maze_solver = MazeSolver(20, 20, robot['x'], robot['y'], robot['d'])

    for d in [0, 2, 4, 6]: # NORTH | EAST | SOUTH | WEST
        maze_solver.add_obstacle(obstacle['x'], obstacle['y'], d, 1)

    optimal_path, distance = maze_solver.get_optimal_order_dp()
    _commands = command_generator(optimal_path)
    commands = []

    j = 0
    for i in range(len(_commands)):
        if _commands[i].startswith("SNAP"):
            commands.append("SNAP{}".format(get_direction(optimal_path[j].direction)))
            commands.append("NOOP")# add no-op operation;
        else:
            commands.append(_commands[i])
            j += 1

    path_results = []
    for o in optimal_path:
        path_results.append(o.get_dict())

    # add additional DT20 command infront
    # tells STM32 to move until 20cm is reached
    commands.insert(0, 'DT20')

    # add additional location to path (copied from 1st location)
    path_results.insert(0, path_results[0])
    print(commands)
    print(path_results)
    return jsonify({
        "data": {
            "path": path_results,
            "commands": commands
        }
    })


@app.route('/stitch', methods=['GET'])
def stitch():
    img = stitch_image()
    img.show()
    return jsonify({"result": "ok"})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
