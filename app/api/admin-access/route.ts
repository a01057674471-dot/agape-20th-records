import { NextRequest, NextResponse } from "next/server";

export async function POST(request: NextRequest) {
  const { password } = (await request.json()) as { password?: string };
  const adminPassword = process.env.ADMIN_PASSWORD ?? "2222";

  if (password !== adminPassword) {
    return NextResponse.json(
      { ok: false, message: "관리자 비밀번호가 맞지 않습니다." },
      { status: 401 },
    );
  }

  const response = NextResponse.json({ ok: true });
  response.cookies.set("agape-admin", "granted", {
    httpOnly: true,
    sameSite: "lax",
    secure: process.env.NODE_ENV === "production",
    maxAge: 60 * 60 * 12,
    path: "/",
  });
  return response;
}
