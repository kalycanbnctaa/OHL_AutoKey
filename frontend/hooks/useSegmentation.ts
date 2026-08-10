import { useState } from "react";
import { segmentText } from "../services/segmentation";
import type { SegmentResponse } from "../types/segmentation";

export function useSegmentation() {
  const [input, setInput] = useState("");
  const [result, setResult] = useState<SegmentResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const segment = async () => {
    if (!input.trim()) {
      setError("Masukkan string tanpa spasi.");
      return;
    }
    setLoading(true);
    setError(null);
    try {
      const res = await segmentText(input.trim());
      setResult(res);
      if (!res.success) {
        setError(res.error || "Segmentasi gagal.");
      }
    } catch (e) {
      setError((e as Error).message);
    } finally {
      setLoading(false);
    }
  };

  return { input, setInput, result, loading, error, segment };
}