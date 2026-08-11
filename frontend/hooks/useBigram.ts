import { useState, useEffect, useCallback } from "react";
import {
  recordPair as recordPairApi,
  rerank as rerankApi,
  getBigramStatistics,
} from "../services/bigram";
import type { RerankItem, StatisticsResponse } from "../types/bigram";

const SESSION_KEY = "autokey_session_id";

function readOrCreateSessionId(): string {
  let id = sessionStorage.getItem(SESSION_KEY);

  if (!id) {
    id = crypto.randomUUID();
    sessionStorage.setItem(SESSION_KEY, id);
  }

  return id;
}

export function useBigram() {
  const [sessionId, setSessionId] = useState<string>("");
  const [enabled, setEnabled] = useState(true);
  const [statistics, setStatistics] = useState<StatisticsResponse>({
    total_pairs: 0,
    unique_pairs: 0,
  });

  useEffect(() => {
    setSessionId(readOrCreateSessionId());
  }, []);

  const refreshStatistics = useCallback(async () => {
    if (!sessionId) return;

    try {
      const stats = await getBigramStatistics(sessionId);
      setStatistics(stats);
    } catch {
      return;
    }
  }, [sessionId]);

  useEffect(() => {
    refreshStatistics();
  }, [refreshStatistics]);

  const recordPair = useCallback(
    async (prev: string, curr: string) => {
      if (!enabled || !prev || !curr || !sessionId) return;

      try {
        await recordPairApi(prev, curr, sessionId);
        await refreshStatistics();
      } catch {
        return;
      }
    },
    [enabled, sessionId, refreshStatistics],
  );

  const rerankSuggestions = useCallback(
    async (
      prev: string,
      candidates: [string, number][],
    ): Promise<RerankItem[]> => {
      if (!enabled || !prev || !candidates.length || !sessionId) {
        return candidates.map(([word, freq]) => ({
          word,
          frequency: freq,
          score: 0,
        }));
      }

      try {
        const response = await rerankApi(prev, candidates, sessionId);
        return response.candidates;
      } catch {
        return candidates.map(([word, freq]) => ({
          word,
          frequency: freq,
          score: 0,
        }));
      }
    },
    [enabled, sessionId],
  );

  return {
    enabled,
    setEnabled,
    statistics,
    refreshStatistics,
    recordPair,
    rerankSuggestions,
    sessionId,
  };
}