import BaseAPI, {methodType} from "./BaseAPI";

export default class QueryAPI extends BaseAPI {
	public static query(obstacles: any[], callback: any) {
		const content = {
			"obstacles": obstacles
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
}
