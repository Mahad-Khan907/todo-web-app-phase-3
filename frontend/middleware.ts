import { NextRequest, NextResponse } from 'next/server';

// Protect dashboard and other authenticated routes
export function middleware(request: NextRequest) {
  // Get the token from cookies
  const token = request.cookies.get('access_token')?.value;

  // Define protected routes
  const protectedRoutes = ['/dashboard', '/api/tasks'];

  // Check if the current path matches a protected route
  const isProtectedRoute = protectedRoutes.some(route =>
    request.nextUrl.pathname.startsWith(route)
  );

  // If trying to access a protected route without a token, redirect to login
  if (isProtectedRoute && !token) {
    // Store the attempted URL for redirect after login
    const requestedUrl = request.url;
    const loginUrl = new URL('/login', request.url);
    loginUrl.searchParams.set('callbackUrl', requestedUrl);

    return NextResponse.redirect(loginUrl);
  }

  // If user is logged in and tries to access login/register pages, redirect to dashboard
  const authRoutes = ['/login', '/register'];
  const isAuthRoute = authRoutes.some(route =>
    request.nextUrl.pathname.startsWith(route)
  );

  if (isAuthRoute && token) {
    const dashboardUrl = new URL('/dashboard', request.url);
    return NextResponse.redirect(dashboardUrl);
  }

  return NextResponse.next();
}

// Apply middleware to specific paths
export const config = {
  matcher: [
    /*
     * Match all request paths except for the ones starting with:
     * - api (API routes)
     * - _next/static (static files)
     * - _next/image (image optimization files)
     * - favicon.ico (favicon file)
     */
    '/dashboard/:path*',
    '/login',
    '/register',
    '/api/tasks/:path*',
  ],
};