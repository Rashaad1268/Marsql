<script lang="ts">
	import { fetchApi } from '$lib/api';
	import * as Card from '$lib/components/ui/card';
	import * as Table from '$lib/components/ui/table';
	import * as Tabs from '$lib/components/ui/tabs';
	import { Textarea } from '$lib/components/ui/textarea';

	import type { CellDataInterface } from '$lib/types';

	export let data: CellDataInterface;

	async function runQuery() {
		data.timesRun++;

		if (!data.query.trim()) {
			return;
		}

		const response = await fetchApi('/query', {
			method: 'POST',
			body: JSON.stringify({ query: data.query })
		});

		if (response.ok) {
			data.output = await response.json();
		}
	}
</script>

<Card.Root class="max-w-xl w-full">
	<Card.Header class="px-4">
		<div class="flex gap-2">
			<div class="flex flex-col items-center justify-center gap-[2px]">
				<button
					class="flex items-center justify-center size-8 rounded-full p-2 bg-foreground mt-1"
					on:click={runQuery}
				>
					<svg xmlns="http://www.w3.org/2000/svg" class="fill-background" viewBox="0 0 384 512"
						><!--!Font Awesome Free 6.5.2 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license/free Copyright 2024 Fonticons, Inc.--><path
							d="M73 39c-14.8-9.1-33.4-9.4-48.5-.9S0 62.6 0 80V432c0 17.4 9.4 33.4 24.5 41.9s33.7 8.1 48.5-.9L361 297c14.3-8.7 23-24.2 23-41s-8.7-32.2-23-41L73 39z"
						/></svg
					>
				</button>
				<span>{data.timesRun}</span>
			</div>

			<Textarea class="w-full font-mono mb-1" bind:value={data.query} />
		</div>
	</Card.Header>
	<Card.Content class="px-4">
		<Tabs.Root value="query_output" class="w-full">
			<Tabs.List class="justify-between w-full [&>button]:flex-grow">
				<Tabs.Trigger value="query_output">Output</Tabs.Trigger>
				<Tabs.Trigger value="graph">Graph</Tabs.Trigger>
			</Tabs.List>
			<Tabs.Content value="query_output">
				{#if data.output}
					<Table.Root>
						<Table.Caption>
							<p>{data.output.status_message}</p>
							<p>{data.output.rows_affected} rows affected</p>
						</Table.Caption>
						<Table.Header>
							<Table.Row>
								{#each data.output.columns as column}
									<Table.Head>{column}</Table.Head>
								{/each}
							</Table.Row>
						</Table.Header>
						<Table.Body>
							{#each data.output.results as row}
								<Table.Row>
									{#each row as value}
										<Table.Cell>{value}</Table.Cell>
									{/each}
								</Table.Row>
							{/each}
						</Table.Body>
					</Table.Root>
				{:else}
					<h4 class="text-lg font-semibold text-center">No output</h4>
				{/if}
			</Tabs.Content>
			<Tabs.Content value="graph">todo: implement graph</Tabs.Content>
		</Tabs.Root>
	</Card.Content>
</Card.Root>
