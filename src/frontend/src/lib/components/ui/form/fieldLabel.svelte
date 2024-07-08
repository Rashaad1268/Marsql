<script lang="ts">
    import type { HTMLLabelAttributes } from "svelte/elements";

    type $$Props = HTMLLabelAttributes;
</script>

<label
    {...$$restProps}
    class="text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70 data-[fs-error]:text-destructive"
    ><slot /></label
>
