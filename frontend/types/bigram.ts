export type BigramStatistics = {
  total_pairs: number;
  unique_pairs: number;
};

export type RecordPairRequest = {
  prev: string;
  curr: string;
};

export type RecordPairResponse = {
  success: boolean;
  total_pairs: number;
  unique_pairs: number;
};

export type RerankItem = {
  word: string;
  frequency: number;
  score: number;
};

export type RerankRequest = {
  prev: string;
  candidates: [string, number][];
};

export type RerankResponse = {
  prev: string;
  candidates: RerankItem[];
};

export type StatisticsResponse = BigramStatistics;