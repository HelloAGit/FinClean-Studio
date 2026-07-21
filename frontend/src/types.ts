export type DatasetType =
  | "bank_transactions"
  | "general_ledger"
  | "accounts_payable"
  | "accounts_receivable"
  | "budget";

export interface DatasetProfile {
  dataset_id: string;
  rows: number;
  columns: number;
  data_types: Record<string, string>;
  missing_percentages: Record<string, number>;
  unique_counts: Record<string, number>;
  duplicate_rows: number;
  amount_stats: Record<
    string,
    { min: number | null; max: number | null; mean: number | null }
  >;
  date_ranges: Record<string, { min: string | null; max: string | null }>;
  currency_formats: Record<string, { examples: string[] }>;
  sensitive_columns: string[];
  quality_score: number;
}

export interface Correction {
  row_index: number;
  field: string;
  original_value: string | null;
  proposed_value: string | null;
  reason: string;
  confidence: number;
  decision?: "approve" | "reject" | "modify";
}
