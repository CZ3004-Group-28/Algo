export enum methodType {get = 'GET', post = 'POST', put = 'PUT', delete = 'DELETE'}

export class CustomError extends Error {
	public content: Response;

	constructor(content: Response) {
		super();
		this.content = content
	}

	public msg(s: string) {
		this.message = s;
	}
}

export default class BaseAPI {

	protected static JSONRequest(api: string, method: methodType, headers: Record<string, string>, options: object, content: object) {
		const host = "http://127.0.0.1:5000";

		let requestOptions: any = {
			method: method,
			headers: {...headers, 'Content-Type': 'application/json'},
			...options
		}

		if (method === methodType.post || method === methodType.put) {
			requestOptions.body = JSON.stringify(content)
		}

		return new Promise((resolve, reject) => {
			fetch(host + api, requestOptions)
				.then(response => {
					if (!response.ok) {
						throw new CustomError(response);
					}

					response.json()
						.then(res => {
							if (res.error) {
								reject(JSON.stringify(res.error));
							}
							resolve(res.data);
						})
						.catch(err => {
							resolve({});
						});

				})
				.catch(async (err: Error) => {
					console.log(err)
					if (err instanceof CustomError) {

						// best effort to capture all cases of err handling
						let errStr = await err.content.json()
							.then(res => {
								if (res.errors) {
									return JSON.stringify(res.errors);
								}

								return "";
							}).catch(() => {
								return "";
							});

						err.msg(errStr);
						reject(err);

					} else {
						reject(err);
					}
				})
		})
	}

}
