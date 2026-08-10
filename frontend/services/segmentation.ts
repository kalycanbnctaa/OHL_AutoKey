import { api } from "./api";
import type { SegmentResponse } from "../types/segmentation";

export async function segmentText(text: string): Promise<SegmentResponse> {
  return api.post<SegmentResponse>("/segment", { text });
}