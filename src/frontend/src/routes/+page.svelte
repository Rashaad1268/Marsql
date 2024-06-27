<script lang="ts">
	import NotebookCard from './notebookCard.svelte';

	import { userData, myNotebooks } from '$lib/stores';
	import { Button } from '$lib/components/ui/button';
</script>

<svelte:head>
	<title>Your Notebooks</title>
</svelte:head>

<div class="pt-16 px-16">
	{#if $myNotebooks.length > 0}
		<div class="flex items-center gap-3 mb-6">
			<svg xmlns="http://www.w3.org/2000/svg" class="size-7 fill-current" viewBox="0 0 448 512"
				><!--!Font Awesome Free 6.5.2 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license/free Copyright 2024 Fonticons, Inc.--><path
					d="M96 0C43 0 0 43 0 96V416c0 53 43 96 96 96H384h32c17.7 0 32-14.3 32-32s-14.3-32-32-32V384c17.7 0 32-14.3 32-32V32c0-17.7-14.3-32-32-32H384 96zm0 384H352v64H96c-17.7 0-32-14.3-32-32s14.3-32 32-32zm32-240c0-8.8 7.2-16 16-16H336c8.8 0 16 7.2 16 16s-7.2 16-16 16H144c-8.8 0-16-7.2-16-16zm16 48H336c8.8 0 16 7.2 16 16s-7.2 16-16 16H144c-8.8 0-16-7.2-16-16s7.2-16 16-16z"
				/></svg
			>
			<h1 class="font-medium text-4xl">Your notebooks</h1>
		</div>

		<div class="notebook-grid">
			{#each $myNotebooks as notebook}
				<NotebookCard {notebook} />
			{/each}
		</div>
	{:else}
		<h1 class="text-4xl font-medium">You don't have any notebooks</h1>
	{/if}
</div>

<style lang="postcss">
	.notebook-grid {
		@apply grid gap-6;
		grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
	}
</style>
