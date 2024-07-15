<script lang="ts">
    import { highlighter } from "$lib/highlighter";
    import * as Card from "$lib/components/ui/card";
    import * as Tabs from "$lib/components/ui/tabs";
    import { Textarea } from "$lib/components/ui/textarea";
    import * as Tooltip from "$lib/components/ui/tooltip";
    import * as Select from "$lib/components/ui/select/index.js";
    import { Checkbox } from "$lib/components/ui/checkbox";

    import type { CellDataInterface } from "$lib/types";
    import { cellTypeChoices } from "$lib/utils";
    import { Button } from "$lib/components/ui/button";
    import { onMount } from "svelte";
    import QueryOutput from "./queryOutput.svelte";
    import QueryGraph from "./queryGraph.svelte";

    export let cell: CellDataInterface;
    export let isMessageCell: boolean;
    export let doCommitQuery: boolean;
    export let runQuery: () => void;
    export let handleCellUpdate: (e: Event) => void;
    export let currentCellType: (typeof cellTypeChoices)[0];
    export let updateCellType: (value: any) => void;
    export let deleteCell: () => void;

    onMount(() => {
        if (isMessageCell && !cell.output) {
            runQuery();
        }
    });
</script>

<Card.Root class="w-full">
    <Card.Header class="px-4">
        <div class="flex flex-col gap-2">
            <div class="flex gap-2">
                <div class="flex flex-col items-center justify-center gap-[2px]">
                    <Button
                        class="flex items-center justify-center size-8 rounded-full p-2 mt-1"
                        on:click={runQuery}
                    >
                        <svg
                            xmlns="http://www.w3.org/2000/svg"
                            class="fill-background"
                            viewBox="0 0 384 512"
                            ><!--!Font Awesome Free 6.5.2 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license/free Copyright 2024 Fonticons, Inc.--><path
                                d="M73 39c-14.8-9.1-33.4-9.4-48.5-.9S0 62.6 0 80V432c0 17.4 9.4 33.4 24.5 41.9s33.7 8.1 48.5-.9L361 297c14.3-8.7 23-24.2 23-41s-8.7-32.2-23-41L73 39z"
                            />
                        </svg>
                    </Button>
                    <span>{cell.timesRun ?? 0}</span>
                </div>

                <div
                    contenteditable={!isMessageCell}
                    class="max-w-full w-full mb-1 !bg-transparent focus:outline-0 [&>pre]:!bg-transparent
                           !whitespace-break-word overflow-auto"
                    on:input={(e) => {
                        if (!isMessageCell && e.isTrusted) {
                            cell.content = e.target.textContent;
                            handleCellUpdate(e);
                        }
                    }}
                >
                    {@html highlighter.codeToHtml(cell.content, {
                        lang: "sql",
                        theme: "material-theme-ocean"
                    })}
                </div>
            </div>

            <div class="flex items-center">
                <Button
                    disabled={isMessageCell}
                    size="icon"
                    variant="outline"
                    class="mr-4"
                    on:click={deleteCell}
                >
                    <svg
                        xmlns="http://www.w3.org/2000/svg"
                        class="size-4 fill-red-600"
                        viewBox="0 0 448 512"
                        ><!--!Font Awesome Free 6.5.2 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license/free Copyright 2024 Fonticons, Inc.--><path
                            d="M135.2 17.7C140.6 6.8 151.7 0 163.8 0H284.2c12.1 0 23.2 6.8 28.6 17.7L320 32h96c17.7 0 32 14.3 32 32s-14.3 32-32 32H32C14.3 96 0 81.7 0 64S14.3 32 32 32h96l7.2-14.3zM32 128H416V448c0 35.3-28.7 64-64 64H96c-35.3 0-64-28.7-64-64V128zm96 64c-8.8 0-16 7.2-16 16V432c0 8.8 7.2 16 16 16s16-7.2 16-16V208c0-8.8-7.2-16-16-16zm96 0c-8.8 0-16 7.2-16 16V432c0 8.8 7.2 16 16 16s16-7.2 16-16V208c0-8.8-7.2-16-16-16zm96 0c-8.8 0-16 7.2-16 16V432c0 8.8 7.2 16 16 16s16-7.2 16-16V208c0-8.8-7.2-16-16-16z"
                        /></svg
                    >
                </Button>

                <Select.Root
                    bind:selected={currentCellType}
                    disabled={isMessageCell}
                    onSelectedChange={updateCellType}
                >
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

                <Tooltip.Root>
                    <Tooltip.Trigger>
                        <div class="flex items-center space-x-4 ml-8">
                            <label
                                id="do_commit_label"
                                for="do_commit"
                                class="text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70"
                            >
                                Commit transaction
                            </label>
                            <Checkbox
                                id="do_commit"
                                bind:checked={doCommitQuery}
                                aria-labelledby="commit query?"
                            />
                        </div></Tooltip.Trigger
                    >
                    <Tooltip.Content>
                        <p>Whether to commit the transaction</p>
                    </Tooltip.Content>
                </Tooltip.Root>
            </div>
        </div>
    </Card.Header>

    <Card.Content class="px-4">
        <Tabs.Root value="query_output" class="w-full">
            <Tabs.List class="justify-between w-full [&>button]:flex-grow">
                <Tabs.Trigger value="query_output">Output</Tabs.Trigger>
                <Tabs.Trigger value="graph">Graph</Tabs.Trigger>
            </Tabs.List>
            <Tabs.Content value="query_output">
                <QueryOutput {cell} />
            </Tabs.Content>

            <Tabs.Content value="graph">
                <QueryGraph {cell} />
            </Tabs.Content>
        </Tabs.Root>
    </Card.Content>
</Card.Root>
