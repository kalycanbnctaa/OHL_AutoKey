"use client";

import { useSmartTrim } from "../../hooks/useSmartTrim";
import Button from "../common/Button";
import Loading from "../common/Loading";

export default function SmartTrimPanel() {
  const { text, setText, limit, setLimit, result, loading, error, trim } = useSmartTrim();

  return (
    <div className="smart-trim-panel p-6 border border-[#dce8e4] rounded-2xl bg-white">
      <h3 className="text-lg font-semibold text-[#17231f] mb-2">Smart Trim</h3>
      <p className="text-sm text-[#66746f] mb-4">
        Pilih subset kata yang memaksimalkan nilai tanpa melebihi batas karakter (0/1 Knapsack).
      </p>

      <div className="space-y-3 mb-4">
        <textarea
          value={text}
          onChange={(e) => setText(e.target.value)}
          placeholder="Masukkan teks yang akan dipendekkan..."
          className="smart-trim-textarea w-full min-h-[80px] px-4 py-2 border border-[#dce8e4] rounded-xl focus:outline-none focus:ring-2 focus:ring-[#397f70] focus:border-transparent resize-vertical font-inherit"
          disabled={loading}
        />

        <div className="flex flex-wrap items-center gap-4">
          <div className="flex items-center gap-2">
            <label className="text-sm font-medium text-[#66746f]">
              Batas karakter:
            </label>
            <input
              type="number"
              value={limit}
              onChange={(e) => setLimit(Number(e.target.value))}
              className="w-20 px-3 py-1.5 border border-[#dce8e4] rounded-xl focus:outline-none focus:ring-2 focus:ring-[#397f70] focus:border-transparent"
              min={1}
              disabled={loading}
            />
          </div>
          <Button onClick={trim} disabled={loading || !text.trim()}>
            {loading ? "Memproses..." : "Trim"}
          </Button>
        </div>
      </div>

      {error && (
        <div className="mb-4 p-3 bg-[#fde8e8] text-[#bd5b5b] rounded-xl text-sm">
          {error}
        </div>
      )}

      {loading && (
        <div className="py-6">
          <Loading label="Menghitung Knapsack..." />
        </div>
      )}

      {result && result.success && !loading && (
        <div className="result-section space-y-3">
          <div className="result-summary flex flex-wrap gap-6 text-sm text-[#66746f]">
            <span>
              <strong>Kata dipertahankan:</strong> {result.items.length}
            </span>
            <span>
              <strong>Total panjang:</strong> {result.total_weight} karakter
            </span>
            <span>
              <strong>Total value:</strong> {result.total_value.toFixed(4)}
            </span>
          </div>

          <div className="trimmed-words flex flex-wrap gap-2 py-2">
            {result.items.map((item, idx) => (
              <span
                key={idx}
                className="trimmed-word inline-flex items-center gap-1 px-3 py-1 bg-[#dff0eb] rounded-full text-sm text-[#2b685b]"
              >
                {item.word}
                <span className="trimmed-meta text-[#66746f] text-xs">
                  ({item.weight})
                </span>
              </span>
            ))}
          </div>

          {result.items.length === 0 && (
            <p className="text-sm text-[#66746f]">
              Tidak ada kata yang dapat dipertahankan dalam batas {result.limit} karakter.
            </p>
          )}
        </div>
      )}

      {result && !result.success && !loading && (
        <div className="p-3 bg-[#fde8e8] text-[#bd5b5b] rounded-xl text-sm">
          {result.error || "Smart Trim gagal."}
        </div>
      )}
    </div>
  );
}