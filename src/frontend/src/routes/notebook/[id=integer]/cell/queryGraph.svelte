<script lang="ts">
    import { Bar } from "svelte-chartjs";
    import { Pie } from "svelte-chartjs";
    import {
        Chart,
        Title,
        Tooltip,
        Legend,
        BarElement,
        CategoryScale,
        LinearScale,
        ArcElement
    } from "chart.js";

    import type { CellDataInterface } from "$lib/types";

    const generateData = () => {
        return {
            labels: cell.output?.results.map((r) => r[0]),
            datasets: [
                {
                    label: cell.output!.columns[1],
                    data: cell.output!.results.map((r) => r[1]),
                    backgroundColor: [
                        "rgba(255, 134,159,0.4)",
                        "rgba(98,  182, 239,0.4)",
                        "rgba(255, 218, 128,0.4)"
                    ],
                    borderWidth: 2,
                    borderColor: [
                        "rgba(255, 134, 159, 1)",
                        "rgba(98,  182, 239, 1)",
                        "rgba(255, 218, 128, 1)"
                    ]
                }
            ]
        };
    };

    export let cell: CellDataInterface;
    Chart.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale, ArcElement);
</script>

{#if cell.output}
    {#key cell.output?.results}
        <Bar  data={generateData()} options={{ responsive: true }} />
    {/key}
{:else}
    <p>No output</p>
{/if}