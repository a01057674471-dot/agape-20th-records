import { NextRequest, NextResponse } from "next/server";
import { getSupabaseAdmin, STORAGE_BUCKET } from "../../../lib/supabaseAdmin";

type FileInfo = { name?: string; type?: string; size?: number };
const VALID_KINDS = ["manuscript", "photo", "meeting"] as const;
const MAX_FILES = { manuscript: 1, photo: 10, meeting: 1 };
const MAX_SIZE = { manuscript: 30 * 1024 * 1024, photo: 15 * 1024 * 1024, meeting: 30 * 1024 * 1024 };

function safeFileName(name: string) {
  const extension = name.includes(".") ? `.${name.split(".").pop()?.replace(/[^a-zA-Z0-9]/g, "").slice(0, 8)}` : "";
  return `${crypto.randomUUID()}${extension}`;
}

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    const kind = body.kind as typeof VALID_KINDS[number];
    const title = String(body.title ?? "").trim();
    const name = String(body.name ?? "").trim();
    const content = String(body.content ?? "").trim();
    const files = Array.isArray(body.files) ? body.files as FileInfo[] : [];

    if (!VALID_KINDS.includes(kind) || !title || !name) {
      return NextResponse.json({ message: "제목과 이름을 입력해 주세요." }, { status: 400 });
    }
    if (title.length > 120 || name.length > 60) {
      return NextResponse.json({ message: "제목 또는 이름이 너무 깁니다." }, { status: 400 });
    }
    if (files.length > MAX_FILES[kind]) {
      return NextResponse.json({ message: `파일은 최대 ${MAX_FILES[kind]}개까지 올릴 수 있습니다.` }, { status: 400 });
    }
    if (kind !== "manuscript" && files.length === 0) {
      return NextResponse.json({ message: "올릴 파일을 선택해 주세요." }, { status: 400 });
    }
    if (kind === "manuscript" && !content && files.length === 0) {
      return NextResponse.json({ message: "원고 내용을 쓰거나 파일을 선택해 주세요." }, { status: 400 });
    }
    if (files.some((file) => !file.name || !file.size || file.size > MAX_SIZE[kind])) {
      return NextResponse.json({ message: `파일 한 개의 최대 용량은 ${MAX_SIZE[kind] / 1024 / 1024}MB입니다.` }, { status: 400 });
    }

    const supabase = getSupabaseAdmin();
    const { data: submission, error: insertError } = await supabase
      .from("submissions")
      .insert({ kind, title, name, content: content || null })
      .select("id")
      .single();
    if (insertError || !submission) throw insertError ?? new Error("접수 번호 생성 실패");

    const uploads = [];
    for (const file of files) {
      const path = `${kind}/${submission.id}/${safeFileName(file.name!)}`;
      const { data, error } = await supabase.storage.from(STORAGE_BUCKET).createSignedUploadUrl(path);
      if (error || !data) {
        await supabase.from("submissions").delete().eq("id", submission.id);
        throw error ?? new Error("업로드 권한 생성 실패");
      }
      uploads.push({
        path,
        token: data.token,
        originalName: file.name,
        mimeType: file.type || "application/octet-stream",
        sizeBytes: file.size,
      });
    }

    return NextResponse.json({ submissionId: submission.id, uploads });
  } catch (error) {
    console.error("submission start failed", error);
    return NextResponse.json({ message: "온라인 접수를 시작하지 못했습니다." }, { status: 500 });
  }
}
