"use client";

import { useState } from "react";
import Button from "../common/Button";
import Loading from "../common/Loading";

type LevenshteinTableResponse = {
  source: string;
  target: string;
  table: number[][];
  distance: number;
};

export default function LevenshteinPanel() {
  const [source, setSource] = useState("");
  const [target, setTarget] = useState("");
  const [result, setResult] = useState<LevenshteinTableResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const fetchTable = async () => {
    if (!source.trim() || !target.trim()) {
      setError("Masukkan kedua kata.");
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const apiUrl = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";
      const params = new URLSearchParams({
        source: source.trim(),
        target: target.trim(),
      });
      const response = await fetch(
        `${apiUrl}/levenshtein/table?${params}`,
        { cache: "no-store" }
      );

      if (!response.ok) {
        throw new Error("Gagal menghitung Levenshtein");
      }

      const data = (await response.json()) as LevenshteinTableResponse;
      setResult(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Terjadi kesalahan");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="p-6 border border-[#dce8e4] rounded-2xl bg-white">
      <h3 className="text-lg font-semibold text-[#17231f] mb-4">
        Levenshtein Edit Distance
      </h3>

      <div className="flex flex-wrap gap-4 mb-4">
        <div className="flex-1 min-w-[160px]">
          <label className="block text-sm font-medium text-[#66746f] mb-1">
            Kata 1 (source)
          </label>
          <input
            type="text"
            value={source}
            onChange={(e) => setSource(e.target.value)}
            placeholder="mis. kitten"
            className="w-full px-4 py-2 border border-[#dce8e4] rounded-xl focus:outline-none focus:ring-2 focus:ring-[#397f70] focus:border-transparent"
            disabled={loading}
          />
        </div>
        <div className="flex-1 min-w-[160px]">
          <label className="block text-sm font-medium text-[#66746f] mb-1">
            Kata 2 (target)
          </label>
          <input
            type="text"
            value={target}
            onChange={(e) => setTarget(e.target.value)}
            placeholder="mis. sitting"
            className="w-full px-4 py-2 border border-[#dce8e4] rounded-xl focus:outline-none focus:ring-2 focus:ring-[#397f70] focus:border-transparent"
            disabled={loading}
          />
        </div>
        <div className="flex items-end">
          <Button onClick={fetchTable} disabled={loading}>
            {loading ? "Menghitung..." : "Hitung"}
          </Button>
        </div>
      </div>

      {error && (
        <div className="mb-4 p-3 bg-[#fde8e8] text-[#bd5b5b] rounded-xl text-sm">
          {error}
        </div>
      )}

      {loading && (
        <div className="py-8">
          <Loading label="Menghitung tabel DP..." />
        </div>
      )}

      {result && !loading && (
        <div className="mt-4 space-y-4">
          <div className="flex flex-wrap items-center gap-4">
            <span className="text-sm font-medium text-[#66746f]">
              Jarak edit:
            </span>
            <span className="text-xl font-bold text-[#397f70]">
              {result.distance}
            </span>
          </div>

          <div className="overflow-x-auto">
            <div className="inline-block min-w-full">
              <table className="border-collapse text-sm">
                <thead>
                  <tr>
                    <th className="px-2 py-1 text-[#66746f] font-medium text-xs"> </th>
                    <th className="px-2 py-1 text-[#66746f] font-medium text-xs">ε</th>
                    {result.target.split("").map((ch, i) => (
                      <th key={i} className="px-2 py-1 text-[#66746f] font-medium text-xs">
                        {ch}
                      </th>
                    ))}
                  </tr>
                </thead>
                <tbody>
                  {result.table.map((row, i) => (
                    <tr key={i}>
                      <td className="px-2 py-1 text-[#66746f] font-medium text-xs">
                        {i === 0 ? "ε" : result.source[i - 1]}
                      </td>
                      {row.map((val, j) => (
                        <td
                          key={j}
                          className={[
                            "px-3 py-1 border border-[#eef5f2] text-center min-w-[36px]",
                            i === result.source.length && j === result.target.length
                              ? "bg-[#397f70] text-white font-bold"
                              : "",
                          ].join(" ")}
                        >
                          {val}
                        </td>
                      ))}
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>

          <div className="text-xs text-[#66746f] bg-[#f5f8f7] p-3 rounded-xl">
            <p className="font-medium mb-1">Basis:</p>
            <p>dp[0][j] = j, dp[i][0] = i</p>
            <p className="font-medium mt-2 mb-1">Relasi Rekurens:</p>
            <p>
              dp[i][j] = min(dp[i-1][j] + 1, dp[i][j-1] + 1, dp[i-1][j-1] + cost)
            </p>
            <p className="text-xs mt-1">cost = 0 jika sama, 1 jika berbeda</p>
          </div>
        </div>
      )}
    </div>
  );
}