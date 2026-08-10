import { useState, useEffect, useCallback } from "react";
import {
  recordPair,
  rerank,
  getBigramStatistics,
} from "../services/bigram";
import type { RerankItem, StatisticsResponse } from "../types/bigram";

const SESSION_KEY = "autokey_session_id";

function getSessionId(): string {
  let id = sessionStorage.getItem(SESSION_KEY);
  if (!id) {
    id = crypto.randomUUID();
    sessionStorage.setItem(SESSION_KEY, id);
  }
  return id;
}

export function useBigram() {
  const [sessionId] = useState(getSessionId);
  const [enabled, setEnabled] = useState(true);
  const [statistics, setStatistics] = useState<StatisticsResponse>({
    total_pairs: 0,
    unique_pairs: 0,
  });

  const refreshStatistics = useCallback(async () => {
    try {
      const stats = await getBigramStatistics(sessionId);
      setStatistics(stats);
    } catch {
    }
  }, [sessionId]);

  useEffect(() => {
    refreshStatistics();
  }, [refreshStatistics]);

  const recordPair = useCallback(
    async (prev: string, curr: string) => {
      if (!enabled || !prev || !curr) return;
      try {
        await recordPair(prev, curr, sessionId);
        await refreshStatistics();
      } catch {
      }
    },
    [enabled, sessionId, refreshStatistics]
  );

  const rerankSuggestions = useCallback(
    async (prev: string, candidates: [string, number][]): Promise<RerankItem[]> => {
      if (!enabled || !prev || !candidates.length) {
        return candidates.map(([word, freq]) => ({ word, frequency: freq, score: 0 }));
      }
      try {
        const response = await rerank(prev, candidates, sessionId);
        return response.candidates;
      } catch {
        return candidates.map(([word, freq]) => ({ word, frequency: freq, score: 0 }));
      }
    },
    [enabled, sessionId]
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