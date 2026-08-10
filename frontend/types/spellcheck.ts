export type SpellCheckCandidateResponse = {
  word: string;
  distance: number;
  frequency: number;
};

export type SpellCheckWordResponse = {
  word: string;
  is_valid: boolean;
  suggestions: SpellCheckCandidateResponse[];
};

export type SpellCheckIssueResponse = {
  word: string;
  start: number;
  end: number;
  suggestions: SpellCheckCandidateResponse[];
};

export type SpellCheckTextResponse = {
  issues: SpellCheckIssueResponse[];
  issue_count: number;
};