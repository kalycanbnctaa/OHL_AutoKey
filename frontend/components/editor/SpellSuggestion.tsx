import type { SpellCheckCandidateResponse } from "../../types/spellcheck";

type SpellSuggestionProps = {
  word: string;
  suggestions: SpellCheckCandidateResponse[];
  onSelect: (word: string) => void;
  onAdd: () => void;
  onClose: () => void;
  position: { top: number; left: number };
};

export default function SpellSuggestion({
  word,
  suggestions,
  onSelect,
  onAdd,
  onClose,
  position,
}: SpellSuggestionProps) {
  return (
    <div
      className="autocomplete-dropdown dropdown-enter"
      style={{
        position: "absolute",
        top: position.top,
        left: Math.max(position.left, 0),
        minWidth: 220,
        maxWidth: 320,
        transformOrigin: "top",
      }}
      role="menu"
    >
      <div className="autocomplete-header">
        <span>Saran untuk "{word}"</span>
      </div>

      {suggestions.length === 0 ? (
        <div className="autocomplete-item" style={{ color: "#66746f", fontSize: "13px" }}>
          <span>Tidak ada saran</span>
        </div>
      ) : (
        suggestions.map((s) => (
          <div
            key={s.word}
            className="autocomplete-item"
            onMouseDown={(e) => {
              e.preventDefault();
              onSelect(s.word);
            }}
          >
            <span>{s.word}</span>
            <span className="autocomplete-key">dist {s.distance}</span>
          </div>
        ))
      )}

      <div
        className="autocomplete-item"
        style={{ borderTop: "1px solid var(--border)" }}
        onMouseDown={(e) => {
          e.preventDefault();
          onAdd();
        }}
      >
        <span style={{ color: "#397f70" }}>➕ Tambahkan ke kamus</span>
      </div>

      <div
        className="autocomplete-item"
        onMouseDown={(e) => {
          e.preventDefault();
          onClose();
        }}
      >
        <span style={{ color: "#66746f" }}>✕ Tutup</span>
      </div>
    </div>
  );
}