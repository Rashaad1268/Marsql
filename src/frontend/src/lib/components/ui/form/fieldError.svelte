<script lang="ts">
    import { getContext } from "svelte";
    import { slide } from "svelte/transition";
    import type { FormErrorInterface, FormFieldInterface } from ".";
    import type { Writable } from "svelte/store";
    import type { HTMLAttributes } from "svelte/elements";

    $: formErrors = getContext("formErrors") as Writable<FormErrorInterface>;

    $: fieldName = (getContext("fieldData") as FormFieldInterface).name;
    $: errorMessages = $formErrors[fieldName];

    export let errorStyle: string = "";

    interface $$Props extends HTMLAttributes<HTMLDivElement> {
        errorStyle?: string;
    }
</script>

<div {...$$restProps} class="flex flex-col gap-2 {$$restProps.class || ''}">
    {#each errorMessages || [] as errorMsg (errorMsg)}
        <div
            class="flex gap-2 shadow-lg text-red-500 first-of-type:mt-2 last-of-type:mb-2
                   text-sm w-full {errorStyle ?? ''}"
            in:slide
        >
            {errorMsg}
        </div>
    {/each}
</div>
