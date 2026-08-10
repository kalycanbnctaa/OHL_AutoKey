import { useCallback, useRef } from "react";

import type { CaretWordInfo } from "../types/editor";

const WORD_BOUNDARY_REGEX = /[^a-zA-Z0-9\u00C0-\u024F'-]/;

function isWordChar(char: string): boolean {
  return !WORD_BOUNDARY_REGEX.test(char);
}

export function useEditor() {
  const editorRef = useRef<HTMLDivElement | null>(null);

  const getCaretOffset = useCallback((): number => {
    const editor = editorRef.current;
    const selection = window.getSelection();

    if (!editor || !selection || selection.rangeCount === 0) {
      return 0;
    }

    const range = selection.getRangeAt(0);
    const preCaretRange = range.cloneRange();
    preCaretRange.selectNodeContents(editor);
    preCaretRange.setEnd(range.endContainer, range.endOffset);

    return preCaretRange.toString().length;
  }, []);

  const setCaretOffset = useCallback((offset: number) => {
    const editor = editorRef.current;
    const selection = window.getSelection();

    if (!editor || !selection) {
      return;
    }

    const walker = document.createTreeWalker(editor, NodeFilter.SHOW_TEXT);

    let remaining = offset;
    let node = walker.nextNode();
    let targetNode: Node = editor;
    let targetOffset = 0;

    while (node) {
      const length = node.textContent?.length ?? 0;

      if (remaining <= length) {
        targetNode = node;
        targetOffset = remaining;
        break;
      }

      remaining -= length;
      targetNode = node;
      targetOffset = length;
      node = walker.nextNode();
    }

    const range = document.createRange();
    range.setStart(targetNode, targetOffset);
    range.collapse(true);

    selection.removeAllRanges();
    selection.addRange(range);
  }, []);

  const getCaretWordInfo = useCallback((): CaretWordInfo | null => {
    const editor = editorRef.current;

    if (!editor) {
      return null;
    }

    const fullText = editor.textContent ?? "";
    const caretOffset = getCaretOffset();

    let wordStart = caretOffset;

    while (wordStart > 0 && isWordChar(fullText[wordStart - 1])) {
      wordStart -= 1;
    }

    const word = fullText.slice(wordStart, caretOffset);

    if (!word) {
      return null;
    }

    return { word, wordStart, wordEnd: caretOffset, fullText };
  }, [getCaretOffset]);

  const replaceCurrentWord = useCallback(
    (wordStart: number, wordEnd: number, replacement: string) => {
      const editor = editorRef.current;

      if (!editor) {
        return;
      }

      const fullText = editor.textContent ?? "";
      const rest = fullText.slice(wordEnd);
      const needsSpace = rest.length === 0 || !rest.startsWith(" ");

      const newText =
        fullText.slice(0, wordStart) +
        replacement +
        (needsSpace ? " " : "") +
        rest;

      editor.textContent = newText;

      setCaretOffset(wordStart + replacement.length + (needsSpace ? 1 : 0));
    },
    [setCaretOffset],
  );

  return { editorRef, getCaretWordInfo, replaceCurrentWord };
}