import { NextRequest, NextResponse } from "next/server";
import { getSupabaseAdmin, STORAGE_BUCKET } from "../../lib/supabaseAdmin";

export async function GET(request: NextRequest) {
  try {
    const isAdmin = request.cookies.get("agape-admin")?.value === "granted";
    const hasSiteAccess = request.cookies.get("agape-access")?.value === "granted";
    const requestedKind = request.nextUrl.searchParams.get("kind");

    if (!isAdmin && !hasSiteAccess) {
      return NextResponse.json({ message: "열람 권한이 없습니다." }, { status: 403 });
    }

    const supabase = getSupabaseAdmin();
    let query = supabase
      .from("submissions")
      .select("id, kind, title, name, content, status, created_at, submission_files(id, storage_path, original_name, mime_type, size_bytes)")
      .order("created_at", { ascending: false });
    if (requestedKind) query = query.eq("kind", requestedKind);

    const { data, error } = await query;
    if (error) throw error;

    const submissions = await Promise.all((data ?? []).map(async (submission) => ({
      ...submission,
      submission_files: await Promise.all((submission.submission_files ?? []).map(async (file) => {
        const { data: signed } = await supabase.storage
          .from(STORAGE_BUCKET)
          .createSignedUrl(file.storage_path, 60 * 10);
        return { ...file, downloadUrl: signed?.signedUrl ?? null };
      })),
    })));

    return NextResponse.json({ submissions });
  } catch (error) {
    console.error("submission list failed", error);
    return NextResponse.json({ message: "접수 목록을 불러오지 못했습니다." }, { status: 500 });
  }
}
