"use client";

import { createClient } from "@supabase/supabase-js";

export type SubmissionKind = "manuscript" | "photo" | "meeting";

type UploadTicket = {
  path: string;
  token: string;
  originalName: string;
  mimeType: string;
  sizeBytes: number;
};

type SubmitInput = {
  kind: SubmissionKind;
  title: string;
  name: string;
  content?: string;
  files: File[];
};

export async function uploadSubmission(input: SubmitInput) {
  const startResponse = await fetch("/api/submissions/start", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      kind: input.kind,
      title: input.title,
      name: input.name,
      content: input.content,
      files: input.files.map((file) => ({
        name: file.name,
        type: file.type || "application/octet-stream",
        size: file.size,
      })),
    }),
  });

  const startData = await startResponse.json();
  if (!startResponse.ok) throw new Error(startData.message || "접수를 시작하지 못했습니다.");

  const url = process.env.NEXT_PUBLIC_SUPABASE_URL;
  const anonKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY;
  if (!url || !anonKey) throw new Error("온라인 저장소 연결 정보가 없습니다.");

  const supabase = createClient(url, anonKey, {
    auth: { autoRefreshToken: false, persistSession: false },
  });

  for (let index = 0; index < startData.uploads.length; index += 1) {
    const ticket = startData.uploads[index] as UploadTicket;
    const file = input.files[index];
    const { error } = await supabase.storage
      .from("agape-records")
      .uploadToSignedUrl(ticket.path, ticket.token, file, {
        contentType: ticket.mimeType,
      });
    if (error) throw new Error(`${file.name} 업로드에 실패했습니다.`);
  }

  const completeResponse = await fetch("/api/submissions/complete", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      submissionId: startData.submissionId,
      files: startData.uploads,
    }),
  });
  const completeData = await completeResponse.json();
  if (!completeResponse.ok) throw new Error(completeData.message || "접수를 완료하지 못했습니다.");

  return completeData;
}
