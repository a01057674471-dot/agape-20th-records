import { NextRequest, NextResponse } from "next/server";
import { getSupabaseAdmin } from "../../../lib/supabaseAdmin";

type CompletedFile = {
  path?: string;
  originalName?: string;
  mimeType?: string;
  sizeBytes?: number;
};

export async function POST(request: NextRequest) {
  try {
    const { submissionId, files } = await request.json() as {
      submissionId?: string;
      files?: CompletedFile[];
    };
    if (!submissionId || !Array.isArray(files)) {
      return NextResponse.json({ message: "잘못된 접수 정보입니다." }, { status: 400 });
    }

    const supabase = getSupabaseAdmin();
    const { data: submission } = await supabase
      .from("submissions")
      .select("id, kind")
      .eq("id", submissionId)
      .single();
    if (!submission) return NextResponse.json({ message: "접수 내역을 찾을 수 없습니다." }, { status: 404 });

    const prefix = `${submission.kind}/${submission.id}/`;
    if (files.some((file) => !file.path?.startsWith(prefix) || !file.originalName || !file.sizeBytes)) {
      return NextResponse.json({ message: "파일 정보가 올바르지 않습니다." }, { status: 400 });
    }

    if (files.length > 0) {
      const { error } = await supabase.from("submission_files").insert(files.map((file) => ({
        submission_id: submission.id,
        storage_path: file.path,
        original_name: file.originalName,
        mime_type: file.mimeType || "application/octet-stream",
        size_bytes: file.sizeBytes,
      })));
      if (error) throw error;
    }

    return NextResponse.json({ ok: true, submissionId });
  } catch (error) {
    console.error("submission complete failed", error);
    return NextResponse.json({ message: "온라인 접수를 완료하지 못했습니다." }, { status: 500 });
  }
}
