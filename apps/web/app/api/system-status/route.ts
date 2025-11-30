import { NextResponse } from 'next/server'

const DEFAULT_BASE = 'http://localhost:8000'
const API_BASE = (process.env.NEXT_PUBLIC_API_BASE || DEFAULT_BASE).replace(/\/$/, '')

export async function GET() {
  try {
    const upstream = await fetch(`${API_BASE}/api/system-status`, {
      headers: { Accept: 'application/json' },
      cache: 'no-store',
    })

    if (!upstream.ok) {
      const body = await upstream.text()
      throw new Error(`Upstream ${API_BASE}/api/system-status responded ${upstream.status}: ${body}`)
    }

    const payload = await upstream.json()
    return NextResponse.json({ success: true, data: payload })
  } catch (error: unknown) {
    console.error('[system-status] using fallback payload:', error)
    const fallback = {
      core_services: 'Degraded',
      network: 'Disconnected',
      maintenance: 'Offline',
      data_integrity: 'Unverified',
      timestamp: new Date().toISOString(),
    }
    return NextResponse.json({ success: false, data: fallback }, { status: 200 })
  }
}
