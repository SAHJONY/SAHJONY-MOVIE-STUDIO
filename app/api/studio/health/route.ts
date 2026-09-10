import { NextResponse } from "next/server";

export const runtime = "nodejs";
export const dynamic = "force-dynamic";

export async function GET() {
  const providers = {
    higgsfield: Boolean(process.env.HF_API_KEY && process.env.HF_API_SECRET),
    supabase: Boolean(process.env.SUPABASE_URL && (process.env.SUPABASE_SECRET_KEY || process.env.SUPABASE_SERVICE_ROLE_KEY)),
  };

  return NextResponse.json(
    {
      studio: "SAHJONY Movie OS",
      version: "0.3.0",
      status: "operational",
      providers,
      generatedAt: new Date().toISOString(),
    },
    { headers: { "Cache-Control": "no-store" } },
  );
}
