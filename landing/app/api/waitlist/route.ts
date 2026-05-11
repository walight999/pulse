import { NextResponse } from "next/server";

// Minimal waitlist endpoint. Replace with Supabase / Resend / ConvertKit when ready.
// For now: log to Vercel logs + return success.

export async function POST(req: Request) {
  try {
    const { email } = await req.json();
    if (!email || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
      return NextResponse.json({ ok: false, error: "invalid_email" }, { status: 400 });
    }
    // TODO: send to Supabase waitlist table or 3rd-party email provider
    console.log("[pulse waitlist]", email, new Date().toISOString());
    return NextResponse.json({ ok: true });
  } catch (e) {
    return NextResponse.json({ ok: false, error: "server" }, { status: 500 });
  }
}
