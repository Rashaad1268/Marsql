<script lang="ts">
	import '../styles/app.scss';
	import { browser } from '$app/environment';
	import type { LayoutData } from './$types';

	import { Toaster } from "svelte-sonner";
	import NavBar from './navbar.svelte';
	import { userData } from '$lib/stores';
	import { fetchUserData } from '$lib/utils';

	export let data: LayoutData;

	$: {
		if (!browser) {
			break $;
		}

		if (data.isLoggedIn && !$userData) {
			fetchUserData();
		}
	}
</script>

<NavBar />

<main class="h-full">
	<slot />
</main>

<Toaster />
