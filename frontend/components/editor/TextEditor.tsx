"use client";

import { useCallback, useEffect, useRef, useState } from "react";
import type { KeyboardEvent } from "react";

import { useAutocomplete } from "../../hooks/useAutocomplete";
import { useEditor } from "../../hooks/useEditor";
import { useSpellcheck, type MisspelledWord } from "../../hooks/useSpellcheck";
import { useBigram } from "../../hooks/useBigram";
import { checkWord } from "../../services/spellcheck";
import AutocompleteDropdown from "./AutocompleteDropdown";
import SpellSuggestion from "./SpellSuggestion";
import IssueList from "./IssueList";
import { checkText } from "../../services/spellcheck";
import type { SpellCheckIssueResponse } from "../../types/spellcheck";
import Button from "../common/Button";
import Badge from "../common/Badge";

const WORD_BOUNDARY_REGEX = /[^a-zA-Z0-9\u00C0-\u024F'-]/;

function getWordAtOffset(text: string, offset: number): {
  word: string;
  start: number;
  end: number;
} | null {
  let start = offset;
  while (start > 0 && !WORD_BOUNDARY_REGEX.test(text[start - 1])) {
    start--;
  }
  let end = offset;
  while (end < text.length && !WORD_BOUNDARY_REGEX.test(text[end])) {
    end++;
  }
  const word = text.slice(start, end);
  if (!word) return null;
  return { word, start, end };
}

function escapeHtml(str: string): string {
  return str
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;");
}

export default function TextEditor() {
  const { editorRef, getCaretWordInfo, replaceCurrentWord } = useEditor();
  const {
    misspelled,
    setMisspelled,
    activeSuggestion,
    validateWord,
    clearAll,
    addToDictionary,
    showSuggestions,
    closeSuggestions,
  } = useSpellcheck();

  const {
    enabled: bigramEnabled,
    recordPair,
    rerankSuggestions,
  } = useBigram();

  const [lastWord, setLastWord] = useState<string>("");
  const [caretPosition, setCaretPosition] = useState<{ top: number; left: number; direction: "down" | "up" } | null>(null);
  const [allIssues, setAllIssues] = useState<SpellCheckIssueResponse[]>([]);
  const [isCheckingAll, setIsCheckingAll] = useState(false);
  const containerRef = useRef<HTMLDivElement | null>(null);
  const compositionRef = useRef(false);

  const {
    suggestions,
    activeIndex,
    isOpen,
    latencyMs,
    query,
    clear,
    moveActiveIndex,
    setActiveIndex,
  } = useAutocomplete({
    rerankFn: rerankSuggestions,
    prevWord: lastWord,
    bigramEnabled,
  });

  const updateCaretPosition = useCallback(() => {
    const selection = window.getSelection();
    if (!selection || selection.rangeCount === 0 || !containerRef.current) return;
    const range = selection.getRangeAt(0).cloneRange();
    range.collapse(true);
    const rect = range.getClientRects()[0];
    const containerRect = containerRef.current.getBoundingClientRect();
    if (!rect) return;

    const dropdownHeight = 320;
    const spaceBelow = window.innerHeight - rect.bottom;
    const spaceAbove = rect.top;
    const direction = spaceBelow < dropdownHeight && spaceAbove > dropdownHeight ? "up" : "down";

    setCaretPosition({
      top: direction === "down"
        ? rect.bottom - containerRect.top + 6
        : rect.top - containerRect.top - dropdownHeight - 6,
      left: Math.min(rect.left - containerRect.left, containerRect.width - 220),
      direction,
    });
  }, []);

  const recordPairIfValid = useCallback(
    async (prev: string, curr: string) => {
      if (!bigramEnabled || !prev || !curr) return;
      const response = await checkWord(curr, 2, 1);
      if (response.is_valid) {
        await recordPair(prev, curr);
        setLastWord(curr);
      }
    },
    [bigramEnabled, recordPair]
  );

  const handleInput = useCallback(async () => {
    const wordInfo = getCaretWordInfo();
    updateCaretPosition();

    if (!wordInfo) {
      clear();
      return;
    }

    query(wordInfo.word);

    const editor = editorRef.current;
    if (!editor) return;
    const text = editor.textContent ?? "";
    const caretOffset = getCaretWordInfo()?.wordEnd ?? text.length;

    if (caretOffset > 0 && WORD_BOUNDARY_REGEX.test(text[caretOffset - 1])) {
      const prev = getWordAtOffset(text, caretOffset - 1);
      if (prev) {
        const response = await checkWord(prev.word, 2, 5);
        if (response.is_valid) {
          if (lastWord) {
            await recordPairIfValid(lastWord, prev.word);
          }
          setLastWord(prev.word);
        }
        validateWord(prev.word, prev.start, prev.end);
      }
    }
  }, [
    getCaretWordInfo,
    updateCaretPosition,
    clear,
    query,
    editorRef,
    lastWord,
    recordPairIfValid,
    validateWord,
  ]);

  const selectSuggestion = useCallback(
    (word: string) => {
      const wordInfo = getCaretWordInfo();
      if (!wordInfo) return;
      replaceCurrentWord(wordInfo.wordStart, wordInfo.wordEnd, word);
      clear();
      editorRef.current?.focus();
    },
    [getCaretWordInfo, replaceCurrentWord, clear, editorRef]
  );

  const handleSpellSelect = useCallback(
    async (word: string, start: number, end: number) => {
      replaceCurrentWord(start, end, word);
      if (bigramEnabled && lastWord) {
        await recordPair(lastWord, word);
        setLastWord(word);
      }
      setMisspelled((prev: MisspelledWord[]) =>
        prev.filter((m) => m.start !== start || m.end !== end)
      );
      setAllIssues((prev: SpellCheckIssueResponse[]) =>
        prev.filter((i) => i.start !== start || i.end !== end)
      );
      closeSuggestions();
    },
    [replaceCurrentWord, bigramEnabled, lastWord, recordPair, setMisspelled, closeSuggestions]
  );

  const handleKeyDown = useCallback(
    (event: KeyboardEvent<HTMLDivElement>) => {
      if (compositionRef.current) return;

      if (event.ctrlKey && event.shiftKey && event.key === "C") {
        event.preventDefault();
        handleCheckAll();
        return;
      }

      if (isOpen) {
        if (event.key === "Tab" || event.key === "Enter") {
          const suggestion = suggestions[activeIndex];
          if (suggestion) {
            event.preventDefault();
            selectSuggestion(suggestion.word);
          }
          return;
        }
        if (event.key === "ArrowDown") {
          event.preventDefault();
          moveActiveIndex(1);
          return;
        }
        if (event.key === "ArrowUp") {
          event.preventDefault();
          moveActiveIndex(-1);
          return;
        }
        if (event.key === "Escape") {
          event.preventDefault();
          clear();
          return;
        }
      }

      if (activeSuggestion) {
        if (event.key === "Escape") {
          event.preventDefault();
          closeSuggestions();
          return;
        }
      }

      if (event.key === "Space" && isOpen) {
        clear();
      }
    },
    [
      isOpen,
      suggestions,
      activeIndex,
      selectSuggestion,
      moveActiveIndex,
      clear,
      activeSuggestion,
      closeSuggestions,
    ]
  );

  const handleCompositionStart = useCallback(() => {
    compositionRef.current = true;
  }, []);

  const handleCompositionEnd = useCallback(() => {
    compositionRef.current = false;
    handleInput();
  }, [handleInput]);

  const handleClick = useCallback(
    (e: React.MouseEvent) => {
      const target = e.target as HTMLElement;
      const misspelledSpan = target.closest(".misspelled");
      if (misspelledSpan) {
        const span = misspelledSpan as HTMLElement;
        const word = span.textContent || "";
        const start = parseInt(span.dataset.start || "0", 10);
        const end = parseInt(span.dataset.end || "0", 10);
        const found = misspelled.find((m) => m.start === start && m.end === end);
        if (found && found.suggestions.length > 0) {
          const rect = span.getBoundingClientRect();
          const containerRect = containerRef.current?.getBoundingClientRect();
          if (containerRect) {
            const dropdownHeight = 320;
            const spaceBelow = window.innerHeight - rect.bottom;
            const direction = spaceBelow < dropdownHeight ? "up" : "down";
            showSuggestions(
              found.word,
              found.start,
              found.end,
              found.suggestions,
              {
                top: direction === "down"
                  ? rect.bottom - containerRect.top + 4
                  : rect.top - containerRect.top - dropdownHeight - 4,
                left: rect.left - containerRect.left,
              }
            );
          }
        } else if (found) {
          showSuggestions(
            found.word,
            found.start,
            found.end,
            [],
            { top: 0, left: 0 }
          );
        }
      } else {
        closeSuggestions();
      }
    },
    [misspelled, showSuggestions, closeSuggestions]
  );

  const renderTextWithMarkup = useCallback(() => {
    const editor = editorRef.current;
    if (!editor) return;
    const text = editor.textContent || "";
    if (!text) {
      editor.innerHTML = "";
      return;
    }

    let html = "";
    let lastIndex = 0;
    const sorted = [...misspelled].sort((a, b) => a.start - b.start);

    for (const item of sorted) {
      if (item.start > lastIndex) {
        html += escapeHtml(text.slice(lastIndex, item.start));
      }
      html += `<span class="misspelled" data-start="${item.start}" data-end="${item.end}" title="Klik untuk melihat saran" style="text-decoration: underline wavy red; cursor: pointer;">${escapeHtml(item.word)}</span>`;
      lastIndex = item.end;
    }
    if (lastIndex < text.length) {
      html += escapeHtml(text.slice(lastIndex));
    }

    editor.innerHTML = html;

    const sel = window.getSelection();
    if (sel && sel.rangeCount > 0) {
      const range = sel.getRangeAt(0);
      try {
        const textNodes = editor.querySelectorAll("span, .misspelled");
        let totalLength = 0;
        let targetNode: Node | null = null;
        let targetOffset = 0;

        for (const node of textNodes) {
          const nodeText = node.textContent || "";
          if (totalLength + nodeText.length >= range.startOffset) {
            targetNode = node.firstChild || node;
            targetOffset = range.startOffset - totalLength;
            break;
          }
          totalLength += nodeText.length;
        }

        if (targetNode) {
          const newRange = document.createRange();
          newRange.setStart(targetNode, Math.min(targetOffset, targetNode.textContent?.length || 0));
          newRange.collapse(true);
          sel.removeAllRanges();
          sel.addRange(newRange);
        }
      } catch {
        const newRange = document.createRange();
        newRange.selectNodeContents(editor);
        newRange.collapse(false);
        sel.removeAllRanges();
        sel.addRange(newRange);
      }
    }
  }, [misspelled, editorRef]);

  useEffect(() => {
    renderTextWithMarkup();
  }, [misspelled, renderTextWithMarkup]);

  const handleCheckAll = useCallback(async () => {
    const text = editorRef.current?.textContent || "";
    if (!text.trim()) {
      setAllIssues([]);
      return;
    }

    setIsCheckingAll(true);
    try {
      const response = await checkText(text, 2, 5);
      setAllIssues(response.issues);
      clearAll();
      for (const issue of response.issues) {
        validateWord(issue.word, issue.start, issue.end);
      }
    } catch {
      setAllIssues([]);
    } finally {
      setIsCheckingAll(false);
    }
  }, [editorRef, clearAll, validateWord]);

  const applySuggestionFromIssue = useCallback(
    async (word: string, start: number, end: number) => {
      replaceCurrentWord(start, end, word);
      if (bigramEnabled && lastWord) {
        await recordPair(lastWord, word);
        setLastWord(word);
      }
      setMisspelled((prev: MisspelledWord[]) =>
        prev.filter((m) => m.start !== start || m.end !== end)
      );
      setAllIssues((prev: SpellCheckIssueResponse[]) =>
        prev.filter((i) => i.start !== start || i.end !== end)
      );
    },
    [replaceCurrentWord, bigramEnabled, lastWord, recordPair, setMisspelled]
  );

  return (
    <div className="editor-wrapper" ref={containerRef}>
      <div
        ref={editorRef}
        className="text-editor"
        contentEditable
        suppressContentEditableWarning
        onInput={handleInput}
        onKeyDown={handleKeyDown}
        onCompositionStart={handleCompositionStart}
        onCompositionEnd={handleCompositionEnd}
        onClick={handleClick}
        onBlur={() => setTimeout(closeSuggestions, 200)}
        data-placeholder="Mulai mengetik di sini..."
      />

      {isOpen && caretPosition && (
        <div
          className="autocomplete-anchor dropdown-enter"
          style={{
            top: caretPosition.top,
            left: Math.max(caretPosition.left, 0),
            transformOrigin: caretPosition.direction === "up" ? "bottom" : "top",
          }}
        >
          <AutocompleteDropdown
            suggestions={suggestions}
            activeIndex={activeIndex}
            latencyMs={latencyMs}
            onSelect={selectSuggestion}
            onHover={setActiveIndex}
          />
        </div>
      )}

      {activeSuggestion && (
        <SpellSuggestion
          word={activeSuggestion.word}
          suggestions={activeSuggestion.suggestions}
          position={activeSuggestion.position}
          onSelect={(word) =>
            handleSpellSelect(word, activeSuggestion.start, activeSuggestion.end)
          }
          onAdd={() =>
            addToDictionary(activeSuggestion.word, activeSuggestion.start, activeSuggestion.end)
          }
          onClose={closeSuggestions}
        />
      )}

      <div className="flex flex-wrap items-center gap-3 mt-4">
        <Button
          onClick={handleCheckAll}
          loading={isCheckingAll}
          disabled={isCheckingAll}
        >
          Check All
        </Button>

        {allIssues.length > 0 && (
          <Badge variant="error">{allIssues.length} isu</Badge>
        )}

        {allIssues.length === 0 && !isCheckingAll && (
          <span className="text-sm text-[#66746f]">
            {editorRef.current?.textContent?.trim() ? "✓ Semua kata valid" : "Belum ada teks"}
          </span>
        )}
      </div>

      {allIssues.length > 0 && (
        <div className="mt-4">
          <IssueList
            issues={allIssues}
            onSelectSuggestion={applySuggestionFromIssue}
          />
        </div>
      )}
    </div>
  );
}