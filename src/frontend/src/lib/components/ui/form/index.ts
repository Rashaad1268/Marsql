import { setContext } from "svelte";
import { get, writable } from "svelte/store";

export { default as Field } from "./field.svelte";
export { default as FieldErrors } from "./fieldError.svelte"
export { default as FieldLabel } from "./fieldLabel.svelte";
export { default as FormMessages } from "./formMessages.svelte";
export { default as FormSubmit } from "./formSubmit.svelte";

export interface FormErrorInterface {
    [fieldName: string]: string[];
}
export interface FormFieldInterface {
    name: string;
}

export function createForm() {
    const formErrors = writable<FormErrorInterface>({});
    setContext("formErrors", formErrors);

    const formMessages = writable<string[]>([]);
    setContext("formMessages", formMessages);

    return {
        errors: formErrors,
        messages: formMessages,

        setErrors(fieldName: string, errors: string[]) {
            formErrors.update((errs) => {
                errs[fieldName] = errors;
                return errs;
            });
        },

        setBackendErrors(data: any) {
            this.clearState();

            for (const [key, value] of Object.entries(data)) {
                if (key === "detail") {
                    this.messages.set(Array.isArray(value) ? value : [value]);
                } else {
                    if (JSON.stringify(value).startsWith('{')) { // check if the value is a JS object
                        for (const [k, v] of Object.entries(value as any)) {
                            this.setErrors(key + '.' + k, v as string[]);
                        }
                    } else {
                        this.setErrors(key, value as string[]);
                    }
                }
            }
        },

        clearState() {
            this.errors.set({})
            this.messages.set([])
        },

        isValid() {
            return Object.keys(get(this.errors)).length === 0;
        }
    };
}

export type FormType = ReturnType<typeof createForm>;
