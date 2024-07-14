<script lang="ts">
    import { setContext } from "svelte";
    import type { HTMLAttributes } from "svelte/elements";

    export let name: string;

    interface $$Props extends HTMLAttributes<HTMLDivElement> {
        name: string;
    };

    setContext("fieldData", { name });
</script>

<div {...$$restProps}>
    <slot />
</div>
