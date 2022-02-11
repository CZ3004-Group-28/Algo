import time

from consts import Direction
from algo.algo import MazeSolver
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


@app.route('/image', methods=['POST'])
def image_predict():
    # save the image file to the uploads folder
    file = request.files['file']
    filename = file.filename
    file.save(os.path.join('uploads', filename))

    # perform image recognition
    # filename format: "<obstacle_id>_<timestamp>.jpeg"
    obstacle_id = file.filename.split("_")[0]  
    image_id = predict_image(filename, model)

    return jsonify({
        "obstacle_id": obstacle_id,
        "image_id": image_id
    })


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
    commands = command_generator(optimal_path)

    j = 0
    for i in range(len(commands)):
        if commands[i].startswith("SNAP"):
            commands[i] = "SNAP{}".format(get_direction(optimal_path[j].direction))
        else:
            j += 1

    return jsonify({
        "commands": commands
    })


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
