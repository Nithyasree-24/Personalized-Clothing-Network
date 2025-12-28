# 🔐 Chat Logout Integration Guide

## 🎯 Overview
This guide shows how to integrate the FashionPulse chat with your authentication system to ensure chat sessions persist until user logout.

## 🔧 Integration Methods

### **Method 1: Using Global Function (Recommended)**

```javascript
// When user logs out, call this function
window.clearFashionPulseChat();

// Example in your logout handler:
const handleLogout = () => {
  // Your existing logout logic
  localStorage.removeItem('token');
  localStorage.removeItem('user_id');
  
  // Clear chat session
  window.clearFashionPulseChat();
  
  // Redirect to login
  window.location.href = '/login';
};
```

### **Method 2: Using Chat Session Manager**

```javascript
import { chatSessionManager } from '@/utils/chatSessionManager';

// When user logs in
const handleLogin = (userId, token) => {
  localStorage.setItem('user_id', userId);
  localStorage.setItem('token', token);
  
  // Initialize chat session
  chatSessionManager.initializeChatSession(userId);
};

// When user logs out
const handleLogout = () => {
  // Clear chat session
  chatSessionManager.clearChatSession();
  
  // Your existing logout logic
  localStorage.removeItem('token');
  localStorage.removeItem('user_id');
  
  // Redirect
  window.location.href = '/login';
};
```

### **Method 3: Using Custom Event**

```javascript
// Dispatch logout event (chat component listens for this)
window.dispatchEvent(new CustomEvent('fashionpulse-logout', {
  detail: { 
    userId: currentUserId, 
    timestamp: new Date().toISOString() 
  }
}));
```

## 📱 Implementation Examples

### **React Component Logout**

```tsx
// In your header/navbar component
import { chatSessionManager } from '@/utils/chatSessionManager';

const Header = () => {
  const handleLogout = async () => {
    try {
      // Clear chat session first
      chatSessionManager.clearChatSession();
      
      // Call your logout API
      await fetch('/api/logout', { method: 'POST' });
      
      // Clear local storage
      localStorage.clear();
      
      // Redirect
      router.push('/login');
    } catch (error) {
      console.error('Logout error:', error);
    }
  };

  return (
    <button onClick={handleLogout}>
      Logout
    </button>
  );
};
```

### **Next.js API Route Integration**

```typescript
// pages/api/logout.ts or app/api/logout/route.ts
export async function POST(request: Request) {
  // Your logout logic here
  
  return Response.json({ 
    success: true,
    message: 'Logged out successfully',
    clearChat: true // Signal to clear chat
  });
}
```

### **Vanilla JavaScript Integration**

```javascript
// In your main app.js or wherever you handle logout
document.getElementById('logout-btn').addEventListener('click', function() {
  // Clear chat session
  if (window.clearFashionPulseChat) {
    window.clearFashionPulseChat();
  }
  
  // Your logout logic
  fetch('/logout', { method: 'POST' })
    .then(() => {
      localStorage.clear();
      window.location.href = '/login';
    });
});
```

## 🔄 Chat Persistence Behavior

### **When Chat Persists:**
- ✅ User is logged in
- ✅ User navigates between pages
- ✅ User refreshes the page
- ✅ User closes and reopens browser (if still logged in)

### **When Chat Clears:**
- ❌ User explicitly logs out
- ❌ User session expires (if you implement session expiry)
- ❌ User clears browser data

## 🛠️ Advanced Configuration

### **User-Specific Chat Sessions**

```javascript
// Chat sessions are automatically user-specific
// Each user gets their own chat history stored as:
// localStorage key: `fashionpulse_chat_${userId}`

// Check current user's chat session
const sessionInfo = chatSessionManager.getChatSessionInfo();
console.log('User:', sessionInfo.userId);
console.log('Has chat history:', sessionInfo.hasSession);
```

### **Session Validation**

```javascript
// Check if chat should persist based on auth status
const shouldPersist = chatSessionManager.shouldPersistChat();

if (!shouldPersist) {
  // User not properly authenticated, clear chat
  chatSessionManager.clearChatSession();
}
```

## 🧪 Testing the Integration

### **Test Scenarios:**

1. **Login → Chat → Logout → Login**
   ```javascript
   // 1. Login as user1
   chatSessionManager.initializeChatSession('user1');
   
   // 2. Use chat, send messages
   // 3. Logout
   chatSessionManager.clearChatSession();
   
   // 4. Login as user2
   chatSessionManager.initializeChatSession('user2');
   
   // Expected: Fresh chat for user2
   ```

2. **Page Refresh Test**
   ```javascript
   // 1. Login and use chat
   // 2. Refresh page
   // Expected: Chat history restored
   
   // 3. Logout
   // 4. Refresh page
   // Expected: Fresh chat
   ```

3. **Multiple Users Test**
   ```javascript
   // Each user should have separate chat history
   // User1's chat should not appear for User2
   ```

## 🔍 Debugging

### **Check Chat Session Status**

```javascript
// Open browser console and run:
console.log('Chat Manager:', window.FashionPulseChatManager);
console.log('Session Info:', window.FashionPulseChatManager.getSessionInfo());
console.log('Should Persist:', window.FashionPulseChatManager.shouldPersist());

// Check localStorage
Object.keys(localStorage).filter(key => key.includes('fashionpulse_chat'));
```

### **Manual Chat Clear**

```javascript
// Clear chat manually in console
window.clearFashionPulseChat();

// Or using manager
window.FashionPulseChatManager.clearSession();
```

## 📋 Integration Checklist

- [ ] **Login Integration**: Call `initializeChatSession(userId)` on login
- [ ] **Logout Integration**: Call `clearChatSession()` on logout
- [ ] **User ID Storage**: Store user ID in localStorage as 'user_id'
- [ ] **Token Management**: Ensure auth token is available for persistence check
- [ ] **Event Handling**: Handle 'fashionpulse-logout' event if using custom events
- [ ] **Testing**: Test login/logout flow with chat persistence
- [ ] **Error Handling**: Handle cases where chat functions might not be available

## 🎯 Quick Implementation

**Minimal integration (add to your logout function):**

```javascript
const logout = () => {
  // Clear chat
  if (window.clearFashionPulseChat) {
    window.clearFashionPulseChat();
  }
  
  // Your existing logout code
  localStorage.clear();
  window.location.href = '/login';
};
```

That's it! The chat will now persist until the user logs out. 🎉