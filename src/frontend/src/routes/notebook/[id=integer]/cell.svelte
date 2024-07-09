<script lang="ts">
    import { fetchApi } from "$lib/api";

    import type { CellDataInterface } from "$lib/types";
    import { cellTypeChoices } from "$lib/utils";
    import { noteBookCells } from "$lib/stores";
    import { toast } from "svelte-sonner";

    import TextCell from "./textCell.svelte";
    import CodeCell from "./codeCell.svelte";

    export let cell: CellDataInterface;
    export let isMessageCell = false;
    cell.timesRun = 0;

    let doCommitQuery = false;

    let cellUpdateTimeout: number;
    let savingToast: string | number | undefined;

    async function runQuery() {
        if (cell.type !== 1) return;

        cell.timesRun!++;

        if (!cell.content.trim()) {
            return;
        }

        const response = await fetchApi(`notebooks/${cell.notebook}/cells/${cell.id}/run/`, {
            method: "POST",
            body: JSON.stringify({ commit: doCommitQuery })
        });

        if (response.ok) {
            cell.output = await response.json();
        }
    }

    function updateCellContent() {
        fetchApi(`notebooks/${cell.notebook}/cells/${cell.id}/`, {
            method: "PATCH",
            body: JSON.stringify({ content: cell.content.trim() })
        }).then((resp) => {
            if (resp.ok) {
                toast.dismiss(savingToast);
                savingToast = undefined;
                toast.success("Saved");
            }
        });
    }

    function handleCellUpdate(e: Event): void {
        if (!e.isTrusted) return; // Not today spammers

        if (savingToast === undefined) {
            savingToast = toast.loading("Saving...", { duration: Number.POSITIVE_INFINITY });
            toast;
        }

        if (cellUpdateTimeout) {
            clearTimeout(cellUpdateTimeout);
        }

        cellUpdateTimeout = setTimeout(updateCellContent, 700);
    }

    $: currentCellType = cellTypeChoices.find((c) => c.value == cell.type)!;

    async function updateCellType(value: any) {
        const selectedValue = value.value as number;

        // if the selected value is the current value, do nothing
        if (selectedValue === cell.type) return;

        const response = await fetchApi(`notebooks/${cell.notebook}/cells/${cell.id}/`, {
            method: "PATCH",
            body: JSON.stringify({ type: selectedValue })
        });

        if (response.ok) {
            cell.type = selectedValue as CellDataInterface["type"];
        }
    }

    async function deleteCell() {
        const response = await fetchApi(`notebooks/${cell.notebook}/cells/${cell.id}/`, {
            method: "DELETE"
        });

        if (response.ok) {
            noteBookCells.update((cells) => cells.filter((c) => c.id !== cell.id));
        }
    }
</script>

{#if cell.type === 1}
    <CodeCell
        bind:cell
        bind:doCommitQuery
        {isMessageCell}
        {runQuery}
        {handleCellUpdate}
        {currentCellType}
        {updateCellType}
        {deleteCell}
    />
{:else}
    <TextCell
        bind:cell
        {handleCellUpdate}
        {currentCellType}
        {updateCellType}
        {deleteCell}
    />
{/if}
