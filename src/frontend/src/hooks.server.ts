import type { Handle } from "@sveltejs/kit";

export const handle: Handle = async ({ event, resolve }) => {
    const urlEndpoint = event.url.pathname.slice();
    const authEndpoints = ["auth/", "/auth/login", "/auth/signup", "/welcome"];

    const isLoggedIn = !!event.cookies.get("sessionid"); // Check if the sessionid cookie exists

    if (isLoggedIn) {
        // If the user is logged in and he visits the authentication pages
        if (authEndpoints.includes(urlEndpoint)) {
            // redirect the user to the home page
            event.url = new URL(event.url.origin);
            return Response.redirect(event.url);
        }
    } else {
        // If the user is not logged in and visits any other pages than the auth pages
        if (!authEndpoints.includes(urlEndpoint)) {
            // redirect him to the welcome page
            event.url = new URL(`${event.url.origin}/auth/login?next=${event.url.pathname}`);

            return Response.redirect(event.url);
        }
    }

    return await resolve(event);
};
 