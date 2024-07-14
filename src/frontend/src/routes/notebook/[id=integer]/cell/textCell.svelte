<script lang="ts">
    import { fetchApi } from "$lib/api";
    import * as Card from "$lib/components/ui/card";
    import * as Table from "$lib/components/ui/table";
    import * as Tabs from "$lib/components/ui/tabs";
    import { Textarea } from "$lib/components/ui/textarea";
    import * as Tooltip from "$lib/components/ui/tooltip";
    import * as Select from "$lib/components/ui/select/index.js";
    import { Checkbox } from "$lib/components/ui/checkbox";

    import sanitizeHtml from "sanitize-html";
    import { marked } from "marked";

    import type { CellDataInterface } from "$lib/types";
    import { cellTypeChoices } from "$lib/utils";
    import { noteBookCells } from "$lib/stores";
    import { Button } from "$lib/components/ui/button";
    import { toast } from "svelte-sonner";

    export let cell: CellDataInterface;
    export let handleCellUpdate: (e: Event) => void;
    export let currentCellType: (typeof cellTypeChoices)[0];
    export let updateCellType: (value: any) => void;
    export let deleteCell: () => void;

    let isEditingCell = false;
</script>

<Card.Root class="w-full">
    <Card.Header class="px-4 pt-4">
        <div class="flex flex-col gap-2">
            <div>
                {#if isEditingCell}
                    <Textarea
                        on:input={handleCellUpdate}
                        on:focusout={() => (isEditingCell = false)}
                        class="w-full font-mono mb-1"
                        bind:value={cell.content}
                    />
                {:else}
                    <button class="pb-4 text-left w-full" on:click={() => (isEditingCell = true)}>
                        <Card.Root>
                            <Card.Header>
                                <div class="prose prose-invert">
                                    {@html marked(sanitizeHtml(cell.content))}
                                </div>
                            </Card.Header>
                        </Card.Root>
                    </button>
                {/if}
            </div>

            <div class="flex items-center">
                <Button size="icon" variant="outline" class="mr-4" on:click={deleteCell}>
                    <svg
                        xmlns="http://www.w3.org/2000/svg"
                        class="size-4 fill-red-600"
                        viewBox="0 0 448 512"
                        ><!--!Font Awesome Free 6.5.2 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license/free Copyright 2024 Fonticons, Inc.--><path
                            d="M135.2 17.7C140.6 6.8 151.7 0 163.8 0H284.2c12.1 0 23.2 6.8 28.6 17.7L320 32h96c17.7 0 32 14.3 32 32s-14.3 32-32 32H32C14.3 96 0 81.7 0 64S14.3 32 32 32h96l7.2-14.3zM32 128H416V448c0 35.3-28.7 64-64 64H96c-35.3 0-64-28.7-64-64V128zm96 64c-8.8 0-16 7.2-16 16V432c0 8.8 7.2 16 16 16s16-7.2 16-16V208c0-8.8-7.2-16-16-16zm96 0c-8.8 0-16 7.2-16 16V432c0 8.8 7.2 16 16 16s16-7.2 16-16V208c0-8.8-7.2-16-16-16zm96 0c-8.8 0-16 7.2-16 16V432c0 8.8 7.2 16 16 16s16-7.2 16-16V208c0-8.8-7.2-16-16-16z"
                        /></svg
                    >
                </Button>

                <Select.Root bind:selected={currentCellType} onSelectedChange={updateCellType}>
                    <Select.Trigger class="flex-1">
                        <Select.Value placeholder="Cell type" />
                    </Select.Trigger>
                    <Select.Content>
                        <Select.Group>
                            <Select.Label>Cell Types</Select.Label>
                            {#each cellTypeChoices as cellChoice (cellChoice.value)}
                                <Select.Item value={cellChoice.value} label={cellChoice.label}
                                    >{cellChoice.label}</Select.Item
                                >
                            {/each}
                        </Select.Group>
                    </Select.Content>
                    <Select.Input name="favoriteFruit" />
                </Select.Root>
            </div>
        </div>
    </Card.Header>
</Card.Root>
