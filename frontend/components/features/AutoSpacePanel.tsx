"use client";

import { useSegmentation } from "../../hooks/useSegmentation";
import Button from "../common/Button";
import Loading from "../common/Loading";
import DPTable from "../dp/DPTable";

export default function AutoSpacePanel() {
  const { input, setInput, result, loading, error, segment } = useSegmentation();

  return (
    <div className="auto-space-panel p-6 border border-[#dce8e4] rounded-2xl bg-white">
      <h3 className="text-lg font-semibold text-[#17231f] mb-2">Auto-Space</h3>
      <p className="text-sm text-[#66746f] mb-4">
        Masukkan string tanpa spasi, mis. "programdinamis"
      </p>

      <div className="flex flex-wrap gap-3 mb-4">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="programdinamis"
          className="flex-1 min-w-[200px] px-4 py-2 border border-[#dce8e4] rounded-xl focus:outline-none focus:ring-2 focus:ring-[#397f70] focus:border-transparent"
          disabled={loading}
          onKeyDown={(e) => {
            if (e.key === "Enter") {
              e.preventDefault();
              segment();
            }
          }}
        />
        <Button onClick={segment} disabled={loading || !input.trim()}>
          {loading ? "Memproses..." : "Segmentasi"}
        </Button>
      </div>

      {error && (
        <div className="mb-4 p-3 bg-[#fde8e8] text-[#bd5b5b] rounded-xl text-sm">
          {error}
        </div>
      )}

      {loading && (
        <div className="py-6">
          <Loading label="Menyegmentasi teks..." />
        </div>
      )}

      {result && result.success && !loading && (
        <div className="result-section space-y-3">
          <div className="result-text text-lg">
            <strong>Hasil segmentasi:</strong>{" "}
            <span className="text-[#397f70] font-medium">{result.result}</span>
          </div>
          <div className="result-cost text-sm text-[#66746f]">
            <strong>Total cost:</strong> {result.cost.toFixed(4)}
          </div>

          {result.dp.length > 0 && (
            <DPTable
              dp={result.dp}
              choices={result.choices}
              words={result.words}
              text={result.text}
            />
          )}
        </div>
      )}

      {result && !result.success && !loading && (
        <div className="p-3 bg-[#fde8e8] text-[#bd5b5b] rounded-xl text-sm">
          {result.error || "Segmentasi gagal."}
        </div>
      )}
    </div>
  );
}