<script lang="ts">
    import { fetchApi } from "$lib/api";
    import { Button, buttonVariants } from "$lib/components/ui/button/index.js";
    import * as Dialog from "$lib/components/ui/dialog/index.js";
    import { Field, FormSubmit, FieldErrors, createForm } from "$lib/components/ui/form";
    import FieldLabel from "$lib/components/ui/form/fieldLabel.svelte";
    import { Input } from "$lib/components/ui/input/index.js";
    import * as Select from "$lib/components/ui/select/index.js";
    import { dbTypes } from "$lib/utils";

    const form = createForm();

    let name: string;
    let db_config = {
        db_type: 0,
        db_name: "",
        db_user: "",
        db_password: "",
        db_host: "",
        db_port: ""
    };

    async function createNotebook() {
        form.errors.set({});
        const response = await fetchApi("notebooks/", {
            method: "POST",
            body: JSON.stringify({ name, db_config })
        });

        if (response.ok) {
        } else {
            form.setBackendErrors(await response.json());
        }
    }
</script>

<Dialog.Root>
    <Dialog.Trigger class="{buttonVariants()} mb-8">Create notebook</Dialog.Trigger>
    <Dialog.Content class="sm:max-w-[600px] max-h-[calc(100vh-20px)] my-1 overflow-y-auto">
        <form on:submit|preventDefault={createNotebook}>
            <Dialog.Header>
                <Dialog.Title>Create notebook</Dialog.Title>
                <Dialog.Description>Create a new Marsql notebook</Dialog.Description>
            </Dialog.Header>
            <div class="grid gap-4 py-4">
                <Field name="name" class="grid grid-cols-4 items-center gap-4">
                    <FieldLabel for="name" class="text-right">Name</FieldLabel>
                    <Input id="name" bind:value={name} class="col-span-3" />
                    <FieldErrors errorStyle="!m-0" class="col-span-4" />
                </Field>

                <Dialog.Title class="mt-4 mb-1">Database configuration</Dialog.Title>
                <Field name="db_config.db_type" class="grid grid-cols-4 items-center gap-4">
                    <FieldLabel for="name" class="text-right">DB Type</FieldLabel>
                    <Select.Root
                        required={true}
                        onSelectedChange={(value) => {
                            if (!!value?.value) {
                                db_config.db_type = value?.value;
                            }
                        }}
                    >
                        <Select.Trigger class="col-span-3">
                            <Select.Value placeholder="Database type" />
                        </Select.Trigger>
                        <Select.Content>
                            <Select.Group>
                                <Select.Label>Databases</Select.Label>
                                {#each dbTypes as dbType (dbType.value)}
                                    <Select.Item value={dbType.value} label={dbType.label} />
                                {/each}
                            </Select.Group>
                        </Select.Content>
                        <Select.Input name="favoriteFruit" />
                    </Select.Root><FieldErrors errorStyle="!m-0" class="col-span-4" />
                </Field>

                <Field name="db_config.db_name" class="grid grid-cols-4 items-center gap-4">
                    <FieldLabel for="db_name" class="text-right">DB Name</FieldLabel>
                    <Input
                        id="db_name"
                        bind:value={db_config.db_name}
                        class="col-span-3"
                    /><FieldErrors errorStyle="!m-0" class="col-span-4" />
                </Field>

                <Field name="db_config.db_user" class="grid grid-cols-4 items-center gap-4">
                    <FieldLabel for="db_user" class="text-right">DB User</FieldLabel>
                    <Input
                        id="db_user"
                        bind:value={db_config.db_user}
                        class="col-span-3"
                    /><FieldErrors errorStyle="!m-0" class="col-span-4" />
                </Field>

                <Field name="db_config.db_password" class="grid grid-cols-4 items-center gap-4">
                    <FieldLabel for="db_password" class="text-right">DB Password</FieldLabel>
                    <Input
                        id="db_password"
                        bind:value={db_config.db_password}
                        class="col-span-3"
                    /><FieldErrors errorStyle="!m-0" class="col-span-4" />
                </Field>

                <Field name="db_config.db_host" class="grid grid-cols-4 items-center gap-4">
                    <FieldLabel for="db_host" class="text-right">DB Host</FieldLabel>
                    <Input
                        id="db_host"
                        bind:value={db_config.db_host}
                        class="col-span-3"
                    /><FieldErrors errorStyle="!m-0" class="col-span-4" />
                </Field>

                <Field name="db_config.db_port" class="grid grid-cols-4 items-center gap-4">
                    <FieldLabel for="db_port" class="text-right">DB Port</FieldLabel>
                    <Input
                        id="db_port"
                        type="number"
                        min={0}
                        bind:value={db_config.db_port}
                        class="col-span-3"
                    /><FieldErrors errorStyle="!m-0" class="col-span-4" />
                </Field>
            </div>
            <Dialog.Footer>
                <FormSubmit>Create notebook</FormSubmit>
            </Dialog.Footer>
        </form>
    </Dialog.Content>
</Dialog.Root>
