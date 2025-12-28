const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:5000/api';

export interface SignupData {
  name: string;
  email: string;
  password: string;
}

export interface LoginData {
  email: string;
  password: string;
}

export interface AuthResponse {
  message: string;
  token: string;
  user: {
    id: number;
    name: string;
    email: string;
  };
}

// Signup API call
export async function signup(data: SignupData): Promise<AuthResponse> {
  const response = await fetch(`${API_URL}/signup`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(data),
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.error || 'Signup failed');
  }

  return response.json();
}

// Login API call
export async function login(data: LoginData): Promise<AuthResponse> {
  const response = await fetch(`${API_URL}/login`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(data),
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.error || 'Login failed');
  }

  return response.json();
}

// Verify token
export async function verifyToken(token: string): Promise<boolean> {
  try {
    const response = await fetch(`${API_URL}/verify`, {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${token}`,
      },
    });

    if (response.ok) {
      const data = await response.json();
      return data.valid;
    }
    return false;
  } catch (error) {
    return false;
  }
}

// Get user details
export async function getUser(userId: number, token: string) {
  const response = await fetch(`${API_URL}/user/${userId}`, {
    method: 'GET',
    headers: {
      'Authorization': `Bearer ${token}`,
    },
  });

  if (!response.ok) {
    throw new Error('Failed to fetch user');
  }

  return response.json();
}

// Helper functions for token management
export function saveToken(token: string) {
  localStorage.setItem('authToken', token);
}

export function getToken(): string | null {
  return localStorage.getItem('authToken');
}

export function removeToken() {
  localStorage.removeItem('authToken');
}

export function saveUser(user: any) {
  localStorage.setItem('user', JSON.stringify(user));
}

export function getStoredUser() {
  const user = localStorage.getItem('user');
  return user ? JSON.parse(user) : null;
}
