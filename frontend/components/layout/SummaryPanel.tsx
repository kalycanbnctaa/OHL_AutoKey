type TrieStatistics = {
  word_count: number;
  node_count: number;
  average_depth: number;
  memory_megabytes: number;
};

type SummaryPanelProps = {
  statistics: TrieStatistics | null;
  backendStatus: "checking" | "connected" | "disconnected";
};

export default function SummaryPanel({
  statistics,
  backendStatus,
}: SummaryPanelProps) {
  if (backendStatus === "disconnected") {
    return (
      <div className="p-6 border border-[#dce8e4] rounded-2xl bg-white text-center">
        <p className="text-[#bd5b5b] font-medium">Tidak dapat terhubung ke server.</p>
        <p className="text-sm text-[#66746f] mt-1">Pastikan backend berjalan di http://localhost:8000</p>
      </div>
    );
  }

  if (backendStatus === "checking" || !statistics) {
    return (
      <div className="p-6 border border-[#dce8e4] rounded-2xl bg-white text-center">
        <p className="text-[#66746f]">Memuat kamus...</p>
      </div>
    );
  }

  return (
    <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 p-4 bg-[#f5f8f7] rounded-2xl border border-[#dce8e4]">
      <div className="text-center">
        <div className="text-2xl font-bold text-[#17231f]">
          {statistics.word_count.toLocaleString("id-ID")}
        </div>
        <div className="text-sm text-[#66746f]">Kata</div>
      </div>
      <div className="text-center">
        <div className="text-2xl font-bold text-[#17231f]">
          {statistics.node_count.toLocaleString("id-ID")}
        </div>
        <div className="text-sm text-[#66746f]">Node Trie</div>
      </div>
      <div className="text-center">
        <div className="text-2xl font-bold text-[#17231f]">
          {statistics.average_depth.toFixed(2)}
        </div>
        <div className="text-sm text-[#66746f]">Kedalaman Rata-rata</div>
      </div>
      <div className="text-center">
        <div className="text-2xl font-bold text-[#17231f]">
          {statistics.memory_megabytes.toFixed(2)} MB
        </div>
        <div className="text-sm text-[#66746f]">Estimasi Memori</div>
      </div>
    </div>
  );
}