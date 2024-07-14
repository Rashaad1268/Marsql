<script lang="ts">
    import NotebookCard from "./notebookCard.svelte";

    import { myNotebooks, userData } from "$lib/stores";
    import { Button } from "$lib/components/ui/button";
    import NotebookCreateButton from "./notebookCreateButton.svelte";
</script>

<svelte:head>
    <title>Notebooks</title>
</svelte:head>

{#if $userData}
    <div class="pt-16 px-16">
        {#if $myNotebooks.length < 1}
            <h1 class="text-4xl font-medium mb-4">You don't have any notebooks</h1>
        {/if}

       <NotebookCreateButton />

        {#if $myNotebooks.length > 0}
            <div class="notebook-grid">
                {#each $myNotebooks as notebook (notebook.id)}
                    <NotebookCard {notebook} />
                {/each}
            </div>
        {/if}
    </div>
{/if}

<style lang="postcss">
    .notebook-grid {
        @apply grid gap-6;
        grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
    }
</style>
