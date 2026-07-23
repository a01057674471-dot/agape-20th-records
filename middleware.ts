import { NextRequest, NextResponse } from 'next/server';

const publicPaths = ['/login', '/api/auth', '/api/admin-auth', '/favicon.ico'];

export function middleware(request: NextRequest) {
  const { pathname } = request.nextUrl;
  if (publicPaths.some((path) => pathname.startsWith(path)) || pathname.startsWith('/_next')) {
    return NextResponse.next();
  }

  const siteToken = process.env.SITE_ACCESS_TOKEN || 'dev-site-token';
  const adminToken = process.env.ADMIN_ACCESS_TOKEN || 'dev-admin-token';
  const hasSiteAccess = request.cookies.get('agape_site_access')?.value === siteToken;
  const hasAdminAccess = request.cookies.get('agape_admin_access')?.value === adminToken;

  if (!hasSiteAccess) {
    const url = request.nextUrl.clone();
    url.pathname = '/login';
    return NextResponse.redirect(url);
  }

  if (pathname.startsWith('/admin') && pathname !== '/admin/login' && !hasAdminAccess) {
    const url = request.nextUrl.clone();
    url.pathname = '/admin/login';
    return NextResponse.redirect(url);
  }

  return NextResponse.next();
}

export const config = { matcher: ['/((?!_next/static|_next/image).*)'] };
