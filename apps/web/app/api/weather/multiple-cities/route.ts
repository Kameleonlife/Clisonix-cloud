import { NextResponse } from 'next/server'

const API_BASE = process.env.NEXT_PUBLIC_API_BASE || 'http://localhost:8000'

export async function GET() {
  try {
    const upstream = await fetch(`${API_BASE}/api/weather/multiple-cities`, {
      headers: { Accept: 'application/json' },
      cache: 'no-store',
    })

    if (!upstream.ok) {
      throw new Error(`Upstream responded with ${upstream.status}`)
    }

    const payload = await upstream.json()
    return NextResponse.json({ success: true, data: payload })
  } catch (error) {
    console.error('[weather/multiple-cities] fallback engaged:', error)
    const fallback = [
      { city: 'New York', temperature: 18, condition: 'Rainy' },
      { city: 'London', temperature: 12, condition: 'Cloudy' },
      { city: 'Tokyo', temperature: 25, condition: 'Sunny' },
    ]
    return NextResponse.json({ success: false, data: fallback }, { status: 200 })
  }
}