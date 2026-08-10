export type SmartTrimItem = {
  word: string;
  weight: number;
  value: number;
};

export type SmartTrimRequest = {
  text: string;
  limit: number;
};

export type SmartTrimResponse = {
  text: string;
  limit: number;
  items: SmartTrimItem[];
  total_value: number;
  total_weight: number;
  dp_table: number[][];
  success: boolean;
  error: string | null;
};