import { api } from "./api";
import type { AutocompleteResponse } from "../types/autocomplete";

export async function fetchAutocompleteSuggestions(
  prefix: string,
  topN = 5,
  signal?: AbortSignal,
): Promise<AutocompleteResponse> {
  const params = new URLSearchParams({
    prefix,
    top_n: String(topN),
  });

  return api.get<AutocompleteResponse>(
    `/autocomplete?${params.toString()}`,
    signal,
  );
}