import { NextRequest, NextResponse } from 'next/server';

const BACKEND_URL = 'http://localhost:5000';

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    
    // Forward training data to Python backend
    const response = await fetch(`${BACKEND_URL}/ai-tryon/train`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(body),
    });

    if (!response.ok) {
      const errorData = await response.json();
      return NextResponse.json(
        { error: errorData.error || 'Training failed' },
        { status: response.status }
      );
    }

    const result = await response.json();
    return NextResponse.json(result);

  } catch (error) {
    console.error('AI Training API error:', error);
    return NextResponse.json(
      { error: 'Training request failed' },
      { status: 500 }
    );
  }
}