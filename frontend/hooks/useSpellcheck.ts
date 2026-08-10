import { useCallback, useState } from "react";
import { checkWord, addWordToDictionary } from "../services/spellcheck";
import type { SpellCheckCandidateResponse } from "../types/spellcheck";

export type MisspelledWord = {
  word: string;
  start: number;
  end: number;
  suggestions: SpellCheckCandidateResponse[];
};

export function useSpellcheck() {
  const [misspelled, setMisspelled] = useState<MisspelledWord[]>([]);
  const [activeSuggestion, setActiveSuggestion] = useState<{
    word: string;
    start: number;
    end: number;
    suggestions: SpellCheckCandidateResponse[];
    position: { top: number; left: number };
  } | null>(null);

  const validateWord = useCallback(
    async (word: string, start: number, end: number) => {
      if (!word.trim()) return;
      const response = await checkWord(word, 2, 5);
      if (!response.is_valid) {
        setMisspelled((prev) => [
          ...prev.filter((m) => m.start !== start || m.end !== end),
          {
            word,
            start,
            end,
            suggestions: response.suggestions,
          },
        ]);
      } else {
        setMisspelled((prev) =>
          prev.filter((m) => m.start !== start || m.end !== end)
        );
      }
    },
    []
  );

  const clearAll = useCallback(() => {
    setMisspelled([]);
    setActiveSuggestion(null);
  }, []);

  const addToDictionary = useCallback(
    async (word: string, start: number, end: number) => {
      await addWordToDictionary(word);
      setMisspelled((prev) =>
        prev.filter((m) => m.start !== start || m.end !== end)
      );
      setActiveSuggestion(null);
    },
    []
  );

  const showSuggestions = useCallback(
    (
      word: string,
      start: number,
      end: number,
      suggestions: SpellCheckCandidateResponse[],
      position: { top: number; left: number }
    ) => {
      setActiveSuggestion({ word, start, end, suggestions, position });
    },
    []
  );

  const closeSuggestions = useCallback(() => {
    setActiveSuggestion(null);
  }, []);

  return {
    misspelled,
    setMisspelled,
    activeSuggestion,
    validateWord,
    clearAll,
    addToDictionary,
    showSuggestions,
    closeSuggestions,
  };
}