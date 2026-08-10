type TrieStatistics = {
  word_count: number;
  node_count: number;
  average_depth: number;
  memory_megabytes: number;
};

type BackendStatus = "checking" | "connected" | "disconnected";

type HeaderProps = {
  statistics: TrieStatistics | null;
  backendStatus: BackendStatus;
};

const statusContent: Record<
  BackendStatus,
  {
    label: string;
    className: string;
  }
> = {
  checking: {
    label: "Loading dictionary...",
    className: "status-checking",
  },
  connected: {
    label: "Dictionary loaded",
    className: "status-connected",
  },
  disconnected: {
    label: "Backend unavailable",
    className: "status-disconnected",
  },
};

export default function Header({
  statistics,
  backendStatus,
}: HeaderProps) {
  const status = statusContent[backendStatus];

  return (
    <header className="header">
      <div className="brand">
        <div className="brand-icon">A</div>

        <div>
          <h1>AutoKey</h1>

          <p>
            {statistics
              ? `${statistics.word_count.toLocaleString(
                  "id-ID",
                )} kata · ${statistics.node_count.toLocaleString(
                  "id-ID",
                )} node trie · ${statistics.average_depth.toFixed(
                  2,
                )} depth · ${statistics.memory_megabytes.toFixed(2)} MB`
              : "Loading dictionary statistics..."}
          </p>
        </div>
      </div>

      <div className={`status ${status.className}`}>
        <span className="status-dot" />
        {status.label}
      </div>
    </header>
  );
}