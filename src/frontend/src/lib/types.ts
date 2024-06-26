export interface CellData {
	timesRun: number;
	query: string;
	output?: {
		columns: string[];
		results: Array<any>;
	};
    error?: string;
}
