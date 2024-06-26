export const fetchApi = async (endpoint: string, options: RequestInit): Promise<Response> => {
	options.headers = {
		Accept: 'application/json',
		'Content-Type': 'application/json',
		...options.headers
	};
	options.credentials = 'include';

	return await fetch('/api/' + endpoint, options);
};
