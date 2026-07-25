import { NextRequest, NextResponse } from "next/server";

const PUBLIC_PATHS = ["/access", "/api/access", "/admin-access", "/api/admin-access"];

export function middleware(request: NextRequest) {
  const { pathname } = request.nextUrl;
  const isPublic =
    PUBLIC_PATHS.some((path) => pathname.startsWith(path)) ||
    pathname.startsWith("/_next") ||
    pathname === "/favicon.ico";

  if (isPublic) {
    return NextResponse.next();
  }

  if (pathname.startsWith("/admin")) {
    if (request.cookies.get("agape-admin")?.value === "granted") {
      return NextResponse.next();
    }

    const adminAccessUrl = new URL("/admin-access", request.url);
    adminAccessUrl.searchParams.set("next", pathname);
    return NextResponse.redirect(adminAccessUrl);
  }

  if (request.cookies.get("agape-access")?.value === "granted") {
    return NextResponse.next();
  }

  const accessUrl = new URL("/access", request.url);
  accessUrl.searchParams.set("next", pathname);
  return NextResponse.redirect(accessUrl);
}

export const config = {
  matcher: ["/((?!.*\\..*).*)"],
};
