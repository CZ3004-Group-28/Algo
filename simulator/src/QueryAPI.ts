import BaseAPI, {methodType} from "./BaseAPI";

export default class QueryAPI extends BaseAPI {
	public static query(obstacles: any[], big_turn: number, callback: any) {
		const content = {
			"obstacles": obstacles,
			"big_turn": big_turn
		}

		this.JSONRequest('/path', methodType.post, {}, {}, content)
			.then((res: any) => {
				if (callback) {
					callback({
						data: res,
						error: null,
					})
				}
			})
			.catch(err => {
				console.log(err)
				if (callback) {
					callback({
						data: null,
						error: err
					})
				}
			})
	}

	public static fastest(robotX: number, robotY: number, goalX: number, goalY: number, callback: any) {
		const content = {
			"size_x": 20,
			"size_y": 20,
			"robot_x": robotX,
			"robot_y": robotY,
			"goal_x": goalX,
			"goal_y": goalY
		}

		this.JSONRequest('/fastest_car', methodType.post, {}, {}, content)
			.then((res: any) => {
				if (callback) {
					callback({
						data: res,
						error: null,
					})
				}
			})
			.catch(err => {
				console.log(err)
				if (callback) {
					callback({
						data: null,
						error: err
					})
				}
			})
	}
}
