<header>
    <a class="nav-title size-8 flex items-center gap-4" href="/">Marsql</a>
</header>

<style lang="postcss">
    header {
        @apply flex items-center bg-background bg-background/60 font-bold
			 shadow-neutral-800 shadow-sm sticky top-0 px-8
			   h-[var(--navbar-height)] max-h-[var(--navbar-height)];

        height: var(--navbar-height);
        max-height: var(--navbar-height);
    }

    .nav-title {
        @apply font-sans text-4xl;
    }
</style>
