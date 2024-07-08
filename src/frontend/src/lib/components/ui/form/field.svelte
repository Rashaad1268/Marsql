<script lang="ts">
    import { setContext } from "svelte";

    export let name: string;

    setContext("fieldData", { name });
</script>

<div>
    <slot />
</div>
