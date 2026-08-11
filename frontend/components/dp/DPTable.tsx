type DPTableProps = {
  dp: (number | null)[];
  choices: number[];
  words: string[];
  text: string;
};

export default function DPTable({ dp, choices, words, text }: DPTableProps) {
  if (!dp.length) return null;

  return (
    <div className="dp-table-container p-4 bg-[#f5f8f7] rounded-xl">
      <h4 className="text-sm font-semibold text-[#17231f] mb-2">Array dp[]</h4>
      <div className="dp-array flex flex-wrap gap-1 mb-4">
        {dp.map((val, i) => (
          <div
            key={i}
            className={[
              "dp-cell flex flex-col items-center px-3 py-1 bg-white rounded-lg border border-[#dce8e4] min-w-[44px]",
              i === dp.length - 1 ? "border-[#397f70] bg-[#dff0eb]" : "",
              val === null ? "opacity-50" : "",
            ].join(" ")}
          >
            <span className="dp-index text-[10px] text-[#66746f]">{i}</span>
            <span className="dp-value font-semibold text-sm text-[#17231f]">
              {val === null ? "∞" : val.toFixed(2)}
            </span>
          </div>
        ))}
      </div>

      <h4 className="text-sm font-semibold text-[#17231f] mb-2">Trace-back</h4>
      <div className="traceback-steps space-y-1">
        {words.map((word, idx) => {
          let start = 0;
          for (let k = 0; k < idx; k++) {
            start += words[k].length;
          }
          const end = start + word.length;
          return (
            <div key={idx} className="trace-step flex gap-3 text-sm">
              <span className="step-index text-[#397f70] font-medium">
                dp[{start}] → dp[{end}]
              </span>
              <span className="step-word text-[#17231f]">→ "{word}"</span>
            </div>
          );
        })}
      </div>
    </div>
  );
}