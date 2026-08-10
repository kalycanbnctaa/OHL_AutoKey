export type AutocompleteSuggestion = {
  word: string;
  frequency: number;
};

export type AutocompleteResponse = {
  prefix: string;
  suggestions: AutocompleteSuggestion[];
  latency_ms: number;
};