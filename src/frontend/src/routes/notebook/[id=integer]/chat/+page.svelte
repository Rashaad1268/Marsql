<script lang="ts">
    import { fetchApi } from "$lib/api";
    import type { ChatMessageInterface } from "$lib/types";
    import { onMount } from "svelte";
    import type { PageData } from "./$types";
    import Message from "./message.svelte";
    import { Input } from "$lib/components/ui/input";

    export let data: PageData;
    let messages: ChatMessageInterface[] = [];

    onMount(async () => {
        const response = await fetchApi(`notebooks/${data.notebook.id}/messages/`);

        if (response.ok) {
            messages = await response.json();
        }
    });
</script>

<div class="flex flex-col max-h-full">
    <div class="flex flex-col gap-1 pt-6 p-2 h-full overflow-y-auto pl-10">
        {#each messages as message (message.id)}
            <Message bind:message />
        {/each}
    </div>

    <form class="px-10">
        <Input class="" />
    </form>
</div>
