<script lang="ts">
    import { goto } from "$app/navigation";
    import { Input } from "$lib/components/ui/input";
    import * as Card from "$lib/components/ui/card";
    import BackgroundGrid from "../backgroundGrid.svelte";
    import { fetchApi } from "$lib/api";
    import { Field, FieldErrors, FieldLabel, FormSubmit } from "$lib/components/ui/form";
    import { fetchUserData } from "$lib/utils";
    import { page } from "$app/stores";
    import { createForm } from "$lib/components/ui/form";
    import { toast } from "svelte-sonner";

    $: nextEndpoint = $page.url.searchParams.get("next");
    $: nextUrl = nextEndpoint ? `?next=${nextEndpoint}` : "";

    const form = createForm();

    let email: string;
    let password: string;

    async function handleLogin() {
        const response = await fetchApi("auth/login/", {
            method: "POST",
            body: JSON.stringify({
                email,
                password
            })
        });

        if (response.ok) {
            try {
                fetchUserData().then(() => {
                    goto(nextEndpoint ?? "/");
                });
            } catch (err) {
                toast.error(`Error while fetching user data (${err})`);
            }
        } else {
            form.setBackendErrors(await response.json())
        }
    };
</script>

<svelte:head>
    <title>Login</title>
</svelte:head>

<BackgroundGrid />

<div class="login-form w-full h-full flex flex-col items-center">
    <Card.Root class="max-w-lg w-full p-10 bg-background/90">
        <Card.Header class="text-center">
            <h1 class="font-bold text-4xl">Welcome back</h1>
            <h3>Don't have an account? <a href="signup{nextUrl}" class="link">Signup</a></h3>
        </Card.Header>

        <Card.Content>
            <form class="flex flex-col gap-2" on:submit|preventDefault={handleLogin}>
                <Field name="email">
                    <FieldLabel>Email</FieldLabel>
                    <Input
                        bind:value={email}
                        name="email"
                        type="email"
                        autocomplete="email"
                        placeholder="Email"
                        required
                    />
                    <FieldErrors />
                </Field>

                <Field name="password">
                    <FieldLabel>Password</FieldLabel>
                    <Input
                        id="password"
                        name="password"
                        type="password"
                        bind:value={password}
                        autocomplete="current-password"
                        placeholder="Password"
                        required
                    />
                    <FieldErrors />
                </Field>

                <FormSubmit>Login</FormSubmit>
            </form>
        </Card.Content>
    </Card.Root>
</div>

<style lang="postcss">
    .login-form {
        @apply flex items-center justify-center z-10;

        left: 50%;
        position: absolute;
        top: 50%;
        transform: translate(-50%, -50%);
    }
</style>
