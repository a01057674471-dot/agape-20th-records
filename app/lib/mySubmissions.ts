"use client";

const STORAGE_KEY = "agape-my-submissions";

type SavedTokens = Record<string, string>;

function readTokens(): SavedTokens {
  if (typeof window === "undefined") return {};
  try {
    return JSON.parse(window.localStorage.getItem(STORAGE_KEY) ?? "{}") as SavedTokens;
  } catch {
    return {};
  }
}

export function saveSubmissionToken(id: string, token: string) {
  const tokens = readTokens();
  tokens[id] = token;
  window.localStorage.setItem(STORAGE_KEY, JSON.stringify(tokens));
}

export function getSubmissionToken(id: string) {
  return readTokens()[id] ?? null;
}

export function removeSubmissionToken(id: string) {
  const tokens = readTokens();
  delete tokens[id];
  window.localStorage.setItem(STORAGE_KEY, JSON.stringify(tokens));
}
