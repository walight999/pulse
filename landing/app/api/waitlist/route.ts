import { NextResponse } from "next/server";

// Minimal waitlist endpoint. Replace with Supabase / Resend / ConvertKit when ready.
// For now: log to Vercel logs + return success with a referral code.

const EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

// Optional segmentation fields — all strings or string-arrays, all bounded length.
type Payload = {
  email: string;
  persona?: string;
  os?: string;
  tools?: string[];
  monthlySpend?: string;
  planInterest?: string;
  biggestPain?: string;
  referrer?: string;
};

function clip(v: unknown, max: number): string {
  if (typeof v !== "string") return "";
  return v.slice(0, max).replace(/[\x00-\x1F\x7F]/g, "");
}

function clipArr(v: unknown, maxLen: number, maxItem: number): string[] {
  if (!Array.isArray(v)) return [];
  return v.slice(0, maxLen).map((x) => clip(x, maxItem)).filter(Boolean);
}

function referralCode(seed: string): string {
  // Tiny non-crypto code derived from email + timestamp. Not for auth; just a pretty share link.
  const s = seed + ":" + Date.now();
  let h = 0;
  for (let i = 0; i < s.length; i++) h = (h * 33 + s.charCodeAt(i)) >>> 0;
  return h.toString(36).slice(0, 8);
}

export async function POST(req: Request) {
  try {
    const body = (await req.json()) as Payload;
    const email = clip(body.email, 254);
    if (!email || !EMAIL_RE.test(email)) {
      return NextResponse.json({ ok: false, error: "invalid_email" }, { status: 400 });
    }

    const record = {
      email,
      persona:       clip(body.persona, 40),
      os:            clip(body.os, 24),
      tools:         clipArr(body.tools, 16, 40),
      monthlySpend:  clip(body.monthlySpend, 24),
      planInterest:  clip(body.planInterest, 24),
      biggestPain:   clip(body.biggestPain, 64),
      referrer:      clip(body.referrer, 64),
      ts:            new Date().toISOString(),
    };

    // TODO: write to Supabase waitlist table when cloud lands. For now: structured log.
    console.log("[pulse waitlist]", JSON.stringify(record));

    return NextResponse.json({
      ok: true,
      referralCode: referralCode(email),
    });
  } catch (e) {
    return NextResponse.json({ ok: false, error: "server" }, { status: 500 });
  }
}
