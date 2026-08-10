import { api } from "./api";
import type { SmartTrimResponse } from "../types/smartTrim";

export async function smartTrim(text: string, limit: number): Promise<SmartTrimResponse> {
  return api.post<SmartTrimResponse>("/smart-trim", { text, limit });
}