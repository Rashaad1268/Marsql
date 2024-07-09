export interface UserInterface {
    id: number;
    username: string;
    is_staff: boolean;
}

export interface NoteBookInterface {
    id: number;
    name: string;
    creator: UserInterface;
    created_at: string;

    db_config: {
        db_type: number;
        db_type_display: string;
        db_name: string;
        db_user: string;
        db_host: string;
        db_port: string;
    };
}

export interface CellDataInterface {
    id: number;
    timesRun: number;
    content: string;
    type: 1 | 2;
    notebook: number;
    output?: {
        status: "success" | "error",
        error_message?: string, 
        columns: string[];
        results: Array<any>;
        rows_affected: number;
        status_message: string | null;
    };
}


export enum MessageAuthorTypes {
    user = 1,
    AI = 2,
}

export interface ChatMessageInterface {
    id: number;
    notebook: number;
    author_type: MessageAuthorTypes;
    content: string;
    created_at: string | null; // if the created_at is null that means that the message is still being sent
    cell: CellDataInterface | null;
    attached_image: string | null;
    attached_file: string | null;
}

export interface PaginatorInterface<T> {
    count: number;
    results: Array<T>;
}