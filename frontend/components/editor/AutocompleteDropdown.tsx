import type { AutocompleteSuggestion } from "../../types/autocomplete";

type AutocompleteDropdownProps = {
  suggestions: AutocompleteSuggestion[];
  activeIndex: number;
  latencyMs: number | null;
  onSelect: (word: string) => void;
  onHover: (index: number) => void;
};

export default function AutocompleteDropdown({
  suggestions,
  activeIndex,
  latencyMs,
  onSelect,
  onHover,
}: AutocompleteDropdownProps) {
  if (suggestions.length === 0) {
    return null;
  }

  return (
    <div
      className="autocomplete-dropdown dropdown-enter"
      role="listbox"
      aria-label="Autocomplete suggestions"
    >
      <div className="autocomplete-header">
        <span>Autocomplete</span>
        {latencyMs !== null && (
          <span className="autocomplete-latency">
            {latencyMs.toFixed(2)}ms
          </span>
        )}
      </div>

      {suggestions.map((suggestion, index) => (
        <div
          key={suggestion.word}
          role="option"
          aria-selected={index === activeIndex}
          className={
            index === activeIndex
              ? "autocomplete-item autocomplete-item-active"
              : "autocomplete-item"
          }
          onMouseEnter={() => onHover(index)}
          onMouseDown={(event) => {
            event.preventDefault();
            onSelect(suggestion.word);
          }}
        >
          <span>{suggestion.word}</span>
          {index === activeIndex && (
            <span className="autocomplete-key">
              {latencyMs !== null && latencyMs < 50 ? "↵" : "Tab"}
            </span>
          )}
        </div>
      ))}
    </div>
  );
}