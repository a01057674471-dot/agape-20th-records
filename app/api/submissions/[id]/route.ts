import { NextRequest, NextResponse } from "next/server";
import { getSupabaseAdmin, STORAGE_BUCKET } from "../../../lib/supabaseAdmin";

function isAdmin(request: NextRequest) {
  return request.cookies.get("agape-admin")?.value === "granted";
}

export async function PATCH(
  request: NextRequest,
  context: { params: Promise<{ id: string }> },
) {
  if (!isAdmin(request)) {
    return NextResponse.json({ message: "관리자 권한이 필요합니다." }, { status: 403 });
  }
  const { id } = await context.params;
  const { status } = await request.json() as { status?: string };
  if (!["접수", "검토 중", "완료"].includes(status ?? "")) {
    return NextResponse.json({ message: "올바른 상태가 아닙니다." }, { status: 400 });
  }

  const supabase = getSupabaseAdmin();
  const { error } = await supabase.from("submissions").update({ status }).eq("id", id);
  if (error) return NextResponse.json({ message: "상태를 변경하지 못했습니다." }, { status: 500 });
  return NextResponse.json({ ok: true });
}

export async function DELETE(
  request: NextRequest,
  context: { params: Promise<{ id: string }> },
) {
  if (!isAdmin(request)) {
    return NextResponse.json({ message: "관리자 권한이 필요합니다." }, { status: 403 });
  }
  const { id } = await context.params;
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
