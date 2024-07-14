<script lang="ts">
    import * as Table from "$lib/components/ui/table";
    import type { CellDataInterface } from "$lib/types";

    export let cell: CellDataInterface;
</script>

{#if cell.output}
    {#if cell.output.status === "success"}
        <Table.Root>
            <Table.Caption>
                <p>{cell.output.status_message}</p>
            </Table.Caption>
            <Table.Header> <!-- row id -->
                <Table.Row> 
                    <Table.Head /> 
                    {#each cell.output.columns as column (column)}
                        <Table.Head>{column}</Table.Head>
                    {/each}
                </Table.Row>
            </Table.Header>
            <Table.Body>
                {#each cell.output.results as row, rowId}
                    <Table.Row>
                        <Table.Cell class="font-mono">{rowId + 1}</Table.Cell>
                        {#each row as value}
                            <Table.Cell>{value}</Table.Cell>
                        {/each}
                    </Table.Row>
                {/each}
            </Table.Body>
        </Table.Root>
    {:else}
        <h3 class="font-semibold text-xl my-2 text-red-300">Error</h3>
        <span class="font-mono text-sm">{cell.output.error_message}</span>
    {/if}
{:else}
    <h4 class="text-lg font-semibold text-center">No output</h4>
{/if}
