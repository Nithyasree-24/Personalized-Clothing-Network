import { NextRequest, NextResponse } from 'next/server';

const BACKEND_URL = 'http://localhost:5000';

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    
    // Forward request to Python backend
    const response = await fetch(`${BACKEND_URL}/ai-tryon/process`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(body),
    });

    if (!response.ok) {
      const errorData = await response.json();
      return NextResponse.json(
        { error: errorData.error || 'Backend processing failed' },
        { status: response.status }
      );
    }

    const result = await response.json();
    return NextResponse.json(result);

  } catch (error) {
    console.error('AI Try-On API error:', error);
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    );
  }
}

export async function GET() {
  try {
    // Get AI model metrics
    const response = await fetch(`${BACKEND_URL}/ai-tryon/metrics`);
    
    if (!response.ok) {
      return NextResponse.json(
        { error: 'Failed to get metrics' },
        { status: response.status }
      );
    }

    const metrics = await response.json();
    return NextResponse.json(metrics);

  } catch (error) {
    console.error('AI Try-On metrics error:', error);
    return NextResponse.json(
      { error: 'Failed to get metrics' },
      { status: 500 }
    );
  }
}