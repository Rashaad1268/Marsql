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
        columns: string[];
        results: Array<any>;
        rows_affected: number;
        status_message: string | null;
        error?: string;
    };
}


export enum MessageAuthorTypes {
    user = 1,
    AI = 2,
}