import type { NoteBookInterface } from "$lib/types.js";
import type { LayoutLoad } from "./$types";

interface APIResponse {
    notebook: NoteBookInterface;

    db_schema: { [key: string]: [{ name: string; data_type: string; is_nullable: boolean }] };
}

export const load: LayoutLoad = async ({ params, fetch }) => {
    return (await (await fetch(`/api/notebooks/${params.id}/`)).json()) as APIResponse;
};
