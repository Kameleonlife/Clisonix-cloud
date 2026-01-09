import { NextResponse } from 'next/server'

const API_BASE = process.env.NEXT_PUBLIC_API_BASE || 'http://localhost:8000'

export async function GET() {
  try {
    const upstream = await fetch(`${API_BASE}/api/weather`, {
      headers: { Accept: 'application/json' },
      cache: 'no-store',
    })

    if (!upstream.ok) {
      throw new Error(`Upstream responded with ${upstream.status}`)
    }

    const payload = await upstream.json()
    return NextResponse.json({ success: true, data: payload })
  } catch (error) {
    console.error('[weather] fallback engaged:', error)
    const fallback = {
      temperature: 22,
      humidity: 65,
      condition: 'Cloudy',
      location: 'Local',
      timestamp: new Date().toISOString(),
    }
    return NextResponse.json({ success: false, data: fallback }, { status: 200 })
  }
}