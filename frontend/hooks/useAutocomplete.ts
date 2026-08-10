import { useCallback, useEffect, useRef, useState } from "react";
import { fetchAutocompleteSuggestions } from "../services/autocomplete";
import type { AutocompleteSuggestion } from "../types/autocomplete";
import type { RerankItem } from "../types/bigram";

const DEBOUNCE_MS = 30;

interface UseAutocompleteOptions {
  rerankFn?: (prev: string, candidates: [string, number][]) => Promise<RerankItem[]>;
  prevWord?: string;
  bigramEnabled?: boolean;
}

export function useAutocomplete(options: UseAutocompleteOptions = {}) {
  const { rerankFn, prevWord, bigramEnabled } = options;
  const [suggestions, setSuggestions] = useState<AutocompleteSuggestion[]>([]);
  const [activeIndex, setActiveIndex] = useState(0);
  const [latencyMs, setLatencyMs] = useState<number | null>(null);
  const [isOpen, setIsOpen] = useState(false);

  const debounceRef = useRef<ReturnType<typeof setTimeout> | null>(null);
  const abortRef = useRef<AbortController | null>(null);
  const requestIdRef = useRef(0);

  const query = useCallback(
    (prefix: string) => {
      if (debounceRef.current) {
        clearTimeout(debounceRef.current);
      }

      if (!prefix.trim()) {
        abortRef.current?.abort();
        setSuggestions([]);
        setIsOpen(false);
        return;
      }

      debounceRef.current = setTimeout(async () => {
        abortRef.current?.abort();
        const controller = new AbortController();
        abortRef.current = controller;
        const requestId = ++requestIdRef.current;
        const startedAt = performance.now();

        try {
          const response = await fetchAutocompleteSuggestions(
            prefix,
            5,
            controller.signal
          );

          if (requestId !== requestIdRef.current) return;

          let finalSuggestions = response.suggestions;
          if (
            bigramEnabled &&
            prevWord &&
            rerankFn &&
            finalSuggestions.length > 0
          ) {
            const candidates: [string, number][] = finalSuggestions.map((s) => [
              s.word,
              s.frequency,
            ]);
            const reranked = await rerankFn(prevWord, candidates);
            finalSuggestions = reranked.map((item) => ({
              word: item.word,
              frequency: item.frequency,
            }));
          }

          setSuggestions(finalSuggestions);
          setActiveIndex(0);
          setIsOpen(finalSuggestions.length > 0);
          setLatencyMs(performance.now() - startedAt);
        } catch (error) {
          if (error instanceof DOMException && error.name === "AbortError") {
            return;
          }
          setSuggestions([]);
          setIsOpen(false);
        }
      }, DEBOUNCE_MS);
    },
    [rerankFn, prevWord, bigramEnabled]
  );

  const clear = useCallback(() => {
    abortRef.current?.abort();
    if (debounceRef.current) {
      clearTimeout(debounceRef.current);
    }
    setSuggestions([]);
    setIsOpen(false);
    setActiveIndex(0);
  }, []);

  const moveActiveIndex = useCallback(
    (delta: number) => {
      setActiveIndex((current) => {
        if (suggestions.length === 0) return 0;
        return (current + delta + suggestions.length) % suggestions.length;
      });
    },
    [suggestions.length]
  );

  useEffect(() => {
    return () => {
      abortRef.current?.abort();
      if (debounceRef.current) {
        clearTimeout(debounceRef.current);
      }
    };
  }, []);

  return {
    suggestions,
    activeIndex,
    isOpen,
    latencyMs,
    query,
    clear,
    moveActiveIndex,
    setActiveIndex,
  };
}