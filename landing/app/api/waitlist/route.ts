import { NextResponse } from "next/server";

// Waitlist endpoint with three optional backends:
//   1. Supabase (SUPABASE_URL + SUPABASE_SERVICE_ROLE_KEY) → insert into `waitlist` table
//   2. Resend (RESEND_API_KEY + WAITLIST_FROM_EMAIL) → send confirmation email
//   3. None set → log to Vercel logs + return success
//
// All three use plain fetch — no SDK deps. See landing/WAITLIST_SETUP.md.

const EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

type Payload = {
  email: string;
  persona?: string;
  os?: string;
  tools?: string[];
  monthlySpend?: string;
  planInterest?: string;
  biggestPain?: string;
  referrer?: string;
  utm?: Record<string, string>;
};

type WaitlistRecord = {
  email: string;
  persona: string;
  os: string;
  tools: string[];
  monthly_spend: string;
  plan_interest: string;
  biggest_pain: string;
  referrer: string;
  utm_source: string;
  utm_medium: string;
  utm_campaign: string;
  utm_term: string;
  utm_content: string;
  referred_by: string;
  referral_code: string;
  ts: string;
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
  const s = seed + ":" + Date.now();
  let h = 0;
  for (let i = 0; i < s.length; i++) h = (h * 33 + s.charCodeAt(i)) >>> 0;
  return h.toString(36).slice(0, 8);
}

async function writeToSupabase(record: WaitlistRecord): Promise<{ ok: boolean; error?: string }> {
  const url = process.env.SUPABASE_URL;
  const key = process.env.SUPABASE_SERVICE_ROLE_KEY;
  const table = process.env.SUPABASE_WAITLIST_TABLE || "waitlist";
  if (!url || !key) return { ok: true }; // not configured → no-op
  try {
    const r = await fetch(`${url}/rest/v1/${table}`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "apikey": key,
        "Authorization": `Bearer ${key}`,
        "Prefer": "return=minimal,resolution=ignore-duplicates",
      },
      body: JSON.stringify(record),
    });
    if (!r.ok && r.status !== 409) {
      const text = await r.text().catch(() => "");
      return { ok: false, error: `supabase ${r.status}: ${text.slice(0, 120)}` };
    }
    return { ok: true };
  } catch (e) {
    return { ok: false, error: `supabase fetch: ${(e as Error).message.slice(0, 80)}` };
  }
}

async function sendConfirmationEmail(record: WaitlistRecord): Promise<{ ok: boolean; error?: string }> {
  const apiKey = process.env.RESEND_API_KEY;
  const from = process.env.WAITLIST_FROM_EMAIL || "pulse <hi@mintforai.com>";
  if (!apiKey) return { ok: true }; // not configured → no-op

  const subject = "You're on the pulse waitlist";
  const text = `Thanks for joining the pulse waitlist.

We'll email you twice and never more:
  1. When pulse Pro launches (Q3 2026).
  2. Before any paid tier opens — so you can review terms before paying.

What you can do right now:
  • Download the local app: https://mintforai.com/download
  • Audit ROI math: https://mintforai.com/methodology
  • Read the roadmap: https://mintforai.com/roadmap
  • Star the repo: https://github.com/walight999/pulse

Your referral link:
  https://mintforai.com/?r=${record.referral_code}

— pulse
MIT-licensed local app · operated by White, Bangkok, Thailand
`;

  try {
    const r = await fetch("https://api.resend.com/emails", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${apiKey}`,
      },
      body: JSON.stringify({
        from,
        to: [record.email],
        subject,
        text,
      }),
    });
    if (!r.ok) {
      const text = await r.text().catch(() => "");
      return { ok: false, error: `resend ${r.status}: ${text.slice(0, 120)}` };
    }
    return { ok: true };
  } catch (e) {
    return { ok: false, error: `resend fetch: ${(e as Error).message.slice(0, 80)}` };
  }
}

export async function POST(req: Request) {
  try {
    const body = (await req.json()) as Payload;
    const email = clip(body.email, 254);
    if (!email || !EMAIL_RE.test(email)) {
      return NextResponse.json({ ok: false, error: "invalid_email" }, { status: 400 });
    }

    const code = referralCode(email);
    const utm = body.utm && typeof body.utm === "object" ? body.utm : {};
    const record: WaitlistRecord = {
      email,
      persona:       clip(body.persona, 40),
      os:            clip(body.os, 24),
      tools:         clipArr(body.tools, 16, 40),
      monthly_spend: clip(body.monthlySpend, 24),
      plan_interest: clip(body.planInterest, 24),
      biggest_pain:  clip(body.biggestPain, 64),
      referrer:      clip(body.referrer, 64),
      utm_source:    clip(utm.utm_source, 64),
      utm_medium:    clip(utm.utm_medium, 64),
      utm_campaign:  clip(utm.utm_campaign, 64),
      utm_term:      clip(utm.utm_term, 64),
      utm_content:   clip(utm.utm_content, 64),
      referred_by:   clip(utm.r, 16),
      referral_code: code,
      ts:            new Date().toISOString(),
    };

    // Fan out to optional providers in parallel. Failures of one don't block the others.
    const [supa, resend] = await Promise.all([
      writeToSupabase(record),
      sendConfirmationEmail(record),
    ]);

    // Structured log so failures show up in Vercel logs even when providers aren't configured.
    console.log("[pulse waitlist]", JSON.stringify({
      ...record,
      supabase: supa.ok ? "ok" : supa.error,
      resend:   resend.ok ? "ok" : resend.error,
    }));

    return NextResponse.json({ ok: true, referralCode: code });
  } catch (e) {
    return NextResponse.json({ ok: false, error: "server" }, { status: 500 });
  }
}
