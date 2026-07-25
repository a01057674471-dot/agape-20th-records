import { NextRequest, NextResponse } from "next/server";
import { getSupabaseAdmin, STORAGE_BUCKET } from "../../../lib/supabaseAdmin";
import { verifySubmissionToken } from "../../../lib/submissionToken";

function isAdmin(request: NextRequest) {
  return request.cookies.get("agape-admin")?.value === "granted";
}

export async function PATCH(
  request: NextRequest,
  context: { params: Promise<{ id: string }> },
) {
  const { id } = await context.params;
  const admin = isAdmin(request);
  const author = await verifySubmissionToken(id, request.headers.get("x-submission-token"));
  if (!admin && !author) {
    return NextResponse.json({ message: "이 자료를 수정할 권한이 없습니다." }, { status: 403 });
  }
  const body = await request.json() as {
    status?: string;
    title?: string;
    name?: string;
    content?: string;
  };

  const supabase = getSupabaseAdmin();
  if (admin && body.status) {
    if (!["접수", "검토 중", "완료"].includes(body.status)) {
      return NextResponse.json({ message: "올바른 상태가 아닙니다." }, { status: 400 });
    }
    const { error } = await supabase.from("submissions").update({ status: body.status }).eq("id", id);
    if (error) return NextResponse.json({ message: "상태를 변경하지 못했습니다." }, { status: 500 });
    return NextResponse.json({ ok: true });
  }

  const title = String(body.title ?? "").trim();
  const name = String(body.name ?? "").trim();
  const content = typeof body.content === "string" ? body.content.trim() : undefined;
  if (!title || !name || title.length > 120 || name.length > 60) {
    return NextResponse.json({ message: "제목과 이름을 올바르게 입력해 주세요." }, { status: 400 });
  }
  const changes: { title: string; name: string; content?: string | null } = { title, name };
  if (content !== undefined) changes.content = content || null;
  const { error } = await supabase.from("submissions").update(changes).eq("id", id);
  if (error) return NextResponse.json({ message: "자료를 수정하지 못했습니다." }, { status: 500 });
  return NextResponse.json({ ok: true });
}

export async function DELETE(
  request: NextRequest,
  context: { params: Promise<{ id: string }> },
) {
  const { id } = await context.params;
  const admin = isAdmin(request);
  const author = await verifySubmissionToken(id, request.headers.get("x-submission-token"));
  if (!admin && !author) {
    return NextResponse.json({ message: "이 자료를 삭제할 권한이 없습니다." }, { status: 403 });
  }
  const supabase = getSupabaseAdmin();
  const { data: files } = await supabase
    .from("submission_files")
    .select("storage_path")
    .eq("submission_id", id);

  const paths = (files ?? []).map((file) => file.storage_path);
  if (paths.length) await supabase.storage.from(STORAGE_BUCKET).remove(paths);
  const { error } = await supabase.from("submissions").delete().eq("id", id);
  if (error) return NextResponse.json({ message: "자료를 삭제하지 못했습니다." }, { status: 500 });
  return NextResponse.json({ ok: true });
}
