import { api } from "./api";
import type {
  RecordPairResponse,
  RerankRequest,
  RerankResponse,
  StatisticsResponse,
} from "../types/bigram";

export async function recordPair(
  prev: string,
  curr: string,
  sessionId?: string
): Promise<RecordPairResponse> {
  const headers: HeadersInit = {};
  if (sessionId) {
    headers["X-Session-Id"] = sessionId;
  }
  return api.post<RecordPairResponse>("/bigram/record", { prev, curr });
}

export async function rerank(
  prev: string,
  candidates: [string, number][],
  sessionId?: string
): Promise<RerankResponse> {
  const headers: HeadersInit = {};
  if (sessionId) {
    headers["X-Session-Id"] = sessionId;
  }
  return api.post<RerankResponse>("/bigram/rerank", { prev, candidates });
}

export async function getBigramStatistics(sessionId?: string): Promise<StatisticsResponse> {
  const headers: HeadersInit = {};
  if (sessionId) {
    headers["X-Session-Id"] = sessionId;
  }
  const url = `${process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000"}/bigram/statistics`;
  const response = await fetch(url, {
    headers: {
      "Content-Type": "application/json",
      ...(sessionId ? { "X-Session-Id": sessionId } : {}),
    },
  });
  if (!response.ok) {
    throw new Error("Failed to fetch bigram statistics");
  }
  return response.json();
}