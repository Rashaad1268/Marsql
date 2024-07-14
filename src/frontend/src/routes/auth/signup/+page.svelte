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

    let username: string;
    let email: string;
    let password: string;
    let password2: string;

    async function handleSignup() {
        if (password !== password2) {
            form.messages.set(["Passwords don't match"]);
            return;
        }

        const response = await fetchApi("auth/signup/", {
            method: "POST",
            body: JSON.stringify({
                username,
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
            form.setBackendErrors(await response.json());
        }
    }
</script>

<svelte:head>
    <title>Login</title>
</svelte:head>

<BackgroundGrid />

<div class="login-form w-full h-full flex flex-col items-center">
    <Card.Root class="max-w-lg w-full p-10 bg-background/90">
        <Card.Header class="text-center">
            <h1 class="font-bold text-4xl">The journey begins...</h1>
            <h3>Don't have an account? <a href="signup{nextUrl}" class="link">Login</a></h3>
        </Card.Header>

        <Card.Content>
            <form class="flex flex-col gap-2" on:submit|preventDefault={handleSignup}>
                <Field name="username">
                    <FieldLabel for="username">Username</FieldLabel>
                    <Input
                        id="username"
                        bind:value={username}
                        autocomplete="username"
                        placeholder="Username"
                        required
                    />
                    <FieldErrors />
                </Field>

                <Field name="email">
                    <FieldLabel for="email">Email</FieldLabel>
                    <Input
                        id="email"
                        bind:value={email}
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
                        type="password"
                        bind:value={password}
                        autocomplete="current-password"
                        placeholder="Password"
                        required
                    />
                    <FieldErrors />
                </Field>

                <Field name="password2">
                    <FieldLabel>Password (confirmation)</FieldLabel>
                    <Input
                        id="password2"
                        type="password"
                        bind:value={password2}
                        autocomplete="current-password"
                        placeholder="Password (again)"
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
