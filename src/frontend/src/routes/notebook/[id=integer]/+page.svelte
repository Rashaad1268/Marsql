<script lang="ts">
    import { onMount } from "svelte";

    import Cell from "./cell.svelte";

    import type { CellDataInterface } from "$lib/types";
    import type { PageData } from "./$types";
    import { fetchApi } from "$lib/api";
    import { noteBookCells } from "$lib/stores";

    export let data: PageData;

    onMount(async () => {
        const response = await fetchApi(`notebooks/${data.notebook.id}/cells/`);

        if (response.ok) {
            const cellsData = await response.json();

            noteBookCells.set(cellsData);
        }
    });
</script>

<svelte:head>
    <title>Marsql notebook</title>
</svelte:head>

<div class="flex flex-col gap-8 items-center mb-32">
    {#each $noteBookCells as cellData (cellData.id)}
        <Cell bind:cell={cellData} />
    {/each}
</div>
