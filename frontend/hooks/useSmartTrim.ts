import { useState } from "react";
import { smartTrim } from "../services/smartTrim";
import type { SmartTrimResponse } from "../types/smartTrim";

export function useSmartTrim() {
  const [text, setText] = useState("");
  const [limit, setLimit] = useState(30);
  const [result, setResult] = useState<SmartTrimResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const trim = async () => {
    if (!text.trim()) {
      setError("Masukkan teks yang akan di-trim.");
      return;
    }
    if (limit <= 0) {
      setError("Batas karakter harus lebih dari 0.");
      return;
    }
    setLoading(true);
    setError(null);
    try {
      const res = await smartTrim(text, limit);
      setResult(res);
      if (!res.success) {
        setError(res.error || "Smart Trim gagal.");
      }
    } catch (e) {
      setError((e as Error).message);
    } finally {
      setLoading(false);
    }
  };

  return { text, setText, limit, setLimit, result, loading, error, trim };
}