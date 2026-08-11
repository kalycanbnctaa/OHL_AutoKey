import { api } from "./api";
import type {
  RecordPairResponse,
  RerankResponse,
  StatisticsResponse,
} from "../types/bigram";

export async function recordPair(
  prev: string,
  curr: string,
  sessionId?: string,
): Promise<RecordPairResponse> {
  const headers: HeadersInit = {};

  if (sessionId) {
    headers["X-Session-Id"] = sessionId;
  }

  return api.post<RecordPairResponse>(
    "/bigram/record",
    { prev, curr },
    undefined,
    headers,
  );
}

export async function rerank(
  prev: string,
  candidates: [string, number][],
  sessionId?: string,
): Promise<RerankResponse> {
  const headers: HeadersInit = {};

  if (sessionId) {
    headers["X-Session-Id"] = sessionId;
  }

  return api.post<RerankResponse>(
    "/bigram/rerank",
    { prev, candidates },
    undefined,
    headers,
  );
}

export async function getBigramStatistics(
  sessionId?: string,
): Promise<StatisticsResponse> {
  const headers: HeadersInit = {};

  if (sessionId) {
    headers["X-Session-Id"] = sessionId;
  }

  return api.get<StatisticsResponse>(
    "/bigram/statistics",
    undefined,
    headers,
  );
}