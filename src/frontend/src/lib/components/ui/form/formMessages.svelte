<script lang="ts">
    import { getContext } from "svelte";
    import type { Writable } from "svelte/store";
    import { slide } from "svelte/transition";

    $: messages = getContext("formMessages") as Writable<string[]>;
</script>

<div class="flex flex-col gap-1">
    {#each $messages as message (message)}
        <p in:slide class="text-red-500">{message}</p>
    {/each}
</div>
