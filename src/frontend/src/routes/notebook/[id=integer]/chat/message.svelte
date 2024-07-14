<script lang="ts">
    import { MessageAuthorTypes, type ChatMessageInterface } from "$lib/types";
    import Cell from "../cell/cell.svelte";

    import sanitizeHtml from "sanitize-html";
    import { marked } from "marked";

    export let message: ChatMessageInterface;
</script>

<div class="message" class:user-msg={message.author_type === 1} class:sending={!message.created_at}>
    <div class="content">{@html marked(sanitizeHtml(message.content))}</div>

    {#if message.cell && message.author_type === 2}
        <div class="mt-2 max-w-2xl">
            <Cell bind:cell={message.cell} isMessageCell={true} />
        </div>
    {/if}

    {#if !message.created_at}
        <span class="text-gray-500 text-xs">sending...</span>
    {/if}
</div>

<style lang="scss">
    .message {
        @apply my-2;

        .content {
            @apply max-w-lg w-full;
        }

        &.user-msg {
            @apply ml-auto bg-muted py-3 px-4 rounded-lg my-0;

            .content {
                @apply text-base;
            }
        }

        &.sending {
            @apply bg-neutral-700;
            .content {
                @apply text-neutral-400;
            }
        }
    }
</style>
