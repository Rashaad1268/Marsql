<script lang="ts">
    import { Button } from "$lib/components/ui/button";
    import * as Card from "$lib/components/ui/card";
    import * as DropdownMenu from "$lib/components/ui/dropdown-menu";
    import type { NoteBookInterface } from "$lib/types";

    export let notebook: NoteBookInterface;
</script>

<a
    href="/notebook/{notebook.id}/"
    on:click={(e) => {
        if (document.querySelector(`#notebook-card-ctx-menu-btn:hover`)) {
            // Disable the link if the context menu button is being hovered/clicked
            e.preventDefault();
        }
    }}
>
    <Card.Root class="h-full hover:border-primary transition-all">
        <Card.Header>
            <div class="flex">
                <div class="mr-auto">
                    <h1 class="text-xl font-roboto">{notebook.name}</h1>
                    <h4 class="text-muted-foreground text-sm">
                        {notebook.db_config.db_type_display} database
                    </h4>
                </div>

                <DropdownMenu.Root>
                    <DropdownMenu.Trigger asChild let:builder>
                        <Button
                            id="notebook-card-ctx-menu-btn"
                            builders={[builder]}
                            type="submit"
                            variant="ghost"
                            size="sm"
                        >
                            <svg
                                xmlns="http://www.w3.org/2000/svg"
                                class="size-3 fill-current"
                                viewBox="0 0 448 512"
                                ><!--!Font Awesome Free 6.5.2 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license/free Copyright 2024 Fonticons, Inc.--><path
                                    d="M8 256a56 56 0 1 1 112 0A56 56 0 1 1 8 256zm160 0a56 56 0 1 1 112 0 56 56 0 1 1 -112 0zm216-56a56 56 0 1 1 0 112 56 56 0 1 1 0-112z"
                                />
                            </svg>
                        </Button>
                    </DropdownMenu.Trigger>

                    <DropdownMenu.Content>
                        <!-- Replace with some actual options... -->
                        <DropdownMenu.Group>
                            <DropdownMenu.Label>My Account</DropdownMenu.Label>
                            <DropdownMenu.Separator />
                            <DropdownMenu.Item>Profile</DropdownMenu.Item>
                            <DropdownMenu.Item>Billing</DropdownMenu.Item>
                            <DropdownMenu.Item>Team</DropdownMenu.Item>
                            <DropdownMenu.Item>Subscription</DropdownMenu.Item>
                        </DropdownMenu.Group>
                    </DropdownMenu.Content>
                </DropdownMenu.Root>
            </div>
        </Card.Header>

        <Card.Content>
            <h3 class="text-lg font-medium">DB Configuration</h3>

            <ul class="pl-4 text-sm">
                <li>
                    Database name: <span class="font-mono ml-1">{notebook.db_config.db_name}</span>
                </li>

                <li>
                    Database user: <span class="ml-1 font-mono">{notebook.db_config.db_user}</span>
                </li>

                <li class="overflow-hidden whitespace-nowrap overflow-ellipsis">
                    Address: <span class="font-mono ml-1"
                        >{notebook.db_config.db_host}:{notebook.db_config.db_port}</span
                    >
                </li>
            </ul>
        </Card.Content>
    </Card.Root>
</a>
