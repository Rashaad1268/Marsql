<script>
    import { Button } from "../button";
    import FormMessages from "./formMessages.svelte";
</script>

<div class="mt-2 w-full">
    <FormMessages />
    <Button class="mt-2 w-full" aria-label="login button" type="submit"><slot /></Button>
</div>
