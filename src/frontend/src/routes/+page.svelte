<script lang="ts">
	import { onMount } from 'svelte';
	import { Button } from '$lib/components/ui/button';
	
	import type { CellData } from '$lib/types';
	import Cell from './cell.svelte';

	let cells: CellData[] =  [{ timesRun: 0, query: '' }];

	onMount(() => {
		if (localStorage["cell_data"]) {
			cells = JSON.parse(localStorage["cell_data"])
		}
	})

	function saveCellData() {
		localStorage["cell_data"] = JSON.stringify(cells)
	}
</script>

<svelte:window on:beforeunload={saveCellData} />

<svelte:head>
	<title>Marsql notebook</title>
</svelte:head>

<div class="grid place-items-center mt-6 mb-10">
<Button
	on:click={() => (cells = [...cells, { timesRun: 0, query: '' }])}>Add Cell</Button
></div>


<div class="flex flex-col gap-2 items-center">
	{#each cells as cellData}
		<Cell bind:data={cellData} />
	{/each}
</div>
