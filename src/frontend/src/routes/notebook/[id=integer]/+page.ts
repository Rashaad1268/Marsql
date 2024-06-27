/** @type {import('./$types').PageLoad} */
export async function load({ params, fetch }) {
	return {
		notebook: await (await fetch(`/api/notebooks/${params.id}/`)).json()
	};
}
