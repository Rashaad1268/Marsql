import { setContext } from "svelte";
import { writable } from "svelte/store";

export { default as Field } from "./field.svelte";
export { default as FieldErrors } from "./fieldError.svelte";
export { default as FieldLabel } from "./fieldLabel.svelte";


export interface FormErrorInterface { [fieldName: string]: string[] };
export interface FormFieldInterface { name: string };

export function createForm() {
    const formErrors = writable<FormErrorInterface>({});
    setContext('formErrors', formErrors)
    
    const formMessages = writable<string[]>([]);
    setContext('formMessages', formMessages)

    return {
        errors: formErrors,
        messages: formMessages,

        setErrors(fieldName: string, errors: string[]) {
            formErrors.update((errs) => {
                errs[fieldName] = errors
                return errs;
            })
        },

        isValid() {
            return Object.keys(this.errors).length === 0;
        }
    }
}


export type FormType = ReturnType<typeof createForm>;
