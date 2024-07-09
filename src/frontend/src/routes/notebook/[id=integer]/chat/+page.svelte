<script lang="ts">
    import { fetchApi } from "$lib/api";
    import {
        MessageAuthorTypes,
        type ChatMessageInterface,
        type PaginatorInterface
    } from "$lib/types";
    import { onMount } from "svelte";
    import type { PageData } from "./$types";
    import Message from "./message.svelte";
    import { Input } from "$lib/components/ui/input";

    export let data: PageData;
    let messages: PaginatorInterface<ChatMessageInterface>;
    let isSendingMessage = false;
    let isFetchingNewMessages = false;

    let newMessage = "";

    onMount(async () => {
        const response = await fetchApi(`notebooks/${data.notebook.id}/messages/`);

        if (response.ok) {
            messages = await response.json();
        }
    });

    function loadMessages(event: Event) {
        if (!messages) {
            return;
        }

        const element = event.target as HTMLDivElement;

        if (element.scrollHeight + element.scrollTop < 750) {
            if (!isFetchingNewMessages && messages.results.length !== messages.count) {
                isFetchingNewMessages = true;
                fetchApi(
                    `notebooks/${data.notebook.id}/messages/?before=${messages.results[messages.results.length - 1].id}`
                ).then((response) => {
                    if (response.ok) {
                        response.json().then((data) => {
                            messages = {
                                ...messages,
                                results: [...messages.results, ...data.results]
                            };
                            isFetchingNewMessages = false;
                        });
                    }
                });
            }
        }
    }

    async function sendMessage() {
        if (!newMessage.trim()) return;

        isSendingMessage = true;
        const lastId = messages.results[0].id || 0;

        messages = {
            ...messages,
            results: [
                ...messages.results,
                {
                    id: lastId + 1,
                    content: newMessage,
                    notebook: data.notebook.id,
                    author_type: MessageAuthorTypes.user,
                    created_at: null,
                    cell: null,
                    attached_file: null,
                    attached_image: null
                }
            ]
        };

        await fetchApi(`notebooks/${data.notebook.id}/messages/`, {
            method: "POST",
            body: JSON.stringify({ content: newMessage })
        });
        newMessage = "";
    }
</script>

<div class="flex flex-col max-h-full">
    <div
        class="flex flex-col-reverse gap-1 pt-6 p-2 h-full overflow-y-auto pl-10"
        on:scroll={loadMessages}
    >
        {#each messages?.results || [] as message (message.id)}
            <Message bind:message />
        {/each}
    </div>

    <form class="px-10" on:submit={sendMessage}>
        <Input class="" bind:value={newMessage} disabled={isSendingMessage} />
    </form>
</div>
