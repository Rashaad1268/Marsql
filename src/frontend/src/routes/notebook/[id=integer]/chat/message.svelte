<script lang="ts">
    import { MessageAuthorTypes, type ChatMessageInterface } from "$lib/types";
    import Cell from "../cell.svelte";

    export let message: ChatMessageInterface;
</script>

<div class="message" class:user-msg={message.author_type === 1}>
    <div class="content">{message.content}</div>

    {#if message.cell && message.author_type === 2}
        <div class="mt-2 max-w-2xl">
            <Cell bind:cell={message.cell} readOnly={true} />
        </div>
    {/if}
</div>

<style lang="scss">
    .message {
        @apply my-2;

        .content {
            @apply max-w-sm w-full;
        }

        &.user-msg {
            @apply ml-auto bg-muted py-5 px-4 rounded-lg my-0;

            .content {
                @apply text-sm;
            }
        }
    }
</style>
