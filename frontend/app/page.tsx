"use client";

import { useEffect, useState } from "react";

import Header from "../components/layout/Header";
import SummaryPanel from "../components/layout/SummaryPanel";
import MainLayout from "../components/layout/MainLayout";
import TextEditor from "../components/editor/TextEditor";
import AutoSpacePanel from "../components/features/AutoSpacePanel";
import SmartTrimPanel from "../components/features/SmartTrimPanel";
import LevenshteinPanel from "../components/features/LevenshteinPanel";
import BigramPanel from "../components/features/BigramPanel";
import Loading from "../components/common/Loading";
import Button from "../components/common/Button";

type TrieStatistics = {
  word_count: number;
  node_count: number;
  average_depth: number;
  memory_bytes: number;
  memory_megabytes: number;
};

type BackendStatus = "checking" | "connected" | "disconnected";

export default function Home() {
  const [statistics, setStatistics] = useState<TrieStatistics | null>(null);
  const [backendStatus, setBackendStatus] = useState<BackendStatus>("checking");
  const [retryCount, setRetryCount] = useState(0);

  const loadStatistics = async () => {
    const apiUrl = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";
    const controller = new AbortController();

    try {
      const response = await fetch(`${apiUrl}/statistics`, {
        signal: controller.signal,
        cache: "no-store",
      });

      if (!response.ok) {
        throw new Error("Unable to load statistics");
      }

      const data = (await response.json()) as TrieStatistics;
      setStatistics(data);
      setBackendStatus("connected");
    } catch (error) {
      if (error instanceof DOMException && error.name === "AbortError") {
        return;
      }
      setStatistics(null);
      setBackendStatus("disconnected");
    }

    return () => {
      controller.abort();
    };
  };

  useEffect(() => {
    loadStatistics();
  }, [retryCount]);

  const handleRetry = () => {
    setRetryCount((prev) => prev + 1);
  };

  return (
    <>
      <Header statistics={statistics} backendStatus={backendStatus} />

      {backendStatus === "checking" && (
        <div className="py-12">
          <Loading label="Memuat kamus..." />
        </div>
      )}

      {backendStatus === "disconnected" && (
        <div className="py-12 text-center">
          <div className="mb-4 text-4xl">🔌</div>
          <h2 className="text-xl font-semibold text-[#17231f] mb-2">
            Gagal terhubung ke server
          </h2>
          <p className="text-[#66746f] mb-6">
            Pastikan backend berjalan di{" "}
            <code className="bg-[#eef5f2] px-2 py-1 rounded">
              http://localhost:8000
            </code>
          </p>
          <Button onClick={handleRetry}>Coba Lagi</Button>
        </div>
      )}

      {backendStatus === "connected" && statistics && (
        <>
          <SummaryPanel statistics={statistics} backendStatus={backendStatus} />

          <div className="mt-6">
            <MainLayout>
              <TextEditor />
              <AutoSpacePanel />
              <SmartTrimPanel />
              <LevenshteinPanel />
              <BigramPanel />
            </MainLayout>
          </div>

          <footer className="footer">
            <span>AutoKey</span>
            <span>Sprint 8 · Full Integration</span>
          </footer>
        </>
      )}
    </>
  );
}