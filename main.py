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
    content = request.json

    obstacle_id = content["obstacle_id"]
    image = content["image"]
    image_id = predict_image(image, model)

    return jsonify({
        "obstacle_id": obstacle_id,
        "image_id": image_id
    })


if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)
