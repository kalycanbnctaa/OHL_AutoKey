"use client";

import type { ReactNode } from "react";
import Tabs from "../common/Tabs";

const mainTabs = [
  { id: "editor", label: "Editor", icon: "✏️" },
  { id: "auto-space", label: "Auto-Space", icon: "🔤" },
  { id: "smart-trim", label: "Smart Trim", icon: "✂️" },
  { id: "levenshtein", label: "Levenshtein", icon: "📊" },
  { id: "bigram", label: "Bigram", icon: "🧠" },
];

type MainLayoutProps = {
  children: ReactNode[];
};

export default function MainLayout({ children }: MainLayoutProps) {
  return <Tabs tabs={mainTabs}>{children}</Tabs>;
}