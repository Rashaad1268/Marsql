<script lang="ts">
    import * as Resizable from "$lib/components/ui/resizable/index.js";
    import * as Collapsible from "$lib/components/ui/collapsible";
    import { Button } from "$lib/components/ui/button";

    import type { LayoutData } from "./$types";
    import { invalidate, invalidateAll } from "$app/navigation";
    import { fetchApi } from "$lib/api";
    import { noteBookCells } from "$lib/stores";

    export let data: LayoutData;

    function reFetchData() {
        invalidate(`/api/notebooks/${data.notebook.id}/`);
    }

    async function handleCellCreate() {
        const response = await fetchApi(`notebooks/${data.notebook.id}/cells/`, {
            method: "POST",
            body: JSON.stringify({ type: 1, content: "" })
        });

        if (response.ok) {
            const newCellData = await response.json();

            noteBookCells.update((cells) => [...cells, newCellData]);
        }
    }
</script>

<div class="flex min-w-screen h-full">
    <Resizable.PaneGroup direction="horizontal">
        <Resizable.Pane defaultSize={22} minSize={5} maxSize={50}>
            <aside class="p-6 overflow-y-auto h-full max-h-full">
                <div class="flex items-center mb-4">
                    <a href="/notebook/{data.notebook.id}"
                        ><h1 class="text-xl font-semibold">{data.notebook.name}</h1></a
                    >

                    <Button
                        class="ml-auto group"
                        variant="outline"
                        size="icon"
                        on:click={reFetchData}
                    >
                        <svg
                            xmlns="http://www.w3.org/2000/svg"
                            class="fill-current size-4 group-hover:transition-transform
								   group-hover:duration-700 group-hover:rotate-[360deg]"
                            viewBox="0 0 512 512"
                            ><!--!Font Awesome Free 6.5.2 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license/free Copyright 2024 Fonticons, Inc.--><path
                                d="M463.5 224H472c13.3 0 24-10.7 24-24V72c0-9.7-5.8-18.5-14.8-22.2s-19.3-1.7-26.2 5.2L413.4 96.6c-87.6-86.5-228.7-86.2-315.8 1c-87.5 87.5-87.5 229.3 0 316.8s229.3 87.5 316.8 0c12.5-12.5 12.5-32.8 0-45.3s-32.8-12.5-45.3 0c-62.5 62.5-163.8 62.5-226.3 0s-62.5-163.8 0-226.3c62.2-62.2 162.7-62.5 225.3-1L327 183c-6.9 6.9-8.9 17.2-5.2 26.2s12.5 14.8 22.2 14.8H463.5z"
                            /></svg
                        >
                    </Button>
                </div>

                <div class="flex flex-row gap-2 flex-wrap">
                    <Button class="w-min" size="sm" variant="outline" on:click={handleCellCreate}>
                        <svg
                            xmlns="http://www.w3.org/2000/svg"
                            class="fill-current size-4 mr-2"
                            viewBox="0 0 448 512"
                            ><!--!Font Awesome Free 6.5.2 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license/free Copyright 2024 Fonticons, Inc.--><path
                                d="M256 80c0-17.7-14.3-32-32-32s-32 14.3-32 32V224H48c-17.7 0-32 14.3-32 32s14.3 32 32 32H192V432c0 17.7 14.3 32 32 32s32-14.3 32-32V288H400c17.7 0 32-14.3 32-32s-14.3-32-32-32H256V80z"
                            /></svg
                        >
                        Create Cell
                    </Button>

                    <Button
                        class="w-min"
                        size="sm"
                        variant="outline"
                        href="/notebook/{data.notebook.id}/chat"
                    >
                        <svg
                            xmlns="http://www.w3.org/2000/svg"
                            class="fill-current size-4 mr-2"
                            viewBox="0 0 512 512"
                            ><!--!Font Awesome Free 6.5.2 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license/free Copyright 2024 Fonticons, Inc.--><path
                                d="M64 0C28.7 0 0 28.7 0 64V352c0 35.3 28.7 64 64 64h96v80c0 6.1 3.4 11.6 8.8 14.3s11.9 2.1 16.8-1.5L309.3 416H448c35.3 0 64-28.7 64-64V64c0-35.3-28.7-64-64-64H64z"
                            /></svg
                        >
                        View Chat
                    </Button>
                </div>

                <Collapsible.Root>
                    <Collapsible.Trigger class="text-left">
                        <h2 class="mt-6 font-semibold text-xl">Schema</h2>
                        <h3 class="mt-1 mb-2 font-medium text-lg">
                            Tables ({Object.keys(data.db_schema).length})
                        </h3>
                    </Collapsible.Trigger>

                    <Collapsible.Content>
                        <div class="ml-2 flex flex-col gap-2">
                            {#each Object.entries(data.db_schema) as [tableName, columns] (tableName)}
                                <Collapsible.Root>
                                    <Collapsible.Trigger>
                                        <div
                                            class="font-mono text-sm text-left overflow-hidden whitespace-nowrap overflow-ellipsis"
                                        >
                                            {tableName} ({columns.length})
                                        </div>
                                    </Collapsible.Trigger>

                                    <Collapsible.Content class="ml-4 font-mono">
                                        {#each columns as col (col)}
                                            <div
                                                class="overflow-hidden whitespace-nowrap overflow-ellipsis"
                                            >
                                                {col.name}{col.is_nullable ? "?" : ""}:
                                                <span class="text-sky-600 text-right"
                                                    >{col.data_type}</span
                                                >
                                            </div>
                                        {/each}
                                    </Collapsible.Content>
                                </Collapsible.Root>
                            {/each}
                        </div>
                    </Collapsible.Content>
                </Collapsible.Root>
            </aside>
        </Resizable.Pane>

        <Resizable.Handle />

        <Resizable.Pane class="!overflow-auto">
            <div class="px-6 pt-6">
                <slot />
            </div>
        </Resizable.Pane>
    </Resizable.PaneGroup>
</div>
