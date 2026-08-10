import type { SpellCheckIssueResponse } from "../../types/spellcheck";

type IssueListProps = {
  issues: SpellCheckIssueResponse[];
  onSelectSuggestion: (word: string, start: number, end: number) => void;
};

export default function IssueList({ issues, onSelectSuggestion }: IssueListProps) {
  if (issues.length === 0) {
    return (
      <div className="summary-empty">
        <p className="text-[#66746f]">Tidak ada isu yang ditemukan.</p>
      </div>
    );
  }

  return (
    <div className="summary-panel">
      <h3 className="text-base font-semibold text-[#17231f]">Ringkasan</h3>
      <p className="issue-count text-sm text-[#66746f] mb-3">
        {issues.length} isu
      </p>

      <div className="space-y-3">
        {issues.map((issue) => (
          <div
            key={`${issue.start}-${issue.end}`}
            className="issue-item pb-3 border-b border-[#eef5f2] last:border-0"
          >
            <div className="issue-word font-medium text-[#bd5b5b]">
              {issue.word}
            </div>
            <div className="issue-suggestions flex flex-wrap gap-2 mt-1">
              {issue.suggestions.slice(0, 5).map((s) => (
                <span
                  key={s.word}
                  className="suggestion-tag cursor-pointer px-3 py-1 bg-[#eef5f2] rounded-full text-sm text-[#397f70] hover:bg-[#397f70] hover:text-white transition-colors"
                  onMouseDown={(e) => {
                    e.preventDefault();
                    onSelectSuggestion(s.word, issue.start, issue.end);
                  }}
                >
                  {s.word}
                </span>
              ))}
              {issue.suggestions.length === 0 && (
                <span className="text-sm text-[#66746f]">Tidak ada saran</span>
              )}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}