export type SegmentRequest = {
  text: string;
};

export type SegmentResponse = {
  text: string;
  dp: number[];
  choices: number[];
  words: string[];
  result: string;
  cost: number;
  success: boolean;
  error: string | null;
};