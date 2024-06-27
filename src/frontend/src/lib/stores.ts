import { writable } from "svelte/store";
import type { NoteBookInterface, UserInterface } from "./types";


export const userData = writable<UserInterface | null>(null);

export const myNotebooks = writable<NoteBookInterface[]>([]);
