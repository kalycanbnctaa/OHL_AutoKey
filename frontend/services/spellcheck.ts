import { api } from "./api";
import type {
  SpellCheckWordResponse,
  SpellCheckTextResponse,
} from "../types/spellcheck";

export async function checkWord(
  word: string,
  maxDistance = 2,
  topN = 5
): Promise<SpellCheckWordResponse> {
  const params = new URLSearchParams({
    word,
    max_distance: String(maxDistance),
    top_n: String(topN),
  });
  return api.get<SpellCheckWordResponse>(`/spellcheck/word?${params}`);
}

export async function checkText(
  text: string,
  maxDistance = 2,
  topN = 5
): Promise<SpellCheckTextResponse> {
  const params = new URLSearchParams({
    max_distance: String(maxDistance),
    top_n: String(topN),
  });
  const API_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";
  const response = await fetch(`${API_URL}/spellcheck/check-text?${params}`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ text }),
  });
  if (!response.ok) {
    throw new Error(`Failed to check text: ${response.status}`);
  }
  return response.json();
}

export async function addWordToDictionary(word: string): Promise<{ status: string; word: string }> {
  return api.post<{ status: string; word: string }>("/dictionary/add", { word });
}