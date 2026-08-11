"use client";

import Toggle from "../common/Toggle";
import Badge from "../common/Badge";
import type { StatisticsResponse } from "../../types/bigram";

type BigramPanelProps = {
  enabled: boolean;
  setEnabled: (enabled: boolean) => void;
  statistics: StatisticsResponse;
};

export default function BigramPanel({
  enabled,
  setEnabled,
  statistics,
}: BigramPanelProps) {
  return (
    <div className="bigram-panel p-6 border border-[#dce8e4] rounded-2xl bg-white">
      <div className="flex items-center justify-between flex-wrap gap-3 mb-2">
        <h3 className="text-lg font-semibold text-[#17231f]">Bigram Language Model</h3>
        <Badge variant={enabled ? "success" : "default"}>
          {enabled ? "Aktif" : "Nonaktif"}
        </Badge>
      </div>

      <p className="text-sm text-[#66746f] mb-4">
        Autocomplete diurutkan berdasarkan konteks kata sebelumnya.
      </p>

      <div className="bigram-controls flex flex-wrap items-center gap-6">
        <Toggle
          enabled={enabled}
          onChange={setEnabled}
          label="Bigram reranking"
        />

        <div className="bigram-stats flex gap-4 text-sm text-[#66746f]">
          <span>
            Pasangan tercatat: <strong className="text-[#17231f]">{statistics.total_pairs}</strong>
          </span>
          <span>
            Unik: <strong className="text-[#17231f]">{statistics.unique_pairs}</strong>
          </span>
        </div>
      </div>

      <div className="bigram-info mt-4 p-3 bg-[#f5f8f7] rounded-xl text-sm text-[#66746f]">
        {enabled ? (
          <p>✅ Bigram aktif. Saran autocomplete diurutkan berdasarkan konteks kata sebelumnya.</p>
        ) : (
          <p>⏸ Bigram nonaktif. Saran autocomplete menggunakan frekuensi unigram.</p>
        )}
      </div>
    </div>
  );
}