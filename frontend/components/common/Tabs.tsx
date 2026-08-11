"use client";

import { useState } from "react";
import type { ReactNode } from "react";

type Tab = {
  id: string;
  label: string;
  icon?: ReactNode;
};

type TabsProps = {
  tabs: Tab[];
  children: ReactNode[];
  defaultTab?: string;
  onTabChange?: (tabId: string) => void;
};

export default function Tabs({
  tabs,
  children,
  defaultTab,
  onTabChange,
}: TabsProps) {
  const [activeTab, setActiveTab] = useState(defaultTab || tabs[0]?.id || "");

  const handleTabChange = (tabId: string) => {
    setActiveTab(tabId);
    if (onTabChange) {
      onTabChange(tabId);
    }
  };

  const activeIndex = tabs.findIndex((tab) => tab.id === activeTab);

  return (
    <div className="w-full">
      <div className="flex gap-1 border-b border-[#dce8e4] mb-6 overflow-x-auto scrollbar-thin">
        {tabs.map((tab) => (
          <button
            key={tab.id}
            onClick={() => handleTabChange(tab.id)}
            className={[
              "flex items-center gap-2 px-3 py-2 text-sm font-medium transition-all duration-200 border-b-2 -mb-px whitespace-nowrap",
              "sm:px-4 sm:py-2.5",
              activeTab === tab.id
                ? "border-[#397f70] text-[#397f70]"
                : "border-transparent text-[#66746f] hover:text-[#17231f] hover:border-[#dce8e4]",
            ].join(" ")}
          >
            {tab.icon && <span className="text-base">{tab.icon}</span>}
            {tab.label}
          </button>
        ))}
      </div>
      <div className="min-h-[200px]">
        {children[activeIndex] || children[0]}
      </div>
    </div>
  );
}